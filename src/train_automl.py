import os
import json
import numpy as np
import pandas as pd
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
import optuna

optuna.logging.set_verbosity(optuna.logging.WARNING)
SEED = 42

def evaluate_models(data_path: str = "data/bps_e_commerce_tax_compliance.csv") -> dict:
    df = pd.read_csv(data_path)
    features = [
        "gmv_transaksi_juta", "annual_order_volume", "avg_ticket_size_ribu",
        "digital_payment_ratio", "logistics_tracking_ratio", "customer_return_rate",
        "bps_ecom_penetration_pct", "bps_infra_index",
        "reported_turnover_spt_juta", "tax_paid_final_juta"
    ]
    X, y = df[features], df["target_non_compliance"]
    
    X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, random_state=SEED, stratify=y)
    
    scaler = StandardScaler()
    X_tr_s = scaler.fit_transform(X_tr)
    X_te_s = scaler.transform(X_te)
    
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=SEED)
    
    def objective(trial):
        params = {
            "n_estimators": trial.suggest_int("n_estimators", 50, 200),
            "learning_rate": trial.suggest_float("lr", 0.01, 0.2, log=True),
            "max_depth": trial.suggest_int("max_depth", 3, 6),
            "subsample": trial.suggest_float("subsample", 0.7, 1.0),
            "colsample_bytree": trial.suggest_float("colsample", 0.7, 1.0),
            "random_state": SEED,
            "eval_metric": "logloss"
        }
        scores = [
            roc_auc_score(y_tr.iloc[v], xgb.XGBClassifier(**params).fit(X_tr.iloc[t], y_tr.iloc[t]).predict_proba(X_tr.iloc[v])[:, 1])
            for t, v in cv.split(X_tr, y_tr)
        ]
        return np.mean(scores)
        
    study = optuna.create_study(direction="maximize", sampler=optuna.samplers.TPESampler(seed=SEED))
    study.optimize(objective, n_trials=20)
    bp = study.best_params
    
    models = {
        "Logistic Regression": (LogisticRegression(max_iter=500, random_state=SEED).fit(X_tr_s, y_tr), X_te_s),
        "Random Forest": (RandomForestClassifier(n_estimators=100, max_depth=8, random_state=SEED).fit(X_tr, y_tr), X_te),
        "LightGBM": (lgb.LGBMClassifier(random_state=SEED, verbose=-1).fit(X_tr, y_tr), X_te),
        "AutoML (XGBoost TPE)": (xgb.XGBClassifier(
            n_estimators=bp["n_estimators"], learning_rate=bp["lr"],
            max_depth=bp["max_depth"], subsample=bp["subsample"],
            colsample_bytree=bp["colsample"], random_state=SEED, eval_metric="logloss"
        ).fit(X_tr, y_tr), X_te)
    }
    
    res = {}
    for name, (mod, x_eval) in models.items():
        p = mod.predict_proba(x_eval)[:, 1]
        pred = mod.predict(x_eval)
        pr_p, pr_r, _ = precision_recall_curve(y_te, p)
        cm = confusion_matrix(y_te, pred)
        res[name] = {
            "Holdout_ROC_AUC": round(roc_auc_score(y_te, p), 4),
            "PR_AUC": round(auc(pr_r, pr_p), 4),
            "F1": round(f1_score(y_te, pred), 4),
            "Precision": round(precision_score(y_te, pred), 4),
            "Recall": round(recall_score(y_te, pred), 4),
            "Specificity": round(cm[0, 0] / (cm[0, 0] + cm[0, 1]), 4),
            "CM": cm.tolist()
        }
        
    # Ablation
    subsets = {
        "SPT_Only": ["reported_turnover_spt_juta", "tax_paid_final_juta"],
        "Digital_Trans": ["reported_turnover_spt_juta", "tax_paid_final_juta", "gmv_transaksi_juta", "annual_order_volume", "avg_ticket_size_ribu", "digital_payment_ratio"],
        "Logistics": ["reported_turnover_spt_juta", "tax_paid_final_juta", "gmv_transaksi_juta", "annual_order_volume", "avg_ticket_size_ribu", "digital_payment_ratio", "logistics_tracking_ratio", "customer_return_rate"],
        "Full_BPS": features
    }
    ablation = {}
    for s_name, cols in subsets.items():
        m = xgb.XGBClassifier(n_estimators=bp["n_estimators"], learning_rate=bp["lr"], max_depth=bp["max_depth"], random_state=SEED, eval_metric="logloss").fit(X_tr[cols], y_tr)
        p = m.predict_proba(X_te[cols])[:, 1]
        pr_p, pr_r, _ = precision_recall_curve(y_te, p)
        gdf = pd.DataFrame({"y": y_te, "p": p})
        gdf["d"] = 10 - pd.qcut(gdf["p"], q=10, labels=False, duplicates="drop")
        ablation[s_name] = {
            "ROC_AUC": round(roc_auc_score(y_te, p), 4),
            "PR_AUC": round(auc(pr_r, pr_p), 4),
            "Top20_Decile_Yield": round(gdf[gdf["d"] <= 2]["y"].sum() / gdf["y"].sum() * 100, 2)
        }
        
    # Spatial Holdout (Bali & Sulsel)
    geo_hold = ["Bali", "Sulawesi Selatan"]
    tr_g, te_g = df[~df["provinsi"].isin(geo_hold)], df[df["provinsi"].isin(geo_hold)]
    m_geo = xgb.XGBClassifier(n_estimators=bp["n_estimators"], learning_rate=bp["lr"], max_depth=bp["max_depth"], random_state=SEED, eval_metric="logloss").fit(tr_g[features], tr_g["target_non_compliance"])
    p_geo = m_geo.predict_proba(te_g[features])[:, 1]
    
    return {
        "models": res,
        "ablation": ablation,
        "spatial_holdout_auc": round(roc_auc_score(te_g["target_non_compliance"], p_geo), 4)
    }

if __name__ == "__main__":
    print(json.dumps(evaluate_models(), indent=2))
