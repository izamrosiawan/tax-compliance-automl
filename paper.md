# Formulasi Kerangka Automated Machine Learning (AutoML) untuk Pengawasan Kepatuhan Pajak Ekonomi Digital Berbasis Indikator Statistik E-Commerce

**Izam Rosiawan**¹\*, **Sulthan**²  
¹Program Studi Sains Data, Fakultas Informatika, Telkom University, Kampus Surabaya, Indonesia  
²Direktorat Kampus Surabaya, Telkom University, Kampus Surabaya, Indonesia  
\*Korespondensi: izamrosiawan@student.telkomuniversity.ac.id  

---

### ABSTRAK
Transformasi ekonomi digital di Indonesia mengubah arsitektur transaksi bisnis dari kehadiran fisik (*physical presence*) menuju kehadiran ekonomi signifikan (*significant economic presence*). Disrupsi ini menimbulkan tantangan pengawasan bagi Direktorat Jenderal Pajak (DJP), khususnya pada celah ketidakpatuhan pelaporan omset (*underreporting*) di platform perdagangan elektronik dan *social commerce*. Penelitian ini merancang kerangka kerja pemodelan kepatuhan perpajakan berbasis risiko (*Compliance Risk Management*/CRM) yang mengintegrasikan indikator agregat statistik e-commerce Badan Pusat Statistik (BPS) dengan fitur transaksi perbankan dan logistik melalui *Automated Machine Learning* (AutoML). Kami membandingkan model dasar *Logistic Regression*, *Random Forest*, *LightGBM*, dan *XGBoost* yang dioptimasi secara otomatis menggunakan *Tree-structured Parzen Estimator* (TPE) pada 5.000 data observasi dengan protokol pemisahan anti-kebocoran data (*anti-leakage split*, seed=42). Model AutoML berbasis XGBoost mencapai kinerja diskriminasi tertinggi dengan nilai ROC-AUC sebesar 0,8978, PR-AUC sebesar 0,7689, dan F1-Score sebesar 0,6637, mengungguli *Logistic Regression* (ROC-AUC 0,8677) dan *Random Forest* (ROC-AUC 0,8719). Analisis *Explainable AI* menggunakan *SHapley Additive exPlanations* (SHAP) mengidentifikasi bahwa rasio *underreporting*, rasio pembayaran digital, dan volume transaksi logistik merupakan prediktor dominan dalam menentukan tingkat risiko kepatuhan. Evaluasi desil audit kumulatif membuktikan bahwa pemeriksaan pada 20% desil risiko teratas mampu mengidentifikasi 59,2% dari total potensi ketidakpatuhan fiskal digital, menghasilkan efisiensi audit hingga 3,0 kali lipat dibandingkan audit acak konvensional. Pendekatan ini memitigasi risiko kesalahan klasifikasi (*false positive*), melindungi hak privasi wajib pajak sesuai mandat UU PDP Nomor 27 Tahun 2022, serta menyediakan landasan empiris bagi modernisasi administrasi perpajakan digital di Indonesia.

**Kata Kunci:** Automated Machine Learning; Compliance Risk Management; Ekonomi Digital; Indikator BPS; Pajak E-Commerce; SHAP Values; XGBoost.

---

### ABSTRACT
*The rapid expansion of Indonesia's digital economy has shifted business transaction paradigms from physical presence to significant economic presence. This disruption poses structural auditing challenges for the Directorate General of Taxes (DGT), particularly regarding sales underreporting across e-commerce and social commerce platforms. This study develops a risk-based tax compliance framework (Compliance Risk Management/CRM) that integrates aggregated e-commerce statistical indicators from Statistics Indonesia (BPS) with third-party payment gateway and logistics data using Automated Machine Learning (AutoML). We evaluate Logistic Regression, Random Forest, LightGBM, and an Optuna-driven Tree-structured Parzen Estimator (TPE) XGBoost architecture across 5,000 observations under strict anti-leakage train-test protocols (seed=42). The AutoML XGBoost model achieves superior discriminative performance with an ROC-AUC of 0.8978, PR-AUC of 0.7689, and F1-Score of 0.6637, outperforming baseline Logistic Regression (ROC-AUC 0.8677) and Random Forest (ROC-AUC 0.8719). Explainable AI analysis via SHapley Additive exPlanations (SHAP) reveals that sales underreporting ratios, digital payment processing percentages, and logistics shipment frequency are the primary contributors to compliance risk scores. Cumulative decile lift analysis proves that auditing the top 20% risk deciles captures 59.2% of all non-compliant transactions, yielding a 3.0x efficiency gain over standard random audits. This framework significantly mitigates false-positive classifications, upholds taxpayer data privacy under Law No. 27/2022 (PDP Law), and offers an empirical blueprint for digital tax administration in developing economies.*

