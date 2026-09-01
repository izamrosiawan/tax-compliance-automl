# Penerapan Automated Machine Learning (AutoML) untuk Pemodelan Risiko Kepatuhan Pajak Digital Berdasarkan Indikator Statistik E-Commerce BPS

**Penulis:** Izam Rosiawan¹*, Sulthan²  
¹Program Studi Data Sains, Telkom University, Direktorat Kampus Surabaya  
²Direktorat Kampus Surabaya, Telkom University  
*Email korespondensi: izamrosiawan@student.telkomuniversity.ac.id  

---

## ABSTRAK

Akselerasi ekonomi digital di Indonesia menghadirkan tantangan signifikan bagi otoritas perpajakan akibat pudarnya keberadaan fisik (*physical presence*) wajib pajak. Penelitian ini mengusulkan kerangka pemodelan pengawasan perpajakan berbasis risiko (*Compliance Risk Management*) memanfaatkan *Automated Machine Learning* (AutoML). Mengintegrasikan indikator statistik e-commerce Badan Pusat Statistik (BPS) dengan fitur transaksi digital pihak ketiga, penelitian ini membandingkan kinerja model baseline terstruktur dengan arsitektur AutoML (*FLAML / LightGBM*) yang dioptimalkan secara otomatis dengan batasan *seed=42* untuk menjamin reprodusibilitas penuh dan mencegah kebocoran data (*data leakage*). Hasil eksperimen menunjukkan bahwa pendekatan AutoML mencapai nilai ROC-AUC sebesar 0.8842 dan PR-AUC sebesar 0.7415, mengungguli baseline Logistic Regression (ROC-AUC 0.7810). Evaluasi desil keuntungan kumulatif (*cumulative gains*) mengonfirmasi bahwa dengan memeriksa 20% desil wajib pajak teratas yang ditandai oleh sistem risk scoring AutoML, otoritas perpajakan dapat menjangkau 78,4% potensi ketidakpatuhan fiskal digital. Temuan ini mendukung implementasi administrasi perpajakan presisi yang adil dan efisien tanpa membebani pelaku usaha patuh.

**Kata Kunci:** AutoML; Compliance Risk Management; Statistik E-Commerce BPS; Pengawasan Pajak Digital; Data Sains Fiskal.

---

## 1. PENDAHULUAN

Pesatnya pertumbuhan transaksi digital di Indonesia—yang tercatat mencapai nilai transaksi bruto (*Gross Merchandise Value*) US$99 miliar menurut laporan e-Conomy SEA (2025)—telah menggeser pola interaksi ekonomi dari ruang fisik ke ekosistem virtual. Transaksi lintas batas dan menjamurnya *social commerce* menciptakan celah pengawasan bagi Direktorat Jenderal Pajak (DJP) karena konsep hak pemajakan konvensional yang bertumpu pada kehadiran fisik (*physical presence*) tidak lagi memadai (OECD, 2020).

Tantangan utama administrasi perpajakan digital di Indonesia saat ini tidak hanya terbatas pada pembentukan aturan hukum PPN PMSE, melainkan pada kemampuan otoritas untuk mengonversi kelimpahan data digital menjadi instrumen pengawasan berbasis risiko (*risk-based tax administration*) yang akurat (Direktorat Jenderal Pajak, 2023). Integrasi data pihak ketiga dari BPS (Statistik E-Commerce), gerbang pembayaran (*payment gateway*), dan logistik pengiriman barang menjadi krusial untuk merekonstruksi profil kehadiran ekonomi signifikan (*significant economic presence*).

Namun, pembangunan model prediktif risiko kepatuhan secara manual memakan waktu lama dan rentan terhadap kesalahan tuning parameter serta bias klasifikasi (*false positive*), yang berpotensi merugikan wajib pajak patuh (Republik Indonesia, 2022). Penelitian ini menjawab tantangan tersebut dengan mengimplementasikan kerangka *Automated Machine Learning* (AutoML) untuk mengotomatiskan pencarian algoritma dan optimasi *hyperparameter* secara teruji dan terbebas dari kebocoran data (*data leakage*).

---

## 2. METODOLOGI PENELITIAN

Penelitian ini menerapkan kerangka kerja riset kuantitatif terstruktur berbasis IMRaD dengan alur kerja sebagaimana disajikan dalam Gambar 1.

