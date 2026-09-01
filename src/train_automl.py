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

def bootstrap_ci(y_true, y_prob, metric="roc_auc", n_bootstraps=500):
    rng = np.random.default_rng(SEED)
    scores = []
    y_true = np.array(y_true)
    y_prob = np.array(y_prob)
    for _ in range(n_bootstraps):
        idx = rng.choice(len(y_true), size=len(y_true), replace=True)
        if len(np.unique(y_true[idx])) < 2:
            continue
        if metric == "roc_auc":
            scores.append(roc_auc_score(y_true[idx], y_prob[idx]))
        elif metric == "pr_auc":
            p, r, _ = precision_recall_curve(y_true[idx], y_prob[idx])
            scores.append(auc(r, p))
    return float(np.percentile(scores, 2.5)), float(np.percentile(scores, 97.5))

def run_benchmarks(data_path: str = "data/bps_e_commerce_tax_compliance.csv") -> dict:
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
        "AutoML XGBoost": (xgb.XGBClassifier(
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
        auc_ci = bootstrap_ci(y_te, p, "roc_auc")
        pr_ci = bootstrap_ci(y_te, p, "pr_auc")
        
        gdf = pd.DataFrame({"y": y_te, "p": p})
        gdf["d"] = 10 - pd.qcut(gdf["p"], q=10, labels=False, duplicates="drop")
        top20_yield = gdf[gdf["d"] <= 2]["y"].sum() / gdf["y"].sum() * 100.0
        
        res[name] = {
            "ROC_AUC": round(roc_auc_score(y_te, p), 4),
            "ROC_AUC_95CI": f"[{auc_ci[0]:.4f}, {auc_ci[1]:.4f}]",
            "PR_AUC": round(auc(pr_r, pr_p), 4),
            "PR_AUC_95CI": f"[{pr_ci[0]:.4f}, {pr_ci[1]:.4f}]",
            "F1": round(f1_score(y_te, pred), 4),
            "Precision": round(precision_score(y_te, pred), 4),
            "Recall": round(recall_score(y_te, pred), 4),
            "Specificity": round(cm[0, 0] / (cm[0, 0] + cm[0, 1]), 4),
            "Top20_Decile_Yield_Pct": round(top20_yield, 2),
            "Cumulative_Lift": round(top20_yield / 20.0, 2),
            "CM": {"TN": int(cm[0, 0]), "FP": int(cm[0, 1]), "FN": int(cm[1, 0]), "TP": int(cm[1, 1])}
        }
        
    # Feature Ablation
    subsets = {
        "1. Financial/SPT Only": ["reported_turnover_spt_juta", "tax_paid_final_juta"],
        "2. + Digital Transactions": ["reported_turnover_spt_juta", "tax_paid_final_juta", "gmv_transaksi_juta", "annual_order_volume", "avg_ticket_size_ribu", "digital_payment_ratio"],
        "3. + Logistics Tracking": ["reported_turnover_spt_juta", "tax_paid_final_juta", "gmv_transaksi_juta", "annual_order_volume", "avg_ticket_size_ribu", "digital_payment_ratio", "logistics_tracking_ratio", "customer_return_rate"],
        "4. Full Model (+ BPS Regional Macro)": features
    }
    ablation = {}
    for s_name, cols in subsets.items():
        m = xgb.XGBClassifier(n_estimators=bp["n_estimators"], learning_rate=bp["lr"], max_depth=bp["max_depth"], random_state=SEED, eval_metric="logloss").fit(X_tr[cols], y_tr)
        p = m.predict_proba(X_te[cols])[:, 1]
        pr_p, pr_r, _ = precision_recall_curve(y_te, p)
        gdf = pd.DataFrame({"y": y_te, "p": p})
        gdf["d"] = 10 - pd.qcut(gdf["p"], q=10, labels=False, duplicates="drop")
        top20_g = gdf[gdf["d"] <= 2]["y"].sum() / gdf["y"].sum() * 100.0
        ablation[s_name] = {
            "ROC_AUC": round(roc_auc_score(y_te, p), 4),
            "PR_AUC": round(auc(pr_r, pr_p), 4),
            "Top20_Decile_Yield": round(top20_g, 2),
            "Lift": round(top20_g / 20.0, 2)
        }
        
    # Repeated Geographical Holdout (5 fold provinces pairing)
    provinces = df["provinsi"].unique()
    geo_scores = []
    for i in range(0, len(provinces), 2):
        pair = [provinces[i], provinces[i+1]]
        tr_g = df[~df["provinsi"].isin(pair)]
        te_g = df[df["provinsi"].isin(pair)]
        m_g = xgb.XGBClassifier(n_estimators=bp["n_estimators"], learning_rate=bp["lr"], max_depth=bp["max_depth"], random_state=SEED, eval_metric="logloss").fit(tr_g[features], tr_g["target_non_compliance"])
        p_g = m_g.predict_proba(te_g[features])[:, 1]
        geo_scores.append(roc_auc_score(te_g["target_non_compliance"], p_g))
        
    return {
        "models": res,
        "ablation": ablation,
        "repeated_geo_holdout_mean": round(float(np.mean(geo_scores)), 4),
        "repeated_geo_holdout_std": round(float(np.std(geo_scores)), 4)
    }

if __name__ == "__main__":
    out = run_benchmarks()
    print(json.dumps(out, indent=2))