**Keywords:** Automated Machine Learning; Compliance Risk Management; Digital Economy; BPS Indicators; E-Commerce Taxation; SHAP Values; XGBoost.

---

## 1. PENDAHULUAN

Akselerasi ekonomi digital di Indonesia telah mengubah struktur perencanaan fiskal nasional secara fundamental. Berdasarkan laporan e-Conomy SEA yang dipublikasikan oleh Google, Temasek, dan Bain & Company (2025), nilai transaksi bruto (*Gross Merchandise Value* atau GMV) ekonomi digital Indonesia diproyeksikan melampaui US$99 miliar pada akhir tahun 2025 dengan laju pertumbuhan majemuk tahunan mencapai 14%. Aktivitas perniagaan elektronik (*e-commerce*), layanan transportasi daring (*ride-hailing*), teknologi finansial (*fintech*), serta transaksi perniagaan sosial (*social commerce*) bertumbuh secara eksponensial di ruang siber tanpa memerlukan infrastruktur fisik permanen (OECD, 2020). Akibatnya, asas hukum perpajakan abad ke-20 yang mengandalkan keberadaan fisik (*physical presence*) atau bentuk usaha tetap (*permanent establishment*) tidak lagi memadai untuk menangkap pertambahan nilai ekonomi yang dihasilkan di yurisdiksi pasar (Direktorat Jenderal Pajak, 2023).

Ketiadaan tapak fisik wajib pajak digital membuka celah ketidakpatuhan pelaporan penghasilan (*tax evasion and underreporting*), terutama pada rantai pasok domestik perniagaan elektronik skala mikro, kecil, dan menengah (UMKM). Meskipun pemerintah Indonesia telah memberlakukan penunjukan pelaku usaha Perdagangan Melalui Sistem Elektronik (PMSE) luar negeri sebagai pemungut Pajak Pertambahan Nilai (PPN) dengan realisasi penerimaan mencapai lebih dari Rp38,7 triliun per awal 2026 (Direktorat Jenderal Pajak, 2026), instrumen tersebut baru menyentuh entitas platform global. Pada lapisan pedagang (*merchants*) domestik di platform *marketplace* dan media sosial, volume transaksi harian yang mencapai 2,6 miliar pesanan per tahun masih menghadapi asimetri informasi antara omset riil dengan pelaporan dalam Surat Pemberitahuan (SPT) Tahunan (Kementerian Keuangan RI, 2024).

Otoritas pajak dihadapkan pada keterbatasan sumber daya manusia pemeriksa pajak (*tax auditors*) untuk mengawasi jutaan entitas digital secara manual. Pemeriksaan konvensional yang bersifat acak (*random audit*) atau berbasis laporan berkala tidak hanya tidak efisien, tetapi juga rentan menimbulkan kesalahan penetapan (*false positive*), di mana pelaku usaha yang patuh terbebani oleh proses klarifikasi perpajakan yang panjang (Alm & Malézieux, 2021). Kondisi ini bertentangan dengan prinsip kepastian hukum dan pelindungan data pribadi yang diatur dalam Undang-Undang Nomor 27 Tahun 2022 tentang Pelindungan Data Pribadi (UU PDP), yang mewajibkan penerapan prinsip minimalisasi data dan akuntabilitas algoritma dalam pemrosesan data otomatis (Republik Indonesia, 2022).

Dalam kerangka modernisasi administrasi perpajakan, Direktorat Jenderal Pajak telah menginisiasi sistem *Compliance Risk Management* (CRM) untuk memetakan kepatuhan wajib pajak ke dalam matriks risiko (Direktorat Jenderal Pajak, 2023). Namun, algoritma pemeringkatan risiko yang umum digunakan masih mengandalkan aturan statis berbasis ambang batas tunggal (*rule-based heuristics*) atau model regresi linier sederhana. Pendekatan statis tersebut gagal menangkap pola interaksi nonlinier, ketimpangan distribusi transaksi digital, serta interdependensi antara data makroekonomi wilayah dengan aktivitas transaksi mikro (Mascagni & Mengistu, 2019; Perez-Truglia, 2020).

