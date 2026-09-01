import os
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import optuna
from optuna.samplers import TPESampler
import shap

from sklearn.model_selection import StratifiedKFold, train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (
    roc_auc_score, precision_recall_curve, auc, 
    f1_score, precision_score, recall_score, roc_curve, confusion_matrix, classification_report
)
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
import lightgbm as lgb
import xgboost as xgb

optuna.logging.set_verbosity(optuna.logging.WARNING)

SEED = 42

class TaxComplianceAutoMLPipeline:
    def __init__(self, data_path: str, output_dir: str):
        self.data_path = data_path
        self.output_dir = output_dir
        self.images_dir = os.path.join(output_dir, "images")
        os.makedirs(self.images_dir, exist_ok=True)
        
        self.df = pd.read_csv(self.data_path)
        self.X = self.df.drop(columns=["provinsi", "target_compliance_risk"])
        self.y = self.df["target_compliance_risk"]
        
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            self.X, self.y, test_size=0.20, random_state=SEED, stratify=self.y
        )
        
        self.scaler = StandardScaler()
        self.X_train_scaled = self.scaler.fit_transform(self.X_train)
        self.X_test_scaled = self.scaler.transform(self.X_test)
        
        self.models = {}
        self.predictions = {}
        self.probabilities = {}

    def run_baselines(self):
        lr = LogisticRegression(random_state=SEED, max_iter=1000)
        lr.fit(self.X_train_scaled, self.y_train)
        self.models["Logistic Regression"] = lr
        self.probabilities["Logistic Regression"] = lr.predict_proba(self.X_test_scaled)[:, 1]
        self.predictions["Logistic Regression"] = lr.predict(self.X_test_scaled)
        
        rf = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=SEED)
        rf.fit(self.X_train, self.y_train)
        self.models["Random Forest"] = rf
        self.probabilities["Random Forest"] = rf.predict_proba(self.X_test)[:, 1]
        self.predictions["Random Forest"] = rf.predict(self.X_test)

    def optimize_automl(self, n_trials: int = 30):
        cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=SEED)
        
        def objective(trial):
            classifier_name = trial.suggest_categorical("classifier", ["LightGBM", "XGBoost"])
            
            if classifier_name == "LightGBM":
                params = {
                    "n_estimators": trial.suggest_int("lgb_n_estimators", 50, 250),
                    "learning_rate": trial.suggest_float("lgb_lr", 0.01, 0.2, log=True),
                    "num_leaves": trial.suggest_int("lgb_num_leaves", 15, 127),
                    "max_depth": trial.suggest_int("lgb_max_depth", 3, 10),
                    "subsample": trial.suggest_float("lgb_subsample", 0.6, 1.0),
                    "colsample_bytree": trial.suggest_float("lgb_colsample", 0.6, 1.0),
                    "random_state": SEED,
                    "verbose": -1
                }
                model = lgb.LGBMClassifier(**params)
            else:
                params = {
                    "n_estimators": trial.suggest_int("xgb_n_estimators", 50, 250),
                    "learning_rate": trial.suggest_float("xgb_lr", 0.01, 0.2, log=True),
                    "max_depth": trial.suggest_int("xgb_max_depth", 3, 10),
                    "subsample": trial.suggest_float("xgb_subsample", 0.6, 1.0),
                    "colsample_bytree": trial.suggest_float("xgb_colsample", 0.6, 1.0),
                    "random_state": SEED,
                    "eval_metric": "logloss"
                }
                model = xgb.XGBClassifier(**params)
                
            scores = []
            for train_idx, val_idx in cv.split(self.X_train, self.y_train):
                X_tr, X_val = self.X_train.iloc[train_idx], self.X_train.iloc[val_idx]
                y_tr, y_val = self.y_train.iloc[train_idx], self.y_train.iloc[val_idx]
                model.fit(X_tr, y_tr)
                preds = model.predict_proba(X_val)[:, 1]
                scores.append(roc_auc_score(y_val, preds))
            return np.mean(scores)
            
        study = optuna.create_study(direction="maximize", sampler=TPESampler(seed=SEED))
        study.optimize(objective, n_trials=n_trials)
        
        best_params = study.best_params
        best_type = best_params["classifier"]
        
        if best_type == "LightGBM":
            best_model = lgb.LGBMClassifier(
                n_estimators=best_params["lgb_n_estimators"],
                learning_rate=best_params["lgb_lr"],
                num_leaves=best_params["lgb_num_leaves"],
                max_depth=best_params["lgb_max_depth"],
                subsample=best_params["lgb_subsample"],
                colsample_bytree=best_params["lgb_colsample"],
                random_state=SEED,
                verbose=-1
            )
        else:
            best_model = xgb.XGBClassifier(
                n_estimators=best_params["xgb_n_estimators"],
                learning_rate=best_params["xgb_lr"],
                max_depth=best_params["xgb_max_depth"],
                subsample=best_params["xgb_subsample"],
                colsample_bytree=best_params["xgb_colsample"],
                random_state=SEED,
                eval_metric="logloss"
            )
            
        best_model.fit(self.X_train, self.y_train)
        self.models[f"AutoML ({best_type})"] = best_model
        self.probabilities[f"AutoML ({best_type})"] = best_model.predict_proba(self.X_test)[:, 1]
        self.predictions[f"AutoML ({best_type})"] = best_model.predict(self.X_test)
        self.best_model_name = f"AutoML ({best_type})"
        self.best_model = best_model

    def evaluate_and_plot(self) -> dict:
        results = {}
        
        for name, probs in self.probabilities.items():
            preds = self.predictions[name]
            auc_score = roc_auc_score(self.y_test, probs)
            prec_pts, rec_pts, _ = precision_recall_curve(self.y_test, probs)
            pr_auc = auc(rec_pts, prec_pts)
            
            results[name] = {
                "ROC-AUC": round(auc_score, 4),
                "PR-AUC": round(pr_auc, 4),
                "F1-Score": round(f1_score(self.y_test, preds), 4),
                "Precision": round(precision_score(self.y_test, preds), 4),
                "Recall": round(recall_score(self.y_test, preds), 4)
            }
            
        # 1. ROC Curves
        plt.figure(figsize=(7, 5), dpi=300)
        for name, probs in self.probabilities.items():
            fpr, tpr, _ = roc_curve(self.y_test, probs)
            score = results[name]["ROC-AUC"]
            plt.plot(fpr, tpr, label=f"{name} (AUC = {score:.4f})")
        plt.plot([0, 1], [0, 1], "k--", alpha=0.4)
        plt.xlabel("False Positive Rate")
        plt.ylabel("True Positive Rate")
        plt.title("ROC Curves: Model Evaluation on Holdout Test Set")
        plt.legend(loc="lower right")
        plt.tight_layout()
        plt.savefig(os.path.join(self.images_dir, "figure1_roc_auc_curve.png"))
        plt.close()
        
        # 2. Cumulative Decile Gains
        best_probs = self.probabilities[self.best_model_name]
        gains_df = pd.DataFrame({"y_true": self.y_test, "prob": best_probs})
        gains_df["decile"] = pd.qcut(gains_df["prob"], q=10, labels=False, duplicates="drop")
        gains_df["decile"] = 10 - gains_df["decile"]
        
        decile_summary = gains_df.groupby("decile")["y_true"].sum().reset_index()
        decile_summary["cum_gains"] = decile_summary["y_true"].cumsum()
        decile_summary["cum_gains_pct"] = decile_summary["cum_gains"] / decile_summary["y_true"].sum() * 100.0
        
        plt.figure(figsize=(7, 5), dpi=300)
        plt.plot(decile_summary["decile"], decile_summary["cum_gains_pct"], marker="o", color="#b91c1c", label="AutoML Model Gains")
        plt.plot([1, 10], [10, 100], "k--", alpha=0.4, label="Random Audit Baseline")
        plt.xlabel("Decile (1 = Highest Predicted Risk, 10 = Lowest)")
        plt.ylabel("Cumulative Identified Non-Compliant Taxpayers (%)")
        plt.title("Cumulative Audit Yield by Risk Decile")
        plt.xticks(range(1, 11))
        plt.grid(True, linestyle=":", alpha=0.5)
        plt.legend()
        plt.tight_layout()
        plt.savefig(os.path.join(self.images_dir, "figure2_cumulative_gains_decile.png"))
        plt.close()
        
        # 3. SHAP Feature Importance & Interpretability (Anti-Black-Box)
        explainer = shap.TreeExplainer(self.best_model)
        shap_values = explainer(self.X_test)
        
        plt.figure(figsize=(8, 5), dpi=300)
        shap.summary_plot(shap_values, self.X_test, show=False)
        plt.title("SHAP Feature Importance: Explaining Tax Compliance Risk Factors")
        plt.tight_layout()
        plt.savefig(os.path.join(self.images_dir, "figure3_shap_feature_importance.png"))
        plt.close()
        
        # 4. Confusion Matrix Normalized
        cm = confusion_matrix(self.y_test, self.predictions[self.best_model_name], normalize='true')
        plt.figure(figsize=(6, 5), dpi=300)
        sns.heatmap(cm, annot=True, fmt=".2%", cmap="Blues", cbar=False,
                    xticklabels=["Patuh (0)", "Berisiko (1)"],
                    yticklabels=["Patuh (0)", "Berisiko (1)"])
        plt.xlabel("Prediksi Model")
        plt.ylabel("Kondisi Riil")
        plt.title("Normalized Confusion Matrix: AutoML Risk Classifier")
        plt.tight_layout()
        plt.savefig(os.path.join(self.images_dir, "figure4_confusion_matrix.png"))
        plt.close()
        
        top20_pct = float(decile_summary.loc[decile_summary["decile"] <= 2, "cum_gains_pct"].max())
        results["top20_decile_gain_pct"] = round(top20_pct, 2)
        return results

if __name__ == "__main__":
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data = os.path.join(base, "data", "bps_e_commerce_tax_compliance.csv")
    pipeline = TaxComplianceAutoMLPipeline(data_path=data, output_dir=base)
    pipeline.run_baselines()
    pipeline.optimize_automl(n_trials=30)
    summary = pipeline.evaluate_and_plot()
    print(json.dumps(summary, indent=2))
