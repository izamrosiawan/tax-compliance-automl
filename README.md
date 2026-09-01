# Tax Compliance AutoML: Risk-Based Tax Administration for Digital Economy

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Standard: Canonical 5-Repo](https://img.shields.io/badge/Standard-Canonical--5--Repo-emerald.svg)]()
[![Paper: SINTA 2 / Scopus](https://img.shields.io/badge/Paper-SINTA%202%20%2F%20Scopus-purple.svg)]()

Repositori riset ilmiah dan eksperimen sains data untuk pemodelan pengawasan perpajakan berbasis risiko (*Compliance Risk Management/CRM*) pada sektor ekonomi digital Indonesia. Penelitian ini mengintegrasikan indikator statistik e-commerce Badan Pusat Statistik (BPS) tingkat provinsi dengan parameter transaksi perbankan (*payment gateway*) dan logistik pengiriman melalui kerangka kerja *Automated Machine Learning* (AutoML) dan *Explainable AI* (SHAP).

---

## 📌 Struktur Repositori

```
tax-compliance-automl/
├── paper.md                 # Naskah Lengkap Artikel Ilmiah IMRaD (Target SINTA 2 / Scopus)
├── notebook.ipynb           # Notebook Eksperimen Utama Tereksekusi (EDA, AutoML, SHAP, Evaluasi)
├── data/                    # Dataset BPS E-Commerce & Indikator Fiskal
│   └── bps_e_commerce_tax_compliance.csv
├── images/                  # Koleksi 8 Visualisasi Plot Publikasi 300 DPI
│   ├── figure1_correlation_matrix.png
│   ├── figure2_roc_auc_curve.png
│   ├── figure3_pr_auc_curve.png
│   ├── figure4_cumulative_gains_decile.png
│   ├── figure5_shap_beeswarm.png
│   ├── figure6_shap_importance_bar.png
│   ├── figure7_confusion_matrix.png
│   └── figure8_regional_risk_distribution.png
├── src/                     # Source Code Modular Python (Anti-AI-Slop Standard)
│   ├── generate_data.py     # Generator Dataset BPS E-Commerce (Deterministic seed=42)
│   ├── train_automl.py      # Pipeline AutoML (Optuna Bayesian TPE) & XAI SHAP
│   ├── generate_visuals.py  # Generator Seluruh Visualisasi 300 DPI
│   └── build_notebook.py    # Otomasi Eksekusi Cell Notebook via nbconvert
├── tests/                   # Test Suite (Pytest Unit Tests - Anti-Data Leakage Verified)
│   └── test_pipeline.py
├── requirements.txt         # Dependencies Python Terkunci
└── README.md                # Dokumentasi Komprehensif Repositori
```

---

## 🎯 Ringkasan Temuan Riset & Kinerja Model

Eksperimen dilakukan pada $5.000$ observasi dengan pembagian data uji independen (*holdout test set* 20%, $n=1.000$) dan *stratified 5-fold cross validation*:

| Model | ROC-AUC | PR-AUC | F1-Score | Precision | Recall | Keterangan Arsitektur |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| Logistic Regression | 0,8677 | 0,7362 | 0,6118 | 0,7429 | 0,5200 | Baseline Linier |
| Random Forest | 0,8719 | 0,7061 | 0,5340 | 0,7727 | 0,4080 | Ensemble Pohon ($N=100$) |
| **AutoML (XGBoost TPE)** | **0,8978** | **0,7689** | **0,6637** | **0,7426** | **0,6000** | **Optimal Bayesian AutoML** |

### 📈 Efisiensi Audit Fiskus (Cumulative Decile Lift):
* **Top 10% Desil Risiko (Desil 1):** Menghasilkan faktor pengali efisiensi (*lift*) **3,28x** dibandingkan audit acak konvensional.
* **Top 20% Desil Risiko (Desil 1 & 2):** Menjaring **59,2% dari total seluruh indikasi ketidakpatuhan perpajakan digital**.
* **Mitigasi False Positive:** Membebaskan 80% populasi wajib pajak patuh dari audit pemeriksaan yang tidak perlu (*93,6% True Negative Specificity Rate*).

---

## 📊 Visualisasi Utama Hasil Riset (300 DPI)

### 1. Kurva ROC Komparatif & Kurva Precision-Recall
![Kurva ROC Evaluasi Model](images/figure2_roc_auc_curve.png)
![Kurva Precision-Recall](images/figure3_pr_auc_curve.png)

### 2. Efisiensi Desil Audit & SHAP Explainability (XAI)
![Kurva Keuntungan Kumulatif per Desil](images/figure4_cumulative_gains_decile.png)
![SHAP Beeswarm Summary Plot](images/figure5_shap_beeswarm.png)

---

## 🚀 Cara Menjalankan Eksperimen Secara Reproducible

1. **Clone Repositori:**
   ```bash
   git clone https://github.com/izamrosiawan/tax-compliance-automl.git
   cd tax-compliance-automl
   ```

2. **Install Dependensi:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Generate Dataset & Train Pipeline:**
   ```bash
   python src/generate_data.py
   python src/train_automl.py
   python src/generate_visuals.py
   ```

4. **Jalankan Unit Test:**
   ```bash
   python -m pytest tests/
   ```

---

## 📄 Naskah Publikasi Ilmiah

Naskah lengkap siap submit ke jurnal terakreditasi **SINTA 2** atau **Scopus** tersedia di:
👉 **[`paper.md`](paper.md)**

---

## 👥 Penulis & Afiliasi

* **Izam Rosiawan** (NIM: 103102400049) - Program Studi Sains Data, Fakultas Informatika, Telkom University Surabaya.
* **Sulthan** - Direktorat Kampus Surabaya, Telkom University.

**Lisensi:** [MIT License](LICENSE)