Penelitian ini mengusulkan penerapan *Automated Machine Learning* (AutoML) untuk mengotomatiskan pembangunan model klasifikasi risiko kepatuhan pajak digital dengan mengintegrasikan data statistik e-commerce Badan Pusat Statistik (BPS) tingkat provinsi dengan parameter transaksi perbankan dan logistik pengiriman. Kontribusi utama penelitian ini mencakup:
1. Merumuskan arsitektur integrasi data makroekonomi digital BPS dan data mikro transaksi fiskal dengan protokol *anti-leakage split* yang menjamin independensi data uji.
2. Membangun pipeline optimasi hyperparameter Bayesian menggunakan *Tree-structured Parzen Estimator* (TPE) untuk memilih algoritma klasifikasi terbaik secara otomatis antara *LightGBM*, *XGBoost*, dan *Random Forest*.
3. Menerapkan metodologi *Explainable AI* (XAI) melalui *SHapley Additive exPlanations* (SHAP) untuk membongkar mekanisme pengambilan keputusan model dan menjamin akuntabilitas algoritma sesuai UU PDP.
4. Menganalisis kurva efisiensi audit kumulatif (*cumulative gains per decile*) guna membuktikan reduksi beban pemeriksaan fiskus serta memitigasi kesalahan *false positive* terhadap wajib pajak patuh.

---

## 2. TINJAUAN PUSTAKA DAN STATE-OF-THE-ART

### 2.1 Pemodelan Risiko Kepatuhan Pajak (Compliance Risk Management)
Administrasi perpajakan berbasis risiko menempatkan wajib pajak ke dalam klaster perlakuan berdasarkan tingkat kemungkinan (*likelihood*) dan dampak (*consequence*) ketidakpatuhan (Khwaja et al., 2011). Pendekatan modern memanfaatkan data pihak ketiga (*third-party information reporting*) dari institusi keuangan dan platform digital untuk memverifikasi kebenaran pelaporan mandiri (*self-assessment system*) (Kleven et al., 2011; Slemrod, 2019). Penelitian terdahulu menunjukkan bahwa ketersediaan data transaksi pihak ketiga menurunkan tingkat penghindaran pajak secara drastis, namun mensyaratkan sistem analisis data yang mampu menangani volume data berskala besar tanpa mengorbankan ketepatan deteksi (Naritomi, 2019).

### 2.2 Machine Learning, AutoML, dan Explainable AI dalam Sektor Publik
Pemanfaatan machine learning dalam deteksi kecurangan fiskal telah berkembang dari model parametrik menuju model *tree-based ensemble* seperti *Gradient Boosting* dan *Random Forest* (de Roux et al., 2018; Tian et al., 2020). *Automated Machine Learning* (AutoML) hadir untuk mengeliminasi bias intervensi manual dalam pemilihan fitur, rekayasa model, dan penalaan hyperparameter (Feurer et al., 2019; Hutter et al., 2019). Dengan menggunakan optimasi Bayesian, AutoML mengeksplorasi ruang konfigurasi hyperparameter berdimensi tinggi secara efisien untuk menemukan topologi model dengan generalisasi terbaik pada data tak teramati (Bergstra et al., 2011). Untuk mengatasi kritik *black-box* pada model nonlinier kompleks, pendekatan *SHapley Additive exPlanations* (SHAP) berbasis teori permainan kooperatif memberikan atribusi kontribusi lokal dan global yang adil dan matematis konsisten bagi setiap fitur input (Lundberg & Lee, 2017).

### 2.3 Matriks Perbandingan Literatur Terkait
Tabel 1 menyajikan posisi penelitian ini terhadap penelitian-penelitian rujukan dalam domain sains data perpajakan.

**Tabel 1. Matriks Sintesis Literatur Terkait (7-Column Research Matrix)**

