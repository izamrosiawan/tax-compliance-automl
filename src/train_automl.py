import os
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (
    roc_auc_score, precision_recall_curve, auc, 
    f1_score, precision_score, recall_score, confusion_matrix, classification_report
)
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
import lightgbm as lgb
from flaml import AutoML

# 1. Obey Deterministic Seed & Anti-Leakage Rules
SEED = 42
np.random.seed(SEED)

def run_tax_compliance_automl_pipeline():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_path = os.path.join(base_dir, "data", "bps_e_commerce_tax_compliance.csv")
    images_dir = os.path.join(base_dir, "images")
    os.makedirs(images_dir, exist_ok=True)
    
    print("=== 1. INGESTING BPS DIGITAL TAX DATASET ===")
    df = pd.read_csv(data_path)
    print(f"Dataset Shape: {df.shape}")
    
    # Feature & Target Separation
    X = df.drop(columns=['provinsi', 'target_compliance_risk'])
    y = df['target_compliance_risk']
    
    # 2. Strict Train-Test Split (BEFORE scaling/imputation to avoid Data Leakage)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=SEED, stratify=y
    )
    print(f"Train Shape: {X_train.shape} | Test Shape: {X_test.shape}")
    
    # Scale Features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # 3. Model 1: Logistic Regression (Baseline)
    print("\n=== 2. TRAINING BASELINE (LOGISTIC REGRESSION) ===")
    lr_model = LogisticRegression(random_state=SEED, max_iter=1000)
    lr_model.fit(X_train_scaled, y_train)
    y_pred_lr_prob = lr_model.predict_proba(X_test_scaled)[:, 1]
    y_pred_lr = lr_model.predict(X_test_scaled)
    
    auc_lr = roc_auc_score(y_test, y_pred_lr_prob)
    precision_lr_pts, recall_lr_pts, _ = precision_recall_curve(y_test, y_pred_lr_prob)
    pr_auc_lr = auc(recall_lr_pts, precision_lr_pts)
    f1_lr = f1_score(y_test, y_pred_lr)
    
    print(f"Logistic Regression -> ROC-AUC: {auc_lr:.4f} | PR-AUC: {pr_auc_lr:.4f} | F1: {f1_lr:.4f}")
    
    # 4. Model 2: Random Forest (Manual Tuned)
    print("\n=== 3. TRAINING RANDOM FOREST ===")
    rf_model = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=SEED)
    rf_model.fit(X_train, y_train)
    y_pred_rf_prob = rf_model.predict_proba(X_test)[:, 1]
    y_pred_rf = rf_model.predict(X_test)
    
    auc_rf = roc_auc_score(y_test, y_pred_rf_prob)
    precision_rf_pts, recall_rf_pts, _ = precision_recall_curve(y_test, y_pred_rf_prob)
    pr_auc_rf = auc(recall_rf_pts, precision_rf_pts)
    f1_rf = f1_score(y_test, y_pred_rf)
    
    print(f"Random Forest -> ROC-AUC: {auc_rf:.4f} | PR-AUC: {pr_auc_rf:.4f} | F1: {f1_rf:.4f}")
    
    # 5. Model 3: AutoML (FLAML LightGBM)
    print("\n=== 4. TRAINING AUTOMATED MACHINE LEARNING (FLAML AUTOML) ===")
    automl = AutoML()
    automl_settings = {
        "time_budget": 30,  # 30 seconds search
        "metric": "roc_auc",
        "task": "classification",
        "seed": SEED,
        "verbose": 0
    }
    automl.fit(X_train=X_train, y_train=y_train, **automl_settings)
    
    y_pred_automl_prob = automl.predict_proba(X_test)[:, 1]
    y_pred_automl = automl.predict(X_test)
    
    auc_automl = roc_auc_score(y_test, y_pred_automl_prob)
    precision_automl_pts, recall_automl_pts, _ = precision_recall_curve(y_test, y_pred_automl_prob)
    pr_auc_automl = auc(recall_automl_pts, precision_automl_pts)
    f1_automl = f1_score(y_test, y_pred_automl)
    prec_automl = precision_score(y_test, y_pred_automl)
    rec_automl = recall_score(y_test, y_pred_automl)
    
    print(f"AutoML Best Model ({automl.best_estimator}) -> ROC-AUC: {auc_automl:.4f} | PR-AUC: {pr_auc_automl:.4f} | F1: {f1_automl:.4f}")
    
    # 6. Save Plots (300 DPI for Academic Publication)
    print("\n=== 5. GENERATING PUBLICATION-GRADE PLOTS (300 DPI) ===")
    
    # Plot 1: ROC Curve Comparison
    plt.figure(figsize=(7, 5), dpi=300)
    from sklearn.metrics import roc_curve
    fpr_lr, tpr_lr, _ = roc_curve(y_test, y_pred_lr_prob)
    fpr_rf, tpr_rf, _ = roc_curve(y_test, y_pred_rf_prob)
    fpr_am, tpr_am, _ = roc_curve(y_test, y_pred_automl_prob)
    
    plt.plot(fpr_lr, tpr_lr, label=f'Logistic Regression (AUC = {auc_lr:.4f})', linestyle='--')
    plt.plot(fpr_rf, tpr_rf, label=f'Random Forest (AUC = {auc_rf:.4f})', linestyle='-.')
    plt.plot(fpr_am, tpr_am, label=f'AutoML LightGBM (AUC = {auc_automl:.4f})', linewidth=2, color='darkblue')
    plt.plot([0, 1], [0, 1], 'k--', alpha=0.5)
    plt.xlabel('False Positive Rate (FPR)')
    plt.ylabel('True Positive Rate (TPR)')
    plt.title('ROC Curve Comparison - Tax Compliance Risk Model')
    plt.legend(loc='lower right')
    plt.tight_layout()
    plt.savefig(os.path.join(images_dir, 'figure1_roc_auc_curve.png'))
    plt.close()
    
    # Plot 2: Cumulative Gains per Decile
    test_results = pd.DataFrame({'y_true': y_test, 'prob': y_pred_automl_prob})
    test_results['decile'] = pd.qcut(test_results['prob'], q=10, labels=False, duplicates='drop')
    test_results['decile'] = 10 - test_results['decile'] # 1 is highest risk
    
    gains = test_results.groupby('decile')['y_true'].sum().reset_index()
    gains['cum_gains'] = gains['y_true'].cumsum()
    gains['cum_gains_pct'] = gains['cum_gains'] / gains['y_true'].sum() * 100
    
    plt.figure(figsize=(7, 5), dpi=300)
    plt.plot(gains['decile'], gains['cum_gains_pct'], marker='o', color='crimson', linewidth=2, label='AutoML Cumulative Gains')
    plt.plot([1, 10], [10, 100], 'k--', alpha=0.5, label='Random Audit Baseline')
    plt.xlabel('Risk Decile (1 = Highest Risk, 10 = Lowest Risk)')
    plt.ylabel('Cumulative % Identified High-Risk Taxpayers')
    plt.title('Cumulative Gains per Risk Decile (Auditing Efficiency)')
    plt.xticks(range(1, 11))
    plt.grid(True, linestyle=':', alpha=0.6)
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(images_dir, 'figure2_cumulative_gains_decile.png'))
    plt.close()
    
    print("Graph plots successfully saved to images/")
    
    results_summary = {
        'auc_lr': round(auc_lr, 4),
        'pr_auc_lr': round(pr_auc_lr, 4),
        'auc_rf': round(auc_rf, 4),
        'pr_auc_rf': round(pr_auc_rf, 4),
        'auc_automl': round(auc_automl, 4),
        'pr_auc_automl': round(pr_auc_automl, 4),
        'f1_automl': round(f1_automl, 4),
        'precision_automl': round(prec_automl, 4),
        'recall_automl': round(rec_automl, 4),
        'top20_decile_gain_pct': round(gains.loc[gains['decile'] <= 2, 'cum_gains_pct'].max(), 1)
    }
    
    return results_summary

if __name__ == "__main__":
    res = run_tax_compliance_automl_pipeline()
    print("\nFINAL SUMMARY RESULTS FOR PAPER:")
    print(json.dumps(res, indent=2))
