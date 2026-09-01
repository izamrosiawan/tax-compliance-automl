import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import shap

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (
    roc_curve, precision_recall_curve, auc, 
    confusion_matrix, roc_auc_score
)
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
import xgboost as xgb
import lightgbm as lgb

SEED = 42
np.random.seed(SEED)

def generate_all_publication_visuals():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_path = os.path.join(base_dir, "data", "bps_e_commerce_tax_compliance.csv")
    images_dir = os.path.join(base_dir, "images")
    os.makedirs(images_dir, exist_ok=True)
    
    df = pd.read_csv(data_path)
    X = df.drop(columns=["provinsi", "target_compliance_risk"])
    y = df["target_compliance_risk"]
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=SEED, stratify=y
    )
    
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Train Best Models
    lr = LogisticRegression(random_state=SEED, max_iter=1000).fit(X_train_scaled, y_train)
    rf = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=SEED).fit(X_train, y_train)
    
    best_xgb = xgb.XGBClassifier(
        n_estimators=180, learning_rate=0.04, max_depth=5,
        subsample=0.85, colsample_bytree=0.85, random_state=SEED, eval_metric="logloss"
    ).fit(X_train, y_train)
    
    lr_probs = lr.predict_proba(X_test_scaled)[:, 1]
    rf_probs = rf.predict_proba(X_test)[:, 1]
    xgb_probs = best_xgb.predict_proba(X_test)[:, 1]
    xgb_preds = best_xgb.predict(X_test)
    
    # Visual 1: Correlation Heatmap (EDA)
    plt.figure(figsize=(9, 7), dpi=300)
    corr = X.corr()
    mask = np.triu(np.ones_like(corr, dtype=bool))
    sns.heatmap(corr, mask=mask, annot=True, fmt=".2f", cmap="mako", vmin=-1, vmax=1, square=True, linewidths=.5)
    plt.title("Matriks Korelasi Multivariat Fitur BPS & Fiskal (EDA)", fontsize=12, pad=12)
    plt.tight_layout()
    plt.savefig(os.path.join(images_dir, "figure1_correlation_matrix.png"))
    plt.close()
    
    # Visual 2: Comparative ROC Curves
    plt.figure(figsize=(7.5, 5.5), dpi=300)
    fpr_lr, tpr_lr, _ = roc_curve(y_test, lr_probs)
    fpr_rf, tpr_rf, _ = roc_curve(y_test, rf_probs)
    fpr_xgb, tpr_xgb, _ = roc_curve(y_test, xgb_probs)
    
    plt.plot(fpr_lr, tpr_lr, label=f"Logistic Regression (AUC = {roc_auc_score(y_test, lr_probs):.4f})", linestyle="--")
    plt.plot(fpr_rf, tpr_rf, label=f"Random Forest (AUC = {roc_auc_score(y_test, rf_probs):.4f})", linestyle="-.")
    plt.plot(fpr_xgb, tpr_xgb, label=f"AutoML XGBoost (AUC = {roc_auc_score(y_test, xgb_probs):.4f})", color="#1e3a8a", linewidth=2.5)
    plt.plot([0, 1], [0, 1], "k--", alpha=0.4)
    plt.xlabel("False Positive Rate (1 - Specificity)", fontsize=10)
    plt.ylabel("True Positive Rate (Sensitivity / Recall)", fontsize=10)
    plt.title("Kurva ROC Komparatif Model Klasifikasi Risiko Kepatuhan Pajak", fontsize=11, pad=10)
    plt.grid(True, linestyle=":", alpha=0.6)
    plt.legend(loc="lower right", frameon=True)
    plt.tight_layout()
    plt.savefig(os.path.join(images_dir, "figure2_roc_auc_curve.png"))
    plt.close()
    
    # Visual 3: Precision-Recall Curve Comparison
    plt.figure(figsize=(7.5, 5.5), dpi=300)
    p_lr, r_lr, _ = precision_recall_curve(y_test, lr_probs)
    p_rf, r_rf, _ = precision_recall_curve(y_test, rf_probs)
    p_xgb, r_xgb, _ = precision_recall_curve(y_test, xgb_probs)
    
    plt.plot(r_lr, p_lr, label=f"Logistic Regression (PR-AUC = {auc(r_lr, p_lr):.4f})", linestyle="--")
    plt.plot(r_rf, p_rf, label=f"Random Forest (PR-AUC = {auc(r_rf, p_rf):.4f})", linestyle="-.")
    plt.plot(r_xgb, p_xgb, label=f"AutoML XGBoost (PR-AUC = {auc(r_xgb, p_xgb):.4f})", color="#047857", linewidth=2.5)
    plt.xlabel("Recall", fontsize=10)
    plt.ylabel("Precision", fontsize=10)
    plt.title("Kurva Precision-Recall (PR-AUC) pada Kasus Ketidakseimbangan Risiko", fontsize=11, pad=10)
    plt.grid(True, linestyle=":", alpha=0.6)
    plt.legend(loc="lower left", frameon=True)
    plt.tight_layout()
    plt.savefig(os.path.join(images_dir, "figure3_pr_auc_curve.png"))
    plt.close()
    
    # Visual 4: Cumulative Decile Lift (Auditing Efficiency)
    gains_df = pd.DataFrame({"y_true": y_test, "prob": xgb_probs})
    gains_df["decile"] = pd.qcut(gains_df["prob"], q=10, labels=False, duplicates="drop")
    gains_df["decile"] = 10 - gains_df["decile"]
    
    decile_summary = gains_df.groupby("decile")["y_true"].sum().reset_index()
    decile_summary["cum_gains"] = decile_summary["y_true"].cumsum()
    decile_summary["cum_gains_pct"] = decile_summary["cum_gains"] / decile_summary["y_true"].sum() * 100.0
    
    plt.figure(figsize=(7.5, 5.5), dpi=300)
    plt.plot(decile_summary["decile"], decile_summary["cum_gains_pct"], marker="o", color="#b91c1c", linewidth=2.5, label="AutoML XGBoost Model Gains")
    plt.plot([1, 10], [10, 100], "k--", alpha=0.5, label="Random Audit Baseline (Tanpa Model)")
    plt.axvline(x=2, color="#4b5563", linestyle=":", label="Ambang Batas Top 20% Desil Audit")
    plt.xlabel("Desil Risiko (Desil 1 = Risiko Tertinggi, Desil 10 = Risiko Terendah)", fontsize=10)
    plt.ylabel("Persentase Kumulatif Wajib Pajak Tidak Patuh Terjaring (%)", fontsize=10)
    plt.title("Kurva Keuntungan Kumulatif per Desil (Efisiensi Audit Fiskus)", fontsize=11, pad=10)
    plt.xticks(range(1, 11))
    plt.grid(True, linestyle=":", alpha=0.6)
    plt.legend(loc="lower right", frameon=True)
    plt.tight_layout()
    plt.savefig(os.path.join(images_dir, "figure4_cumulative_gains_decile.png"))
    plt.close()
    
    # Visual 5: SHAP Beeswarm Summary Plot (Explainable AI)
    explainer = shap.TreeExplainer(best_xgb)
    shap_values = explainer(X_test)
    plt.figure(figsize=(8.5, 5.5), dpi=300)
    shap.summary_plot(shap_values, X_test, show=False)
    plt.title("SHAP Beeswarm Plot: Kontribusi Fitur BPS & Transaksi terhadap Skor Risiko", fontsize=11, pad=12)
    plt.tight_layout()
    plt.savefig(os.path.join(images_dir, "figure5_shap_beeswarm.png"))
    plt.close()
    
    # Visual 6: SHAP Feature Importance Bar Chart
    plt.figure(figsize=(8.5, 5), dpi=300)
    shap.plots.bar(shap_values, show=False)
    plt.title("Mean Absolute SHAP Value: Peringkat Kepentingan Fitur Global", fontsize=11, pad=12)
    plt.tight_layout()
    plt.savefig(os.path.join(images_dir, "figure6_shap_importance_bar.png"))
    plt.close()
    
    # Visual 7: Normalized Confusion Matrix
    cm = confusion_matrix(y_test, xgb_preds, normalize="true")
    plt.figure(figsize=(6, 5), dpi=300)
    sns.heatmap(cm, annot=True, fmt=".2%", cmap="Blues", cbar=False,
                xticklabels=["Patuh (0)", "Berisiko (1)"],
                yticklabels=["Patuh (0)", "Berisiko (1)"])
    plt.xlabel("Prediksi Model AutoML", fontsize=10)
    plt.ylabel("Status Kepatuhan Aktual", fontsize=10)
    plt.title("Normalized Confusion Matrix (Evaluasi Kesalahan Klasifikasi)", fontsize=11, pad=10)
    plt.tight_layout()
    plt.savefig(os.path.join(images_dir, "figure7_confusion_matrix.png"))
    plt.close()
    
    # Visual 8: Regional Risk Distribution (Provinsi Analysis)
    df_test = df.iloc[X_test.index].copy()
    df_test["predicted_risk"] = xgb_preds
    prov_risk = df_test.groupby("provinsi")["predicted_risk"].mean().reset_index()
    prov_risk = prov_risk.sort_values(by="predicted_risk", ascending=False)
    
    plt.figure(figsize=(9, 5), dpi=300)
    sns.barplot(data=prov_risk, x="predicted_risk", y="provinsi", palette="viridis")
    plt.xlabel("Proporsi Wajib Pajak Berisiko Tinggi Terdeteksi", fontsize=10)
    plt.ylabel("Provinsi", fontsize=10)
    plt.title("Distribusi Tingkat Risiko Kepatuhan Pajak Digital Lintas Provinsi", fontsize=11, pad=10)
    plt.tight_layout()
    plt.savefig(os.path.join(images_dir, "figure8_regional_risk_distribution.png"))
    plt.close()
    
    print("All 8 high-resolution (300 DPI) publication figures successfully generated in images/")

if __name__ == "__main__":
    generate_all_publication_visuals()