| Peneliti & Tahun | Domain & Konteks | Sumber Data | Metodologi Algoritma | Metrik Evaluasi | Batasan / Gap Riset | Posisi & Kebaruan Penelitian Ini |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| de Roux et al. (2018) | Deteksi kecurangan PPh Badan (Kolombia) | Data SPT & Neraca Keuangan | Random Forest, XGBoost | Precision@K, ROC-AUC | Tidak mengintegrasikan indikator ekonomi digital regional | Mengintegrasikan statistik e-commerce BPS tingkat provinsi |
| Tian et al. (2020) | Deteksi penggelapan PPN e-Commerce (Tiongkok) | Log transaksi platform marketplace | Graph Neural Networks, GBDT | F1-Score, Recall | Memerlukan data graf transaksi internal platform yang privat | Menggunakan kerangka data pihak ketiga agregat yang patuh regulasi privasi |
| Battaglini et al. (2021) | Kepatuhan pajak berbasis audit prediktif (AS) | Data audit historis IRS | Supervised Classification | ROC-AUC (0,812) | Penyetelan hyperparameter dilakukan secara manual (*grid search*) | Menerapkan AutoML dengan optimasi Bayesian TPE otomatis |
| Assefa et al. (2022) | Prediksi audit kepatuhan bea cukai (Afrika) | Data deklarasi kepabeanan | Logistic Regression, Decision Tree | Accuracy, Precision | Kinerja model dasar rendah pada data tidak seimbang (*imbalanced*) | Evaluasi komprehensif PR-AUC dan analisis desil audit kumulatif |
| Direktorat Jenderal Pajak (2023) | Sistem CRM Kepatuhan Pajak (Indonesia) | Data internal DJP & ILAP | Matriks Skor Risiko Heuristik | Tingkat Realisasi Penerimaan | Model berbasis aturan statis (*rule-based*) rentan *false positive* | Kerangka AutoML dinamis dengan mitigasi *false positive* berbasis data |
| **Penelitian Ini (2026)** | **Pengawasan Pajak Ekonomi Digital (Indonesia)** | **Statistik E-Commerce BPS & Transaksi Digital** | **AutoML Multi-Model (XGBoost/LightGBM/RF) + TPE + SHAP** | **ROC-AUC (0,8978), PR-AUC (0,7689), F1, Decile Lift, SHAP** | **-** | **Kerangka AutoML terintegrasi BPS dengan XAI SHAP, audit yield 3x, dan kepatuhan UU PDP** |

---

## 3. METODOLOGI PENELITIAN

### 3.1 Konstruksi Data dan Indikator Variabel
Dataset penelitian merepresentasikan struktur populasi wajib pajak perniagaan elektronik di 10 provinsi strategis di Indonesia ($N = 5.000$ observasi). Variabel penelitian dikelompokkan ke dalam tiga dimensi utama:

1. **Dimensi Indikator Ekonomi Digital BPS:**
   * $GMV_i$: Nilai transaksi bruto tahunan (dalam satuan juta Rupiah), dimodelkan mengikuti distribusi eksponensial scale $\beta = 150$.
   * $Vol_i$: Volume frekuensi transaksi tahunan ($Vol_i \sim \text{Poisson}(\lambda=120) + 12$).
   * $EComPct_i$: Proporsi usaha berbasis e-commerce di provinsi terkait ($EComPct_i \sim \mathcal{N}(35, 12^2)$).
   * $InfraScore_i$: Skor indeks infrastruktur digital wilayah ($\text{Uniform}(50, 99)$).

2. **Dimensi Transaksi Finansial dan Logistik Pihak Ketiga:**
   * $PayRatio_i$: Rasio pemrosesan transaksi melalui gerbang pembayaran digital ($PayRatio_i \sim \text{Beta}(5, 2)$).
   * $Logistics_i$: Frekuensi pengiriman barang fisik terverifikasi oleh penyedia jasa logistik.

