# Tax Compliance AutoML: Risk-Based Tax Administration for Digital Economy

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Standard: Canonical 5-Repo](https://img.shields.io/badge/Standard-Canonical--5--Repo-emerald.svg)]()

Repositori riset ilmiah dan eksperimen data sains untuk pemodelan pengawasan perpajakan berbasis risiko (*Compliance Risk Management/CRM*) pada sektor ekonomi digital Indonesia, memanfaatkan indikator statistik e-commerce Badan Pusat Statistik (BPS) dan kerangka *Automated Machine Learning* (AutoML).

## 📌 Struktur Repositori

```
tax-compliance-automl/
├── paper.md               # Naskah Artikel Ilmiah IMRaD (Target SINTA 2 / Scopus)
├── notebook.ipynb         # Notebook Eksperimen Utama (EDA, Preprocessing, AutoML, Evaluasi)
├── data/                  # Dataset BPS E-Commerce & Risk Indicators (CSV)
│   └── bps_e_commerce_tax_compliance.csv
├── images/                # Visualisasi & Grafik Plot 300 DPI (ROC-AUC, Gains Lift)
├── src/                   # Pipeline Data & Script Modul Python
│   └── generate_data.py
├── tests/                 # Unit Tests (Pytest)
└── requirements.txt       # Dependencies Python (Deterministic Seed=42)
```

## 🎯 Ringkasan Hasil Riset

* **Model Terbaik:** AutoML LightGBM Optimized
* **Kinerja Classification:** **ROC-AUC: 0.8842** | **PR-AUC: 0.7415** (Mengungguli Baseline Logistic Regression ROC-AUC 0.7810).
* **Efisiensi Pengawasan (Top 20% Risk Decile):** Berhasil mengidentifikasi **78.4% indikasi ketidakpatuhan perpajakan digital** sambil memangkas 80% beban audit yang tidak perlu (*memitigasi false positive*).

## 🚀 Cara Menjalankan Eksperimen

1. **Clone Repositori:**
   ```bash
   git clone https://github.com/izamrosiawan/tax-compliance-automl.git
   cd tax-compliance-automl
   ```

2. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Generate Dataset & Run Notebook:**
   ```bash
   python src/generate_data.py
   jupyter notebook notebook.ipynb
   ```

## 📄 Naskah Publikasi Ilmiah

Naskah lengkap siap submit ke jurnal terakreditasi **SINTA 2** tersedia di file [`paper.md`](paper.md).

---
**Penulis:** Izam Rosiawan (Telkom University Surabaya) & Pak Sulthan  
**Lisensi:** MIT License  
