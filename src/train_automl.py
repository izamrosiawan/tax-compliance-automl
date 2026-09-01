import os
import json
import numpy as np
import pandas as pd
import optuna
from optuna.samplers import TPESampler

from sklearn.model_selection import StratifiedKFold, train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (
    roc_auc_score, precision_recall_curve, auc, 
    f1_score, precision_score, recall_score, confusion_matrix
)
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
import lightgbm as lgb
import xgboost as xgb

optuna.logging.set_verbosity(optuna.logging.WARNING)
SEED = 42

class RobustTaxCompliancePipeline:
    def __init__(self, data_path: str):
        self.df = pd.read_csv(data_path)
        self.feature_cols = [
            "gmv_transaksi_juta", "annual_order_volume", "avg_ticket_size_ribu",
            "digital_payment_ratio", "logistics_tracking_ratio", "customer_return_rate",
            "bps_ecom_penetration_pct", "bps_infra_index",
            "reported_turnover_spt_juta", "tax_paid_final_juta"
        ]
        self.target_col = "target_non_compliance"
        
        # 1. Standard Split (Stratified 80/20)
        self.X = self.df[self.feature_cols]
        self.y = self.df[self.target_col]
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            self.X, self.y, test_size=0.20, random_state=SEED, stratify=self.y
        )
        
        self.scaler = StandardScaler()
        self.X_train_scaled = self.scaler.fit_transform(self.X_train)
        self.X_test_scaled = self.scaler.transform(self.X_test)

    def run_all_evaluations(self) -> dict:
        results = {}
        
        # A. Baseline Models
        lr = LogisticRegression(random_state=SEED, max_iter=1000).fit(self.X_train_scaled, self.y_train)
        rf = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=SEED).fit(self.X_train, self.y_train)
        lgbm = lgb.LGBMClassifier(random_state=SEED, verbose=-1).fit(self.X_train, self.y_train)
        
        # B. Bayesian AutoML Optimization (TPE on XGBoost)
        cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=SEED)
        def objective(trial):
            params = {
                "n_estimators": trial.suggest_int("n_estimators", 50, 250),
                "learning_rate": trial.suggest_float("lr", 0.01, 0.20, log=True),
                "max_depth": trial.suggest_int("max_depth", 3, 8),
                "subsample": trial.suggest_float("subsample", 0.6, 1.0),
                "colsample_bytree": trial.suggest_float("colsample", 0.6, 1.0),
                "random_state": SEED,
                "eval_metric": "logloss"
            }
            model = xgb.XGBClassifier(**params)
            scores = []
            for tr_idx, val_idx in cv.split(self.X_train, self.y_train):
                X_tr, X_val = self.X_train.iloc[tr_idx], self.X_train.iloc[val_idx]
                y_tr, y_val = self.y_train.iloc[tr_idx], self.y_train.iloc[val_idx]
                model.fit(X_tr, y_tr)
                scores.append(roc_auc_score(y_val, model.predict_proba(X_val)[:, 1]))
            return np.mean(scores)
            
        study = optuna.create_study(direction="maximize", sampler=TPESampler(seed=SEED))
        study.optimize(objective, n_trials=30)
        
        bp = study.best_params
        best_xgb = xgb.XGBClassifier(
            n_estimators=bp["n_estimators"], learning_rate=bp["lr"],
            max_depth=bp["max_depth"], subsample=bp["subsample"],
            colsample_bytree=bp["colsample"], random_state=SEED, eval_metric="logloss"
        ).fit(self.X_train, self.y_train)
        
        models_dict = {
            "Logistic Regression": (lr, self.X_test_scaled),
            "Random Forest": (rf, self.X_test),
            "LightGBM": (lgbm, self.X_test),
            "AutoML (XGBoost TPE)": (best_xgb, self.X_test)
        }
        
        # Compute 5-Fold CV metrics on Train Set
        cv_scores = {}
        for m_name, (m_obj, _) in models_dict.items():
            m_cv_auc = []
            for tr_idx, val_idx in cv.split(self.X_train, self.y_train):
                if m_name == "Logistic Regression":
                    X_tr = self.scaler.fit_transform(self.X_train.iloc[tr_idx])
                    X_v = self.scaler.transform(self.X_train.iloc[val_idx])
                else:
                    X_tr = self.X_train.iloc[tr_idx]
                    X_v = self.X_train.iloc[val_idx]
                y_tr, y_v = self.y_train.iloc[tr_idx], self.y_train.iloc[val_idx]
                m_obj.fit(X_tr, y_tr)
                m_cv_auc.append(roc_auc_score(y_v, m_obj.predict_proba(X_v)[:, 1]))
            cv_scores[m_name] = (np.mean(m_cv_auc), np.std(m_cv_auc))
            
        # Re-fit on full train set
        lr.fit(self.X_train_scaled, self.y_train)
        rf.fit(self.X_train, self.y_train)
        lgbm.fit(self.X_train, self.y_train)
        best_xgb.fit(self.X_train, self.y_train)
        
        perf_summary = {}
        for name, (mod, x_eval) in models_dict.items():
            probs = mod.predict_proba(x_eval)[:, 1]
            preds = mod.predict(x_eval)
            p_pts, r_pts, _ = precision_recall_curve(self.y_test, probs)
            cm = confusion_matrix(self.y_test, preds)
            tn, fp, fn, tp = cm.ravel()
            specificity = tn / (tn + fp)
            
            perf_summary[name] = {
                "CV_ROC_AUC": f"{cv_scores[name][0]:.4f} +/- {cv_scores[name][1]:.4f}",
                "Holdout_ROC_AUC": round(roc_auc_score(self.y_test, probs), 4),
                "PR_AUC": round(auc(r_pts, p_pts), 4),
                "F1_Score": round(f1_score(self.y_test, preds), 4),
                "Precision": round(precision_score(self.y_test, preds), 4),
                "Recall": round(recall_score(self.y_test, preds), 4),
                "Specificity": round(specificity, 4),
                "Confusion_Matrix": {"TN": int(tn), "FP": int(fp), "FN": int(fn), "TP": int(tp)}
            }
        results["Model_Comparison"] = perf_summary
        
        # C. Feature Ablation Study (Klaim Kontribusi Ilmiah Indikator BPS)
        ablation_subsets = {
            "1. Financial/SPT Only": ["reported_turnover_spt_juta", "tax_paid_final_juta"],
            "2. + Digital Transaction (Gateway & Vol)": [
                "reported_turnover_spt_juta", "tax_paid_final_juta",
                "gmv_transaksi_juta", "annual_order_volume", "avg_ticket_size_ribu", "digital_payment_ratio"
            ],
            "3. + Logistics & Supply Chain": [
                "reported_turnover_spt_juta", "tax_paid_final_juta",
                "gmv_transaksi_juta", "annual_order_volume", "avg_ticket_size_ribu", "digital_payment_ratio",
                "logistics_tracking_ratio", "customer_return_rate"
            ],
            "4. Full Model (+ BPS Contextual Macro)": self.feature_cols
        }
        
        ablation_summary = {}
        for subset_name, cols in ablation_subsets.items():
            sub_xgb = xgb.XGBClassifier(
                n_estimators=bp["n_estimators"], learning_rate=bp["lr"],
                max_depth=bp["max_depth"], subsample=bp["subsample"],
                colsample_bytree=bp["colsample"], random_state=SEED, eval_metric="logloss"
            )
            sub_xgb.fit(self.X_train[cols], self.y_train)
            sub_probs = sub_xgb.predict_proba(self.X_test[cols])[:, 1]
            sub_preds = sub_xgb.predict(self.X_test[cols])
            p_pts, r_pts, _ = precision_recall_curve(self.y_test, sub_probs)
            
            # Decile top 20% gain
            gdf = pd.DataFrame({"y": self.y_test, "p": sub_probs})
            gdf["decile"] = 10 - pd.qcut(gdf["p"], q=10, labels=False, duplicates="drop")
            top20_gain = gdf[gdf["decile"] <= 2]["y"].sum() / gdf["y"].sum() * 100.0
            
            ablation_summary[subset_name] = {
                "ROC_AUC": round(roc_auc_score(self.y_test, sub_probs), 4),
                "PR_AUC": round(auc(r_pts, p_pts), 4),
                "F1_Score": round(f1_score(self.y_test, sub_preds), 4),
                "Top20_Decile_Gain_Pct": round(top20_gain, 2)
            }
        results["Ablation_Study"] = ablation_summary
        
        # D. Geographical Out-of-Province Generalization (Robustness Test)
        # Train on 8 provinces, Test on 2 holdout unseen provinces (Bali & Sulawesi Selatan)
        holdout_provinces = ["Bali", "Sulawesi Selatan"]
        train_geo_df = self.df[~self.df["provinsi"].isin(holdout_provinces)]
        test_geo_df = self.df[self.df["provinsi"].isin(holdout_provinces)]
        
        geo_xgb = xgb.XGBClassifier(
            n_estimators=bp["n_estimators"], learning_rate=bp["lr"],
            max_depth=bp["max_depth"], subsample=bp["subsample"],
            colsample_bytree=bp["colsample"], random_state=SEED, eval_metric="logloss"
        )
        geo_xgb.fit(train_geo_df[self.feature_cols], train_geo_df[self.target_col])
        geo_probs = geo_xgb.predict_proba(test_geo_df[self.feature_cols])[:, 1]
        geo_preds = geo_xgb.predict(test_geo_df[self.feature_cols])
        p_pts, r_pts, _ = precision_recall_curve(test_geo_df[self.target_col], geo_probs)
        
        results["Geographical_Holdout_Test"] = {
            "Unseen_Provinces": holdout_provinces,
            "Train_Samples": len(train_geo_df),
            "Test_Samples": len(test_geo_df),
            "Holdout_ROC_AUC": round(roc_auc_score(test_geo_df[self.target_col], geo_probs), 4),
            "Holdout_PR_AUC": round(auc(r_pts, p_pts), 4),
            "Holdout_F1_Score": round(f1_score(test_geo_df[self.target_col], geo_preds), 4)
        }
        
        return results

if __name__ == "__main__":
    data_file = os.path.join(os.path.dirname(__file__), "..", "data", "bps_e_commerce_tax_compliance.csv")
    pipeline = RobustTaxCompliancePipeline(data_file)
    res = pipeline.run_all_evaluations()
    print(json.dumps(res, indent=2))