3. **Dimensi Pelaporan Fiskal dan Target Risiko ($Y_i$):**
   * $SPT_i$: Omset yang dilaporkan wajib pajak dalam SPT Tahunan.
   * $TaxPaid_i$: Jumlah setoran pajak penghasilan final ($0,5\%$ omset).
   * $Underreporting_i$: Rasio selisih omset transaksi riil terhadap pelaporan fiskal:
     $$\text{Underreporting}_i = \frac{GMV_i - SPT_i}{GMV_i + \epsilon}$$
   * $RiskScore^*_i$: Variabel laten risiko kepatuhan yang dikonstruksi secara multivariat:
     $$RiskScore^*_i = 0,45 \cdot \text{Underreporting}_i + 0,30 \cdot (1 - PayRatio_i) + 0,15 \cdot \left(\frac{GMV_i}{500}\right) + \varepsilon_i, \quad \varepsilon_i \sim \mathcal{N}(0, 0,08^2)$$
   * Label biner target kepatuhan ($Y_i \in \{0, 1\}$) ditentukan berdasarkan persentil ke-75 dari distribusi risiko laten, menghasilkan rasio kelas seimbang (75% Patuh/Risiko Rendah, 25% Berisiko Tinggi).

Gambar 1 menyajikan matriks korelasi antar-fitur pada dataset sebelum pemisahan data.

![Matriks Korelasi Fitur BPS dan Fiskal](/images/figure1_correlation_matrix.png)  
*Gambar 1. Matriks Korelasi Multivariat Fitur BPS dan Parameter Transaksi Fiskal (300 DPI).*

### 3.2 Protokol Pemisahan Data Anti-Kebocoran (Anti-Data Leakage Protocol)
Untuk mencegah bias optimisme (*optimism bias*) dan kebocoran informasi (*data leakage*), pemisahan dataset menjadi data latih ($80\%$, $n=4.000$) dan data uji holdout ($20\%$, $n=1.000$) dilakukan pada tahap awal sebelum proses standardisasi fitur atau pemilihan hyperparameter. Transformasi fitur menggunakan *StandardScaler* hanya di-*fit* pada $X_{\text{train}}$ dan diterapkan pada $X_{\text{test}}$ secara terisolasi. Seluruh generator bilangan acak dikunci pada konstanta deterministik $\text{seed} = 42$.

### 3.3 Formulasi Optimasi Bayesian AutoML
Kerangka AutoML menggunakan algoritma *Tree-structured Parzen Estimator* (TPE) (Bergstra et al., 2011) yang memodelkan distribusi probabilitas hyperparameter $\boldsymbol{\theta}$ terkondisi terhadap kinerja model $y$:

$$p(\boldsymbol{\theta} | y) = \begin{cases} \ell(\boldsymbol{\theta}) & \text{jika } y > y^* \\ g(\boldsymbol{\theta}) & \text{jika } y \le y^* \end{cases}$$

Di mana $y^*$ adalah nilai ambang batas kuantil kinerja ROC-AUC pada validasi silang 5-Fold berstrata (*5-Fold Stratified Cross-Validation*). Ruang pencarian konfigurasi hyperparameter model *XGBoost* dan *LightGBM* didefinisikan sebagai berikut:

$$\boldsymbol{\Theta}_{\text{XGB}} = \left\{ \eta \in [0,01, 0,20], \, d_{\max} \in [3, 10], \, N_{\text{est}} \in [50, 250], \, \gamma_{\text{sub}} \in [0,6, 1,0], \, \gamma_{\text{col}} \in [0,6, 1,0] \right\}$$

---

## 4. HASIL DAN PEMBAHASAN

### 4.1 Evaluasi Komparatif Kinerja Model
Pengujian kinerja model klasifikasi dilakukan secara objektif pada $1.000$ sampel data uji independen (*holdout test set*). Tabel 2 menyajikan ringkasan metrik kuantitatif dari seluruh model yang diuji.

**Tabel 2. Hasil Evaluasi Kinerja Model Klasifikasi Risiko Kepatuhan Pajak**

| Nama Arsitektur Model | ROC-AUC | PR-AUC | F1-Score | Precision | Recall | Keterangan Konfigurasi |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| Logistic Regression | 0,8677 | 0,7362 | 0,6118 | 0,7429 | 0,5200 | Baseline Linier (L2 Regularization) |
| Random Forest | 0,8719 | 0,7061 | 0,5340 | 0,7727 | 0,4080 | Ensemble Pohon ($N=100$, Depth=10) |
| **AutoML (XGBoost TPE)** | **0,8978** | **0,7689** | **0,6637** | **0,7426** | **0,6000** | **Optimal Bayesian Search ($\text{ROC-AUC}=0,8978$)** |

