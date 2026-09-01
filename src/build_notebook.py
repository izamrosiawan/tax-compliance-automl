import os
import json
import nbformat
from nbformat.v4 import new_notebook, new_markdown_cell, new_code_cell
from nbconvert.preprocessors import ExecutePreprocessor

def build_and_execute_full_notebook():
    nb = new_notebook()
    
    # 1. Header
    nb.cells.append(new_markdown_cell(
        "# Tax Compliance AutoML: Risk-Based Auditing on Digital Economy\n\n"
        "**Authors:** Izam Rosiawan (Data Science) & Sulthan  \n"
        "**Institution:** Telkom University Surabaya  \n"
        "**Focus:** Indonesian BPS Digital Economy Indicators & Compliance Risk Management (CRM)\n"
        "**Methodology:** Automated Machine Learning (Optuna TPE), Anti-Leakage Protocol (`seed=42`), SHAP Explainability"
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
        "    f1_score, precision_score, recall_score, roc_curve, confusion_matrix, classification_report\n"
        ")\n"
        "from sklearn.linear_model import LogisticRegression\n"
        "from sklearn.ensemble import RandomForestClassifier\n"
        "import lightgbm as lgb\n"
        "import xgboost as xgb\n\n"
        "optuna.logging.set_verbosity(optuna.logging.WARNING)\n"
        "SEED = 42\n"
        "np.random.seed(SEED)\n"
        "print('Dependencies loaded successfully. Deterministic SEED=42 set.')"
    ))
    
    # 3. Data Ingestion & EDA
    nb.cells.append(new_markdown_cell(
        "## 1. Exploratory Data Analysis & BPS Regional Indicator Ingestion\n\n"
        "Dataset menggabungkan indikator makroekonomi BPS (Statistik E-Commerce) dengan parameter mikro transaksi fiskal."
    ))
    nb.cells.append(new_code_cell(
        "data_path = os.path.join('data', 'bps_e_commerce_tax_compliance.csv')\n"
        "df = pd.read_csv(data_path)\n"
        "print(f'Total Dataset Shape: {df.shape}')\n"
        "display(df.head(5))\n"
        "print('\\nSummary Statistics:')\n"
        "display(df.describe().T[['mean', 'std', 'min', '50%', 'max']])\n"
        "print('\\nClass Balance:')\n"
        "print(df['target_compliance_risk'].value_counts(normalize=True))"
    ))
    
    # 4. Anti-Leakage Train-Test Split
    nb.cells.append(new_markdown_cell(
        "## 2. Anti-Leakage Data Partitioning & Preprocessing\n\n"
        "Pemisahan data latih (80%) dan data uji independen (20%) dilakukan sebelum fitting transformer untuk mencegah *data leakage*."
    ))
    nb.cells.append(new_code_cell(
        "X = df.drop(columns=['provinsi', 'target_compliance_risk'])\n"
        "y = df['target_compliance_risk']\n\n"
        "X_train, X_test, y_train, y_test = train_test_split(\n"
        "    X, y, test_size=0.20, random_state=SEED, stratify=y\n"
        ")\n\n"
        "scaler = StandardScaler()\n"
        "X_train_scaled = scaler.fit_transform(X_train)\n"
        "X_test_scaled = scaler.transform(X_test)\n\n"
        "print(f'Training Set: {X_train.shape[0]} observations')\n"
        "print(f'Holdout Test Set: {X_test.shape[0]} observations')"
    ))
    
    # 5. Baseline Evaluation
    nb.cells.append(new_markdown_cell(
        "## 3. Baseline Models: Logistic Regression & Random Forest"
    ))
    nb.cells.append(new_code_cell(
        "# Logistic Regression Baseline\n"
        "lr = LogisticRegression(random_state=SEED, max_iter=1000)\n"
        "lr.fit(X_train_scaled, y_train)\n"
        "lr_probs = lr.predict_proba(X_test_scaled)[:, 1]\n"
        "lr_preds = lr.predict(X_test_scaled)\n\n"
        "# Random Forest Model\n"
        "rf = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=SEED)\n"
        "rf.fit(X_train, y_train)\n"
        "rf_probs = rf.predict_proba(X_test)[:, 1]\n"
        "rf_preds = rf.predict(X_test)\n\n"
        "print(f'Logistic Regression Test ROC-AUC: {roc_auc_score(y_test, lr_probs):.4f}')\n"
        "print(f'Random Forest Test ROC-AUC:       {roc_auc_score(y_test, rf_probs):.4f}')"
    ))
    
    # 6. AutoML Bayesian Optimization
    nb.cells.append(new_markdown_cell(
        "## 4. AutoML Model Search & Bayesian Hyperparameter Optimization (Optuna TPE)"
    ))
    nb.cells.append(new_code_cell(
        "cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=SEED)\n\n"
        "def objective(trial):\n"
        "    classifier_name = trial.suggest_categorical('classifier', ['LightGBM', 'XGBoost'])\n"
        "    if classifier_name == 'LightGBM':\n"
        "        params = {\n"
        "            'n_estimators': trial.suggest_int('lgb_n_estimators', 50, 250),\n"
        "            'learning_rate': trial.suggest_float('lgb_lr', 0.01, 0.2, log=True),\n"
        "            'num_leaves': trial.suggest_int('lgb_num_leaves', 15, 127),\n"
        "            'max_depth': trial.suggest_int('lgb_max_depth', 3, 10),\n"
        "            'subsample': trial.suggest_float('lgb_subsample', 0.6, 1.0),\n"
        "            'colsample_bytree': trial.suggest_float('lgb_colsample', 0.6, 1.0),\n"
        "            'random_state': SEED,\n"
        "            'verbose': -1\n"
        "        }\n"
        "        model = lgb.LGBMClassifier(**params)\n"
        "    else:\n"
        "        params = {\n"
        "            'n_estimators': trial.suggest_int('xgb_n_estimators', 50, 250),\n"
        "            'learning_rate': trial.suggest_float('xgb_lr', 0.01, 0.2, log=True),\n"
        "            'max_depth': trial.suggest_int('xgb_max_depth', 3, 10),\n"
        "            'subsample': trial.suggest_float('xgb_subsample', 0.6, 1.0),\n"
        "            'colsample_bytree': trial.suggest_float('xgb_colsample', 0.6, 1.0),\n"
        "            'random_state': SEED,\n"
        "            'eval_metric': 'logloss'\n"
        "        }\n"
        "        model = xgb.XGBClassifier(**params)\n"
        "        \n"
        "    scores = []\n"
        "    for train_idx, val_idx in cv.split(X_train, y_train):\n"
        "        X_tr, X_val = X_train.iloc[train_idx], X_train.iloc[val_idx]\n"
        "        y_tr, y_val = y_train.iloc[train_idx], y_train.iloc[val_idx]\n"
        "        model.fit(X_tr, y_tr)\n"
        "        scores.append(roc_auc_score(y_val, model.predict_proba(X_val)[:, 1]))\n"
        "    return np.mean(scores)\n\n"
        "study = optuna.create_study(direction='maximize', sampler=TPESampler(seed=SEED))\n"
        "study.optimize(objective, n_trials=30)\n\n"
        "best_p = study.best_params\n"
        "print('Optimal Hyperparameters Selected by AutoML:', best_p)\n\n"
        "if best_p['classifier'] == 'LightGBM':\n"
        "    best_automl_model = lgb.LGBMClassifier(\n"
        "        n_estimators=best_p['lgb_n_estimators'],\n"
        "        learning_rate=best_p['lgb_lr'],\n"
        "        num_leaves=best_p['lgb_num_leaves'],\n"
        "        max_depth=best_p['lgb_max_depth'],\n"
        "        subsample=best_p['lgb_subsample'],\n"
        "        colsample_bytree=best_p['lgb_colsample'],\n"
        "        random_state=SEED,\n"
        "        verbose=-1\n"
        "    )\n"
        "else:\n"
        "    best_automl_model = xgb.XGBClassifier(\n"
        "        n_estimators=best_p['xgb_n_estimators'],\n"
        "        learning_rate=best_p['xgb_lr'],\n"
        "        max_depth=best_p['xgb_max_depth'],\n"
        "        subsample=best_p['xgb_subsample'],\n"
        "        colsample_bytree=best_p['xgb_colsample'],\n"
        "        random_state=SEED,\n"
        "        eval_metric='logloss'\n"
        "    )\n\n"
        "best_automl_model.fit(X_train, y_train)\n"
        "automl_probs = best_automl_model.predict_proba(X_test)[:, 1]\n"
        "automl_preds = best_automl_model.predict(X_test)\n"
        "print(f'AutoML Best Test ROC-AUC: {roc_auc_score(y_test, automl_probs):.4f}')"
    ))
    
    # 7. SHAP Explainability & Visualizations
    nb.cells.append(new_markdown_cell(
        "## 5. Model Explainability (SHAP Values) & Decile Audit Efficiency Analysis"
    ))
    nb.cells.append(new_code_cell(
        "# SHAP Summary Plot\n"
        "explainer = shap.TreeExplainer(best_automl_model)\n"
        "shap_values = explainer(X_test)\n"
        "plt.figure(figsize=(8, 5), dpi=300)\n"
        "shap.summary_plot(shap_values, X_test, show=False)\n"
        "plt.title('SHAP Feature Importance: Explaining Tax Compliance Risk Factors')\n"
        "plt.tight_layout()\n"
        "plt.show()\n\n"
        "# Cumulative Decile Lift\n"
        "gains_df = pd.DataFrame({'y_true': y_test, 'prob': automl_probs})\n"
        "gains_df['decile'] = pd.qcut(gains_df['prob'], q=10, labels=False, duplicates='drop')\n"
        "gains_df['decile'] = 10 - gains_df['decile']\n\n"
        "decile_summary = gains_df.groupby('decile')['y_true'].sum().reset_index()\n"
        "decile_summary['cum_gains'] = decile_summary['y_true'].cumsum()\n"
        "decile_summary['cum_gains_pct'] = decile_summary['cum_gains'] / decile_summary['y_true'].sum() * 100.0\n\n"
        "display(decile_summary)\n"
        "print(f'Top 20% Risk Deciles capture {decile_summary.loc[decile_summary[\"decile\"] <= 2, \"cum_gains_pct\"].max():.2f}% of all high-risk taxpayers.')"
    ))
    
    print("Executing complete notebook cells via nbconvert...")
    ep = ExecutePreprocessor(timeout=600, kernel_name='python3')
    ep.preprocess(nb, {'metadata': {'path': '.'}})
    
    nb_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "notebook.ipynb")
    with open(nb_path, "w", encoding="utf-8") as f:
        nbformat.write(nb, f)
    print(f"Notebook successfully written and fully executed with live outputs at: {nb_path}")

if __name__ == "__main__":
    build_and_execute_full_notebook()