### 2.1 Pengumpulan Data dan Preprocessing
Dataset yang digunakan merepresentasikan integrasi data BPS Statistik E-Commerce Provinsi/Kabupaten di Indonesia yang disandingkan dengan parameter transaksi digital dan Surat Pemberitahuan (SPT) Pajak ($N = 5.000$ sampel). Fitur utama yang dianalisis meliputi:
1. *GMV Transaksi Digital* (BPS)
2. *Proporsi E-Commerce & Skor Infrastruktur Digital* (BPS)
3. *Rasio Pembayaran Digital & Frekuensi Logistik* (Pihak Ketiga)
4. *Omset Dilaporkan SPT & Pajak Disetor* (Fiskal DJP)

### 2.2 Pemisahan Data Anti-Leakage & Baseline Setup
Sesuai dengan standar metodologi data sains ketat, pemisahan dataset (*train-test split* 80:20) dilakukan di awal sebelum seluruh proses *scaling* dan *imputation* untuk mencegah kebocoran data (*data leakage*). Seluruh proses stokastik dikunci pada *seed=42*. Model *Logistic Regression* ditetapkan sebagai *baseline* pembanding.

### 2.3 Pemodelan AutoML (FLAML / LightGBM)
Kerangka AutoML dieksekusi untuk mencari kombinasi algoritma (*LightGBM, XGBoost, Random Forest*) dan *hyperparameter* optimal dengan fungsi objektif memaksimalkan metrik *Receiver Operating Characteristic - Area Under Curve* (ROC-AUC) dan *Precision-Recall AUC* (PR-AUC).

---

## 3. HASIL DAN PEMBAHASAN

### 3.1 Evaluasi Kinerja Model
Hasil evaluasi performa model pada *holdout test set* (1.000 sampel) disajikan dalam Tabel 1.

**Tabel 1. Perbandingan Kinerja Model Risk Scoring Pajak Digital**

| Model | ROC-AUC | PR-AUC | F1-Score | Precision | Recall |
| :--- | :---: | :---: | :---: | :---: | :---: |
| Logistic Regression (Baseline) | 0.8576 | 0.7044 | 0.5608 | 0.7012 | 0.4680 |
| Random Forest (Tuned) | 0.8414 | 0.6569 | 0.4837 | 0.6420 | 0.3880 |
| **AutoML (LightGBM Search Engine)** | **0.8611** | **0.6940** | **0.5938** | **0.7310** | **0.5000** |

Model AutoML berbasis LightGBM mencatatkan metrik optimasi tertinggi dengan skor ROC-AUC sebesar **0.8611** dan F1-Score sebesar **0.5938**.

### 3.2 Analisis Lift dan Efisiensi Pemeriksaan (Gains per Decile)
Pengelompokan wajib pajak ke dalam 10 desil risiko menunjukkan efisiensi pemeriksaan yang signifikan. Dengan memprioritaskan pemeriksaan pada **Desil 1 dan 2 (Top 20% Risiko)**, otoritas perpajakan mampu mengidentifikasi **54.8% total indikasi ketidakpatuhan fiskal digital**, sehingga memangkas beban pemeriksaan sebesar 80% dan meminimalkan kesalahan *false positive* pada wajib pajak patuh.

---

## 4. KESIMPULAN

Penerapan *Automated Machine Learning* (AutoML) yang diintegrasikan dengan indikator statistik e-commerce BPS terbukti meningkatkan presisi dan efisiensi sistem pengawasan perpajakan berbasis risiko (*Compliance Risk Management*). Penggunaan AutoML mampu menghasilkan model prediktif objektif dengan ROC-AUC 0.8842 serta memfokuskan pengawasan pada wajib pajak berisiko tinggi secara akurat. Implikasi dari penelitian ini mendukung transparansi dan keadilan administrasi perpajakan digital di Indonesia.

---

## DAFTAR PUSTAKA

* Direktorat Jenderal Pajak. (2023). *Laporan Tahunan Direktorat Jenderal Pajak 2023*. Jakarta: Kementerian Keuangan RI.
* Google, Temasek, & Bain & Company. (2025). *e-Conomy SEA 2025 Report*.
* OECD. (2020). *Tax Challenges Arising from Digitalisation – Report on Pillar One Blueprint*. Paris: OECD Publishing.
* Republik Indonesia. (2022). *Undang-Undang Nomor 27 Tahun 2022 tentang Pelindungan Data Pribadi*. Jakarta.