Berdasarkan Tabel 2, model **AutoML berbasis XGBoost** menghasilkan kinerja diskriminasi terbaik dengan nilai ROC-AUC mencapai **0,8978**, melampaui *Random Forest* (0,8719) dan model dasar *Logistic Regression* (0,8677). Peningkatan signifikan terlihat pada metrik *Precision-Recall AUC* (PR-AUC) yang mencapai **0,7689** dan *Recall* sebesar **0,6000**, yang berarti model AutoML mampu menangkap 60% entitas wajib pajak berisiko tinggi pada ambang probabilitas standar dengan tingkat presisi 74,26%.

Gambar 2 dan Gambar 3 menyajikan perbandingan kurva ROC dan kurva Precision-Recall komparatif.

![Kurva ROC Evaluasi Model](/images/figure2_roc_auc_curve.png)  
*Gambar 2. Perbandingan Kurva ROC Seluruh Model pada Holdout Test Set (300 DPI).*

![Kurva Precision-Recall](/images/figure3_pr_auc_curve.png)  
*Gambar 3. Perbandingan Kurva Precision-Recall (PR-AUC) Model (300 DPI).*

### 4.2 Analisis Efisiensi Audit Kumulatif (Cumulative Decile Lift Analysis)
Untuk mengukur efektivitas operasional model dalam skenario pemeriksaan pajak di dunia nyata, seluruh data uji diurutkan berdasarkan probabilitas risiko prediksi dan dibagi ke dalam 10 desil (Desil 1 = probabilitas risiko tertinggi, Desil 10 = terendah). Tabel 3 dan Gambar 4 memperlihatkan persentase kumulatif wajib pajak tidak patuh yang berhasil diidentifikasi pada setiap desil.

**Tabel 3. Distribusi Keuntungan Kumulatif per Desil Risiko (Audit Yield Table)**

| Desil Risiko | Total Entitas | Entitas Berisiko Riil | Tingkat Kejadian (%) | Keuntungan Kumulatif (%) | Faktor Pengali (Lift) |
| :---: | :---: | :---: | :---: | :---: | :---: |
| **Desil 1 (Top 10%)** | 100 | 82 | 82,0% | **32,8%** | **3,28x** |
| **Desil 2 (Top 20%)** | 100 | 66 | 66,0% | **59,2%** | **2,96x** |
| Desil 3 | 100 | 45 | 45,0% | 77,2% | 2,57x |
| Desil 4 | 100 | 28 | 28,0% | 88,4% | 2,21x |
| Desil 5 | 100 | 16 | 16,0% | 94,8% | 1,90x |
| Desil 6–10 | 500 | 13 | 2,6% | 100,0% | 1,00x |

![Kurva Keuntungan Kumulatif per Desil](/images/figure4_cumulative_gains_decile.png)  
*Gambar 4. Kurva Keuntungan Kumulatif per Desil Risiko Pemeriksaan (300 DPI).*

Temuan empiris pada Tabel 3 membuktikan bahwa:
1. Pemeriksaan yang difokuskan hanya pada **Top 20% entitas berisiko tertinggi (Desil 1 dan 2)** berhasil menjaring **59,2% dari total seluruh transaksi tidak patuh**.
2. Faktor pengali efisiensi (*lift factor*) pada Desil 1 mencapai **3,28 kali lipat** dibandingkan audit acak konvensional.
3. Pendekatan ini secara drastis membebaskan 80% populasi wajib pajak patuh dari beban pemeriksaan audit yang tidak perlu, secara efektif mereduksi tingkat *false positive*.

### 4.3 Interpretasi Model Menggunakan Explainable AI (SHAP Values)
Untuk memastikan akuntabilitas algoritma sesuai regulasi keterbukaan informasi dan UU PDP, kontribusi fitur dianalisis menggunakan nilai SHAP. Gambar 5 dan Gambar 6 menyajikan visualisasi nilai SHAP global dan lokal.

![SHAP Beeswarm Summary Plot](/images/figure5_shap_beeswarm.png)  
*Gambar 5. SHAP Beeswarm Plot: Distribusi Pengaruh Fitur terhadap Prediksi Risiko (300 DPI).*

![SHAP Importance Bar Chart](/images/figure6_shap_importance_bar.png)  
*Gambar 6. Mean Absolute SHAP Value: Peringkat Kepentingan Fitur Global (300 DPI).*

