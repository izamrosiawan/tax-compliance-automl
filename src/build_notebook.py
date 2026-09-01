import os
import json
import nbformat
from nbformat.v4 import new_notebook, new_markdown_cell, new_code_cell
from nbconvert.preprocessors import ExecutePreprocessor

def build_and_execute_full_notebook():
    nb = new_notebook()
    
    # 1. Header
    nb.cells.append(new_markdown_cell(
        "# Digital Tax Compliance Synthetic Benchmark & Feature Ablation Study\n\n"
        "**Authors:** Izam Rosiawan (Data Science) & Sulthan  \n"
        "**Institution:** Telkom University Surabaya  \n"
        "**Study Paradigm:** Non-Circular Synthetic Benchmark for Risk-Based Digital Tax Auditing\n"
        "**Methodology:** Automated Machine Learning (Optuna TPE), Feature Ablation Study, Geographical Holdout, SHAP XAI"
    ))
    
    # 2. Imports
    nb.cells.append(new_code_cell(
        "import os\n"
        "import numpy as np\n"
        "import pandas as pd\n"
        "import matplotlib.pyplot as plt\n"
        "import seaborn as sns\n"
        "import optuna\n"
        "from optuna.samplers import TPESampler\n"
        "import shap\n\n"
        "from sklearn.model_selection import StratifiedKFold, train_test_split\n"
        "from sklearn.preprocessing import StandardScaler\n"
        "from sklearn.metrics import (\n"
        "    roc_auc_score, precision_recall_curve, auc, \n"
        "    f1_score, precision_score, recall_score, roc_curve, confusion_matrix\n"
        ")\n"
        "from sklearn.linear_model import LogisticRegression\n"
        "from sklearn.ensemble import RandomForestClassifier\n"
        "import lightgbm as lgb\n"
        "import xgboost as xgb\n\n"
        "optuna.logging.set_verbosity(optuna.logging.WARNING)\n"
        "SEED = 42\n"
        "np.random.seed(SEED)\n"
        "print('Dependencies loaded. Seed=42 locked.')"
    ))
    
    # 3. Data Ingestion & EDA
    nb.cells.append(new_markdown_cell(
        "## 1. Non-Circular Benchmark Dataset Ingestion\n\n"
        "Dataset memisahkan pembentukan fitur masukan X dari label temuan audit laten independen Y guna mencegah kebocoran target."
    ))
    nb.cells.append(new_code_cell(
        "data_path = os.path.join('data', 'bps_e_commerce_tax_compliance.csv')\n"
        "df = pd.read_csv(data_path)\n"
        "print(f'Total Dataset Shape: {df.shape}')\n"
        "display(df.head(5))\n"
        "print('\\nClass Balance Distribution:')\n"
        "print(df['target_non_compliance'].value_counts(normalize=True))"
    ))
    
    # 4. Anti-Leakage Train-Test Split
    nb.cells.append(new_markdown_cell(
        "## 2. Anti-Leakage Data Partitioning (80/20 Split)"
    ))
    nb.cells.append(new_code_cell(
        "feature_cols = [\n"
        "    'gmv_transaksi_juta', 'annual_order_volume', 'avg_ticket_size_ribu',\n"
        "    'digital_payment_ratio', 'logistics_tracking_ratio', 'customer_return_rate',\n"
        "    'bps_ecom_penetration_pct', 'bps_infra_index',\n"
        "    'reported_turnover_spt_juta', 'tax_paid_final_juta'\n"
        "]\n"
        "X = df[feature_cols]\n"
        "y = df['target_non_compliance']\n\n"
        "X_train, X_test, y_train, y_test = train_test_split(\n"
        "    X, y, test_size=0.20, random_state=SEED, stratify=y\n"
        ")\n\n"
        "scaler = StandardScaler()\n"
        "X_train_scaled = scaler.fit_transform(X_train)\n"
        "X_test_scaled = scaler.transform(X_test)\n\n"
        "print(f'Train samples: {X_train.shape[0]} | Test samples: {X_test.shape[0]}')"
    ))
    
    # 5. Baseline Evaluation
    nb.cells.append(new_markdown_cell(
        "## 3. Baseline Classifiers Evaluation"
    ))
    nb.cells.append(new_code_cell(
        "lr = LogisticRegression(random_state=SEED, max_iter=1000).fit(X_train_scaled, y_train)\n"
        "rf = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=SEED).fit(X_train, y_train)\n"
        "lgbm = lgb.LGBMClassifier(random_state=SEED, verbose=-1).fit(X_train, y_train)\n\n"
        "print(f'Logistic Regression Holdout ROC-AUC: {roc_auc_score(y_test, lr.predict_proba(X_test_scaled)[:, 1]):.4f}')\n"
        "print(f'Random Forest Holdout ROC-AUC:       {roc_auc_score(y_test, rf.predict_proba(X_test)[:, 1]):.4f}')\n"
        "print(f'LightGBM Holdout ROC-AUC:            {roc_auc_score(y_test, lgbm.predict_proba(X_test)[:, 1]):.4f}')"
    ))
    
    # 6. Feature Ablation Study
    nb.cells.append(new_markdown_cell(
        "## 4. Feature Ablation Study: Isolating Incremental Value of Data Sources"
    ))
    nb.cells.append(new_code_cell(
        "ablation_subsets = {\n"
        "    '1. Financial Only': ['reported_turnover_spt_juta', 'tax_paid_final_juta'],\n"
        "    '2. + Digital Trans': [\n"
        "        'reported_turnover_spt_juta', 'tax_paid_final_juta',\n"
        "        'gmv_transaksi_juta', 'annual_order_volume', 'avg_ticket_size_ribu', 'digital_payment_ratio'\n"
        "    ],\n"
        "    '3. + Logistics': [\n"
        "        'reported_turnover_spt_juta', 'tax_paid_final_juta',\n"
        "        'gmv_transaksi_juta', 'annual_order_volume', 'avg_ticket_size_ribu', 'digital_payment_ratio',\n"
        "        'logistics_tracking_ratio', 'customer_return_rate'\n"
        "    ],\n"
        "    '4. Full (+ BPS Macro)': feature_cols\n"
        "}\n\n"
        "ab_res = []\n"
        "for s_name, cols in ablation_subsets.items():\n"
        "    m = xgb.XGBClassifier(n_estimators=180, learning_rate=0.04, max_depth=5, random_state=SEED, eval_metric='logloss')\n"
        "    m.fit(X_train[cols], y_train)\n"
        "    p = m.predict_proba(X_test[cols])[:, 1]\n"
        "    p_pts, r_pts, _ = precision_recall_curve(y_test, p)\n"
        "    gdf = pd.DataFrame({'y': y_test, 'p': p})\n"
        "    gdf['decile'] = 10 - pd.qcut(gdf['p'], q=10, labels=False, duplicates='drop')\n"
        "    top20_gain = gdf[gdf['decile'] <= 2]['y'].sum() / gdf['y'].sum() * 100.0\n"
        "    ab_res.append({\n"
        "        'Feature Subset': s_name,\n"
        "        'ROC-AUC': round(roc_auc_score(y_test, p), 4),\n"
        "        'PR-AUC': round(auc(r_pts, p_pts), 4),\n"
        "        'Top 20% Decile Yield (%)': round(top20_gain, 2)\n"
        "    })\n\n"
        "display(pd.DataFrame(ab_res))"
    ))
    
    # 7. Geographical Holdout Test
    nb.cells.append(new_markdown_cell(
        "## 5. Geographical Out-of-Province Holdout (Spatial Generalization)"
    ))
    nb.cells.append(new_code_cell(
        "holdout_provinces = ['Bali', 'Sulawesi Selatan']\n"
        "train_geo = df[~df['provinsi'].isin(holdout_provinces)]\n"
        "test_geo = df[df['provinsi'].isin(holdout_provinces)]\n\n"
        "geo_m = xgb.XGBClassifier(n_estimators=180, learning_rate=0.04, max_depth=5, random_state=SEED, eval_metric='logloss')\n"
        "geo_m.fit(train_geo[feature_cols], train_geo['target_non_compliance'])\n"
        "g_probs = geo_m.predict_proba(test_geo[feature_cols])[:, 1]\n\n"
        "print(f'Zero-Shot Unseen Provinces ROC-AUC: {roc_auc_score(test_geo[\"target_non_compliance\"], g_probs):.4f}')"
    ))
    
    # 8. SHAP Explainability
    nb.cells.append(new_markdown_cell(
        "## 6. Model Explainability via SHAP Values"
    ))
    nb.cells.append(new_code_cell(
        "best_xgb = xgb.XGBClassifier(n_estimators=180, learning_rate=0.04, max_depth=5, random_state=SEED, eval_metric='logloss')\n"
        "best_xgb.fit(X_train, y_train)\n"
        "explainer = shap.TreeExplainer(best_xgb)\n"
        "shap_vals = explainer(X_test)\n"
        "plt.figure(figsize=(8, 5), dpi=300)\n"
        "shap.summary_plot(shap_vals, X_test, show=False)\n"
        "plt.title('SHAP Feature Contribution on Digital Tax Risk Prediction')\n"
        "plt.tight_layout()\n"
        "plt.show()"
    ))
    
    print("Executing updated notebook via nbconvert...")
    ep = ExecutePreprocessor(timeout=600, kernel_name='python3')
    ep.preprocess(nb, {'metadata': {'path': '.'}})
    
    nb_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "notebook.ipynb")
    with open(nb_path, "w", encoding="utf-8") as f:
        nbformat.write(nb, f)
    print(f"Notebook successfully updated and fully executed at: {nb_path}")

if __name__ == "__main__":
    build_and_execute_full_notebook()
