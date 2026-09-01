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
import xgboost as xgb
import optuna

optuna.logging.set_verbosity(optuna.logging.WARNING)
SEED = 42

def test_prediction_bootstrap_ci(y_true, y_prob, metric="roc_auc", n_bootstraps=500):
    """
    R4 Compliance: Non-parametric bootstrap resampling strictly on held-out test predictions
    with fixed trained model parameters to compute empirical 95% Confidence Intervals.
    """
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

def run_dgp_sensitivity_analysis(seed=42):
    """
    R8 Compliance: DGP Sensitivity Analysis across alternative latent parameter weights:
    Scenario A (Baseline): 40/35/25
    Scenario B (Inventory Heavy): 25/50/25
    Scenario C (Logistics Heavy): 30/25/45
    """
    rng = np.random.default_rng(seed)
    n = 5000
    d_cash = rng.beta(2.0, 4.0, size=n)
    d_inv = rng.exponential(0.25, size=n)
    d_log = rng.beta(1.5, 4.5, size=n)
    noise = rng.normal(0, 0.08, size=n)
    
    scenarios = {
        "Scenario A (40/35/25)": (0.40, 0.35, 0.25),
        "Scenario B (25/50/25)": (0.25, 0.50, 0.25),
        "Scenario C (30/25/45)": (0.30, 0.25, 0.45)
    }
    
    sens_res = {}
    for sc_name, (w_c, w_i, w_l) in scenarios.items():
        score = w_c * d_cash + w_i * (d_inv / (1.0 + d_inv)) + w_l * d_log + noise
        y = (score > np.percentile(score, 75.0)).astype(int)
        
        # Observable proxies
        gmv = (rng.poisson(140, size=n) + 20) * (rng.lognormal(4.8, 0.6, size=n) + 25.0) / 1000.0
        pay = np.clip(1.0 - (0.6 * d_cash + rng.normal(0.2, 0.1, size=n)), 0.05, 0.99)
        log = np.clip(1.0 - (0.5 * d_log + rng.normal(0.15, 0.08, size=n)), 0.10, 1.00)
        u_frac = np.clip(0.4 * d_cash + 0.3 * (d_inv / (1.0 + d_inv)) + rng.normal(0.1, 0.1, size=n), 0.0, 0.85)
        spt = gmv * (1.0 - u_frac)
        
        X = pd.DataFrame({"gmv": gmv, "pay": pay, "log": log, "spt": spt})
        X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, random_state=seed, stratify=y)
        
        lr_auc = roc_auc_score(y_te, LogisticRegression().fit(StandardScaler().fit_transform(X_tr), y_tr).predict_proba(StandardScaler().fit(X_tr).transform(X_te))[:, 1])
        xgb_auc = roc_auc_score(y_te, xgb.XGBClassifier(n_estimators=100, max_depth=4, random_state=seed, eval_metric="logloss").fit(X_tr, y_tr).predict_proba(X_te)[:, 1])
        sens_res[sc_name] = {"Logistic_ROC_AUC": round(lr_auc, 4), "XGBoost_ROC_AUC": round(xgb_auc, 4)}
    return sens_res

if __name__ == "__main__":
    sens = run_dgp_sensitivity_analysis()
    print("DGP Sensitivity Analysis Results:")
    print(json.dumps(sens, indent=2))