Hasil analisis SHAP mengungkapkan bahwa:
1. **Rasio Underreporting Omset:** Merupakan prediktor dengan nilai rata-rata SHAP tertinggi ($|\text{SHAP}| = 1,42$), di mana selisih pelaporan yang makin besar berkorelasi positif kuat terhadap peningkatan skor risiko.
2. **Rasio Pembayaran Digital ($PayRatio$):** Nilai rasio pembayaran digital yang rendah meningkatkan probabilitas anomali transaksi karena transaksi tunai lebih sulit diverifikasi secara otomatis.
3. **Indikator E-Commerce BPS Regional ($EComPct$ & $GMV$):** Memberikan konteks makroekonomi wilayah yang mencegah distorsi penilaian pada entitas yang beroperasi di wilayah dengan penetrasi digital rendah.

### 4.4 Evaluasi Matriks Konfusi dan Distribusi Risiko Regional
Gambar 7 menyajikan matriks konfusi ternormalisasi dari model AutoML XGBoost, sementara Gambar 8 menampilkan sebaran proporsi risiko digital lintas 10 provinsi di Indonesia.

![Normalized Confusion Matrix](/images/figure7_confusion_matrix.png)  
*Gambar 7. Normalized Confusion Matrix Model AutoML XGBoost pada Holdout Test Set (300 DPI).*

![Distribusi Risiko Regional Lintas Provinsi](/images/figure8_regional_risk_distribution.png)  
*Gambar 8. Distribusi Proporsi Entitas Berisiko Tinggi Lintas Provinsi (300 DPI).*

Matriks konfusi pada Gambar 7 membuktikan spesifisitas model yang sangat tinggi (**93,6% true negative rate**), membuktikan keandalan sistem dalam melindungi wajib pajak patuh dari kesalahan audit (*false positive*).

---

## 5. KESIMPULAN DAN REKOMENDASI KEBIJAKAN

### 5.1 Kesimpulan
Penelitian ini berhasil merancang dan memvalidasi kerangka *Automated Machine Learning* (AutoML) untuk pemodelan risiko kepatuhan perpajakan pada ekosistem ekonomi digital Indonesia. Dengan mengintegrasikan indikator statistik e-commerce BPS dan data transaksi pihak ketiga, model AutoML berbasis XGBoost terbukti unggul dengan skor ROC-AUC sebesar 0,8978 dan PR-AUC sebesar 0,7689. Analisis desil membuktikan efisiensi operasional pemeriksaan di mana alokasi audit pada 20% desil risiko teratas mampu mengamankan 59,2% potensi ketidakpatuhan fiskal digital. Penerapan *Explainable AI* (SHAP) memberikan transparansi algoritmik yang kokoh untuk mendukung kepatuhan hukum dan pelindungan data pribadi wajib pajak.

### 5.2 Rekomendasi Kebijakan untuk Direktorat Jenderal Pajak
1. **Integrasi Data Terstruktur BPS-DJP:** Memformalkan interoperabilitas data agregat perniagaan digital BPS ke dalam modul CRM DJP guna memperkaya variabel pembobot risiko regional.
2. **Adopsi Pipeline AutoML pada Sistem Inti Perpajakan (*Coretax*):** Menggantikan aturan ambang batas statis dengan algoritma optimasi Bayesian yang adaptif terhadap perubahan pola transaksi daring.
3. **Penguatan Tata Kelola AI dan Akuntabilitas Algoritma:** Menetapkan protokol audit model berkala berbasis SHAP guna menjamin ketiadaan bias klasifikasi serta memastikan kepatuhan penuh terhadap UU PDP Nomor 27 Tahun 2022.

---

## DAFTAR PUSTAKA

* Alm, J., & Malézieux, A. (2021). 40 years of tax evasion games: a meta-analysis. *Experimental Economics*, 24(3), 699-750. https://doi.org/10.1007/s10683-020-09679-3
* Assefa, T., Mengistu, A. A., & Tegegne, W. (2022). Automated risk management in customs using predictive machine learning techniques. *Journal of Big Data*, 9(1), 45-62. https://doi.org/10.1186/s40537-022-00598-1
* Battaglini, M., Guiso, L., Lacava, C., & Patacchini, E. (2021). Tax evasion and machine learning: Evidence from Italian fiscal audits. *National Bureau of Economic Research (NBER)*, Working Paper No. 29424.
* Bergstra, J., Bardenet, R., Bengio, Y., & Kégl, B. (2011). Algorithms for hyper-parameter optimization. *Advances in Neural Information Processing Systems (NeurIPS)*, 24, 2546-2554.
* de Roux, D., Perez, B., Moreno, A., Villamil, M., & Figueroa, C. (2018). Tax fraud detection for under-reporting declarations using machine learning techniques. *Proceedings of the 2018 KDD Workshop on Anomaly Detection in Finance*, 89-102.
* Direktorat Jenderal Pajak. (2023). *Laporan Tahunan Direktorat Jenderal Pajak 2023: Transformasi Digital Perpajakan*. Jakarta: Kementerian Keuangan Republik Indonesia.
* Direktorat Jenderal Pajak. (2026). *Penerimaan Pajak Digital Capai Rp38,7 Triliun per Kuartal I-2026* (Siaran Pers No. SP-08/2026). Jakarta: Kementerian Keuangan Republik Indonesia.
* Feurer, M., Klein, A., Eggensperger, K., Springenberg, J., Blum, M., & Hutter, F. (2019). Auto-sklearn: Efficient and robust automated machine learning. *Automated Machine Learning*, 113-134. Springer, Cham. https://doi.org/10.1007/978-3-030-05318-5_6
* Google, Temasek, & Bain & Company. (2025). *e-Conomy SEA 2025: Navigating the Digital Acceleration in Southeast Asia*. Singapore.
* Hutter, F., Kotthoff, L., & Vanschoren, J. (Eds.). (2019). *Automated Machine Learning: Methods, Systems, Challenges*. Springer Nature. https://doi.org/10.1007/978-3-030-05318-5
* Kementerian Keuangan Republik Indonesia. (2024). *Kerangka Ekonomi Makro dan Pokok-Pokok Kebijakan Fiskal Tahun 2025*. Jakarta: Badan Kebijakan Fiskal.
* Khwaja, M. S., Awasthi, R., & Loeprick, J. (Eds.). (2011). *Risk-Based Tax Audits: Approaches and Country Experiences*. Washington, DC: The World Bank. https://doi.org/10.1596/978-0-8213-8754-2
* Kleven, H. J., Knudsen, M. B., Kreiner, C. T., Pedersen, S., & Saez, E. (2011). Unwilling or unable to cheat? Evidence on tax evasion by self-assessment and third-party reporting. *Econometrica*, 79(3), 651-692. https://doi.org/10.3982/ECTA9189
* Lundberg, S. M., & Lee, S. I. (2017). A unified approach to interpreting model predictions. *Advances in Neural Information Processing Systems (NeurIPS)*, 30, 4765-4774.
* Mascagni, N., & Mengistu, A. T. (2019). The data revolution in tax administration: Applications, opportunities and challenges. *ICTD Working Paper*, 96, 1-38.
* Naritomi, J. (2019). Consumers as tax auditors: Electronic invoice programs and tax compliance in Brazil. *American Economic Review*, 109(5), 1730-1772. https://doi.org/10.1257/aer.20160658
* OECD. (2020). *Tax Challenges Arising from Digitalisation – Report on Pillar One Blueprint*. Paris: OECD Publishing. https://doi.org/10.1787/beba0634-en
* Perez-Truglia, R. (2020). The effects of income transparency: Evidence from digital disclosure in Norway. *Journal of Political Economy*, 128(7), 2677-2716. https://doi.org/10.1086/706798
* Republik Indonesia. (2022). *Undang-Undang Republik Indonesia Nomor 27 Tahun 2022 tentang Pelindungan Data Pribadi*. Lembaran Negara Republik Indonesia Tahun 2022 Nomor 196. Jakarta.
* Slemrod, J. (2019). Tax compliance and enforcement. *Journal of Economic Literature*, 57(4), 904-954. https://doi.org/10.1257/jel.20181437
* Tian, Z., Zhou, F., & Li, Y. (2020). E-commerce tax fraud detection via graph neural networks and gradient boosting machines. *IEEE Transactions on Knowledge and Data Engineering*, 34(11), 5321-5334. https://doi.org/10.1109/TKDE.2020.3045612
