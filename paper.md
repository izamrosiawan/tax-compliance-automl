# Kerangka Benchmark Simulasi Non-Sirkular untuk Pemeringkatan Risiko Kepatuhan Pajak Digital melalui Integrasi Data Transaksi, Logistik, dan Indikator Makro BPS

**Izam Rosiawan**¹\*, **Sulthan**²  
¹Program Studi Sains Data, Fakultas Informatika, Telkom University, Kampus Surabaya, Indonesia  
²Direktorat Kampus Surabaya, Telkom University, Kampus Surabaya, Indonesia  
\*Penulis Korespondensi: `izamrosiawan@student.telkomuniversity.ac.id`

---

### ABSTRAK
Pertumbuhan perniagaan elektronik di Indonesia menimbulkan tantangan pengawasan bagi Direktorat Jenderal Pajak (DJP), khususnya dalam memverifikasi kewajaran pelaporan peredaran usaha (*self-assessment*) pedagang daring. Mengingat adanya batasan kerahasiaan data perpajakan individual (*taxpayer confidentiality*), penelitian ini merancang sebuah kerangka kerja tolok ukur simulasi (*synthetic simulation benchmark*) yang dirancang secara murni non-sirkular. Target temuan audit dibangkitkan 100% dari variabel laten tak teramati (perilaku *cash skimming*, distorsi inventaris, dan anomali logistik), sedangkan data yang diamati model (*observable features*) diperlakukan sebagai proksi bernoise (*noisy proxies*). Melalui eksperimen terhadap 5.000 data observasi dengan prevalensi dasar (*base rate*) risiko sebesar 25,0% dan skema validasi silang berstrata 5-Fold ($\text{seed}=42$), kami mengevaluasi kemampuan pemeringkatan risiko (*risk ranking*) dari empat model: *Logistic Regression*, *Random Forest*, *LightGBM*, dan *AutoML XGBoost* yang dioptimasi menggunakan *Tree-structured Parzen Estimator* (TPE). Studi ablasi fitur menunjukkan bahwa pelaporan SPT mandiri semata memiliki daya pembeda yang sangat terbatas (ROC-AUC $0,5641$, 95% CI $[0,5281, 0,5994]$). Penambahan data transaksi digital dan logistik secara empiris meningkatkan performa pemeringkatan menjadi ROC-AUC $0,7667$ ($95\%$ CI $[0,7329, 0,7998]$) dan PR-AUC $0,5455$ (jauh melampaui garis dasar prevalensi $0,2500$). Penambahan indikator makro BPS menghasilkan ROC-AUC $0,7684$ dan mempertahankan tangkapan temuan pada 20% desil risiko teratas (*Top 20% Decile Yield*) sebesar $45,2\%$ (*cumulative lift* $2,26\times$). Model linier *Logistic Regression* menghasilkan ROC-AUC tertinggi ($0,7856$, 95% CI $[0,7529, 0,8168]$), sementara *AutoML XGBoost* berperan sebagai pembanding nonlinier utama ($0,7682$, 95% CI $[0,7346, 0,8011]$). Uji ketahanan spasial berulang (*repeated geographical holdout*) menghasilkan rata-rata ROC-AUC sebesar $0,7643 \pm 0,0321$, dan analisis sensitivitas DGP mengonfirmasi stabilitas pemeringkatan lintas variasi bobot parameter laten. Analisis SHAP mendeskripsikan kontribusi relatif fitur masukan terhadap skor prediksi tanpa mengasumsikan hubungan kausalitas langsung. Kerangka kerja ini menunjukkan nilai tambah integrasi data pihak ketiga dalam lingkungan simulasi serta menyediakan arsitektur sistem pendukung keputusan (*decision support system*) yang mendukung prinsip akuntabilitas tata kelola pemrosesan data.

**Kata Kunci:** Ablation Study, Compliance Risk Management, Data Generating Process, Indikator BPS, Pajak Digital, Risk Ranking, Synthetic Benchmark.

---

### ABSTRACT
*The expansion of electronic commerce in Indonesia presents monitoring hurdles for the Directorate General of Taxes (DGT), particularly in assessing the plausibility of self-reported turnover. Constrained by statutory taxpayer confidentiality, this paper develops a non-circular synthetic simulation benchmark. Ground-truth audit outcomes are generated exclusively from unobserved latent states (cash skimming propensity, inventory distortion, and logistics deviations), while observed input features serve as noisy empirical proxies. Across 5,000 simulated merchant profiles with a 25.0% baseline risk prevalence under 5-fold stratified cross-validation (seed=42), we benchmark the risk-ranking capabilities of Logistic Regression, Random Forest, LightGBM, and an Optuna-optimized AutoML XGBoost model. A feature ablation study shows that self-reported tax returns alone exhibit limited discriminatory power (ROC-AUC 0.5641, 95% CI [0.5281, 0.5994]). Progressively integrating digital transaction volumes and logistics tracking substantially improves ranking quality to ROC-AUC 0.7667 (95% CI [0.7329, 0.7998]) and PR-AUC 0.5455 (substantially above the 0.2500 prevalence baseline). Incorporating provincial macro indicators from BPS yields ROC-AUC 0.7684 and achieves a top 20% risk decile yield of 45.2% (2.26x cumulative lift). Logistic Regression delivers the highest holdout ROC-AUC (0.7856, 95% CI [0.7529, 0.8168]), establishing a strong linear baseline alongside non-linear AutoML models (0.7682, 95% CI [0.7346, 0.8011]). Repeated geographical holdout validation across unseen provinces yields a consistent mean ROC-AUC of 0.7643 +/- 0.0321, and DGP sensitivity tests confirm structural stability across varied latent parameter weights. SHAP analysis illustrates predictive feature attributions without implying causal mechanisms. This benchmark provides an empirical framework for multi-source risk-based tax decision support aligning with algorithmic accountability principles.*

**Keywords:** Ablation Study, Compliance Risk Management, Data Generating Process, BPS Indicators, Digital Taxation, Risk Ranking, Synthetic Benchmark.

---

## 1. PENDAHULUAN

Pertumbuhan ekonomi digital di Indonesia terus mencatatkan peningkatan volume transaksi yang pesat. Laporan e-Conomy SEA (Google, Temasek, & Bain, 2025) memperkirakan nilai transaksi bruto (*Gross Merchandise Value*) ekonomi digital Indonesia mencapai US$99 miliar pada tahun 2025. Perdagangan melalui lokapasar (*marketplace*) dan niaga sosial (*social commerce*) bertumpu pada interaksi virtual tanpa mengharuskan keberadaan kantor fisik atau tempat usaha permanen (OECD, 2020). Akibatnya, pengawasan perpajakan berbasis tapak fisik (*physical presence*) tidak lagi memadai untuk memantau peredaran usaha secara akurat (Direktorat Jenderal Pajak, 2023).

Kondisi tersebut memperbesar tantangan asimetri informasi pada pelaporan Surat Pemberitahuan (SPT) Tahunan, terutama pada sektor pedagang skala mikro dan menengah yang memiliki banyak saluran penjualan (Kementerian Keuangan RI, 2024). Meskipun pemerintah telah memungut PPN Perdagangan Melalui Sistem Elektronik (PMSE) dari penyedia platform digital luar negeri dengan penerimaan mencapai Rp38,7 triliun per awal 2026 (Direktorat Jenderal Pajak, 2026), proses verifikasi kepatuhan atas jutaan pedagang lokal tetap memerlukan pendekatan berbasis data yang efisien.

Mengingat keterbatasan jumlah personel pemeriksa pajak, pemeriksaan secara menyeluruh terhadap seluruh pedagang tidak memungkinkan. Melakukan pemeriksaan acak (*random audit*) tidak efisien serta berisiko membebani pelaku usaha yang sebenarnya patuh (*false positive*) (Alm & Malézieux, 2021). Di sisi lain, Undang-Undang Nomor 27 Tahun 2022 tentang Pelindungan Data Pribadi (UU PDP) mewajibkan pemrosesan data otomatis dilakukan secara akuntabel, terukur, dan meminimalkan beban administratif bagi masyarakat (Republik Indonesia, 2022).

Dalam kerangka *Compliance Risk Management* (CRM), otoritas pajak mengelompokkan wajib pajak ke dalam kuadran risiko guna menetapkan prioritas tindakan (Direktorat Jenderal Pajak, 2023). Karena data individual SPT wajib pajak dilindungi oleh asas kerahasiaan jabatan (Pasal 34 UU KUP), riset data sains komputasional membutuhkan tolok ukur simulasi (*simulation benchmark*) yang bebas dari kelemahan metodologis (*target circularity*) untuk menguji efektivitas integrasi data pihak ketiga.

Penelitian ini merumuskan kerangka tolok ukur simulasi non-sirkular untuk pemeringkatan risiko (*risk ranking*) kepatuhan pajak digital. Kontribusi utama penelitian ini meliputi:
a. **Desain Target Laten Non-Sirkular:** Memisahkan secara tegas variabel laten tak teramati pembentuk label temuan audit dari fitur-fitur masukan teramati ($X$).
b. **Studi Ablasi Fitur Bertahap:** Mengukur kontribusi marginal dari data pelaporan mandiri, transaksi digital, logistik, dan data makroekonomi BPS dengan interval kepercayaan 95% (*95% Confidence Interval*).
c. **Validasi Geografis Berulang (*Repeated Geographical Holdout*):** Menguji kemampuan generalisasi spasial model pada kelompok provinsi yang belum pernah dilihat dalam data latih.
d. **Pemosisian Model sebagai Decision Support System:** Memposisikan model sebagai alat pemeringkat prioritas audit (*risk ranking*), didukung analisis keterbukaan SHAP yang mendukung prinsip akuntabilitas dalam tata kelola pemrosesan data.

---

## 2. TINJAUAN PUSTAKA DAN STATE-OF-THE-ART

### 2.1 Informasi Pihak Ketiga dan Perilaku Kepatuhan
Model kepatuhan pajak Allingham-Sandmo-Yitzhaki menempatkan wajib pajak sebagai agen ekonomi yang menimbang manfaat penghindaran pajak terhadap risiko terdeteksi (Alm & Malézieux, 2021). Kajian empiris oleh Kleven et al. (2011) serta Slemrod (2019) membuktikan bahwa ketersediaan laporan informasi pihak ketiga (*third-party information reporting*) secara substansial menekan peluang ketidakpatuhan. Pada ekosistem digital, integrasi data transaksi perbankan dan resi pengiriman barang menjadi instrumen verifikasi silang paling efektif (Naritomi, 2019).

### 2.2 Machine Learning, AutoML, dan Interpretabilitas Model
Penerapan algoritma machine learning telah banyak dieksplorasi untuk mendeteksi anomali pada data keuangan (de Roux et al., 2018; Tian et al., 2020). *Automated Machine Learning* (AutoML) dengan algoritma *Tree-structured Parzen Estimator* (TPE) mengotomatiskan pencarian konfigurasi hyperparameter berdasarkan pendekatan Bayesian (Bergstra et al., 2011; Feurer et al., 2019).

Untuk memastikan transparansi keputusan, metode *SHapley Additive exPlanations* (SHAP) memberikan estimasi kontribusi fitur masukan terhadap nilai prediksi (Lundberg & Lee, 2017):

$$g(z') = \phi_0 + \sum_{j=1}^{M} \phi_j z'_j$$

Nilai $\phi_j$ menunjukkan besaran atribusi prediktif variabel ke-$j$ terhadap skor risiko individual tanpa mengklaim hubungan sebab-akibat kausal murni.

### 2.3 Matriks Literatur Rujukan (7 Kolom Standar Riset)
Tabel 1 menyajikan posisi penelitian ini dalam literatur machine learning perpajakan.

**Tabel 1. Matriks Sintesis Literatur Terkait (7 Kolom Standar Riset)**

| Peneliti & Tahun | Domain & Konteks | Sumber Data | Metodologi Algoritma | Metrik Evaluasi | Batasan Riset Sebelumnya | Posisi & Diferensiasi Riset Ini |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| de Roux et al. (2018) | Kecurangan PPh Badan (Kolombia) | SPT & Laporan Keuangan | Random Forest, XGBoost | Precision@K, ROC-AUC | Tidak memasukkan variabel logistik dan indikator makro wilayah | Menambahkan variabel logistik pihak ketiga dan indikator BPS regional |
| Tian et al. (2020) | PPN e-Commerce (Tiongkok) | Log platform marketplace | GNN, GBDT | F1-Score, Recall | Bergantung pada data graf internal platform privat | Menggunakan kerangka data pihak ketiga agregat yang dapat diakses |
| Battaglini et al. (2021) | Kepatuhan Pajak (Italia) | Data audit historis fiskus | Supervised Classification | ROC-AUC (0,812) | Penyetelan hyperparameter manual tanpa uji ketahanan spasial | Menggunakan optimasi Bayesian TPE dan validasi holdout geografis berulang |
| Assefa et al. (2022) | Audit Kepabeanan (Afrika) | Deklarasi pabean | Logistic Regression, Decision Tree | Accuracy, Precision | Performa rendah pada data tidak seimbang (*imbalanced*) | Menggunakan PR-AUC, bootstrap CI, dan studi ablasi fitur bertahap |
| DJP (2023) | Sistem CRM Pajak (Indonesia) | Data internal & ILAP | Aturan Matriks Heuristik | Realisasi Penerimaan | Model berbasis aturan statis rentan *false positive* | Membangun tolok ukur simulasi non-sirkular berbasis AutoML |
| **Penelitian Ini (2026)** | **Benchmark Pajak Digital Indonesia** | **Simulasi Laten & Data Pihak Ketiga** | **AutoML XGBoost + Logistic + TPE + SHAP** | **ROC-AUC (95% CI), PR-AUC, Decile Yield, Geo-Holdout** | **-** | **Mengembangkan framework simulasi yang mengintegrasikan DGP variabel laten dengan repeated geographical holdout** |

---

## 3. METODOLOGI PENELITIAN

### 3.1 Data Generating Process (DGP) dan Arsitektur Variabel
Tabel 2 merangkum struktur variabel, distribusi pembangkitan, dan peranannya dalam kerangka kerja eksperimen.

**Tabel 2. Karakteristik Variabel dan Mekanisme Pembangkitan Data (DGP Table)**

| Nama Variabel | Level Data | Distribusi / Mekanisme Pembangkitan Lengkap | Peran dalam Eksperimen | Digunakan di Formula Target $Y$? |
| :--- | :--- | :--- | :--- | :---: |
| $\delta_{\text{cash}}$ | Wajib Pajak (Laten) | $\text{Beta}(2.0, 4.0)$ | Unobserved Ground Truth | **Ya** |
| $\delta_{\text{inv}}$ | Wajib Pajak (Laten) | $\text{Exponential}(\beta=0.25)$ | Unobserved Ground Truth | **Ya** |
| $\delta_{\text{log}}$ | Wajib Pajak (Laten) | $\text{Beta}(1.5, 4.5)$ | Unobserved Ground Truth | **Ya** |
| $u_{\text{frac}}$ | Wajib Pajak (Perantara) | $\text{Clip}\left(0,40\delta_{\text{cash}} + 0,30\left(\frac{\delta_{\text{inv}}}{1+\delta_{\text{inv}}}\right) + \mathcal{N}(0,10, 0,10^2), 0, 0,85\right)$ | Intermediate Variable | **Tidak** |
| $GMV_i$ | Wajib Pajak (Teramati) | $\text{Poisson}(\lambda=140)+20 \times \text{Lognormal}(\mu=4.8, \sigma=0.6) / 1000$ | Noisy Feature ($X$) | **Tidak** |
| $SPT_i$ | Wajib Pajak (Teramati) | $GMV_i \times (1 - u_{\text{frac}})$ | Noisy Feature ($X$) | **Tidak** |
| $TaxPaid_i$ | Wajib Pajak (Teramati) | $SPT_i \times 0,005$ (PPh Final PP 55/2022) | Noisy Feature ($X$) | **Tidak** |
| $PayRatio_i$ | Wajib Pajak (Teramati) | $\text{Clip}\left(1.0 - (0.60\delta_{\text{cash}} + \mathcal{N}(0,20, 0,10^2)), 0.05, 0.99\right)$ | Noisy Feature ($X$) | **Tidak** |
| $Logistics_i$ | Wajib Pajak (Teramati) | $\text{Clip}\left(1.0 - (0.50\delta_{\text{log}} + \mathcal{N}(0,15, 0,08^2)), 0.10, 1.00\right)$ | Noisy Feature ($X$) | **Tidak** |
| $EComPct_p$ | Provinsi (Makro) | BPS Benchmark $\pm \mathcal{N}(0, 1.5)$ | Contextual Feature ($X$) | **Tidak** |
| $Infra_p$ | Provinsi (Makro) | BPS Benchmark $\pm \mathcal{N}(0, 1.2)$ | Contextual Feature ($X$) | **Tidak** |
| $Y_i$ (Target) | Wajib Pajak (Audit) | $\mathbb{I}(S^*_{\text{audit}} > P_{75}), \quad \text{Prevalensi Positif } = 25,0\%$ | Ground Truth Label ($Y$) | **Target** |

Formula pembentukan skor temuan audit laten adalah:
$$S^*_{\text{audit}} = 0,40 \cdot \delta_{\text{cash}} + 0,35 \cdot \left(\frac{\delta_{\text{inv}}}{1 + \delta_{\text{inv}}}\right) + 0,25 \cdot \delta_{\text{log}} + \varepsilon_i, \quad \varepsilon_i \sim \mathcal{N}(0, 0,08^2)$$

Hubungan struktural antara variabel laten, fitur masukan teramati, dan proses klasifikasi diilustrasikan pada diagram berikut:

```
          [ STATE LATEN TAK TERAMATI ]
         ┌────────────┬─────────────┬────────────┐
         │ δ_cash     │ δ_inv       │ δ_log      │
         └─────┬──────┴──────┬──────┴─────┬──────┘
               │             │            │
      ┌────────┼─────────────┼────────────┼────────┐
      │        ↓             ↓            ↓        │
      │   [PayRatio]      [SPT/GMV]  [Logistics]   │
      │        │             │            │        │
      │        └─────────────┼────────────┘        │
      │                      ↓                     │
      │           FITUR TERAMATI (X)               │
      │                      ↓                     │
      │           MODEL MACHINE LEARNING           │
      │                      ↓                     │
      │             PREDIKSI SKOR RISIKO           │
      └────────────────────────────────────────────┘
                             │
            DIEVALUASI TERHADAP GROUND TRUTH
                             ↓
              TARGET TEMUAN AUDIT LATEN (Y)
```

Gambar 1 menyajikan korelasi antar-fitur teramati.

![Matriks Korelasi Fitur](/images/figure1_correlation_matrix.png)  
*Gambar 1. Matriks Korelasi Multivariat Fitur BPS dan Parameter Transaksi (300 DPI).*

### 3.2 Protokol Validasi dan Estimasi Interval Kepercayaan
Data dibagi menjadi 80% data latih ($n=4.000$) dan 20% data uji independen ($n=1.000$). Optimasi Bayesian TPE dijalankan murni di dalam validasi silang berstrata 5-Fold pada data latih. Estimasi interval kepercayaan 95% (95% CI) dihitung menggunakan prosedur non-parametrik bootstrap ($B=500$ iterasi) yang dilakukan secara eksklusif pada pasangan prediksi probabilitas dan label data uji dengan bobot model yang telah dibekukan (*fixed trained model weights*).

---

## 4. HASIL DAN PEMBAHASAN

### 4.1 Evaluasi Komparatif Kinerja Model Pemeringkat Risiko
Tabel 3 merangkum performa model pada data uji independen ($n=1.000$, dengan garis dasar prevalensi $P(Y=1) = 25,0\%$).

**Tabel 3. Evaluasi Kinerja Model Klasifikasi dan Pemeringkatan Risiko ($n=1.000, \text{Base Rate} = 0,2500$)**

| Model | ROC-AUC (95% CI) | PR-AUC (95% CI) | F1-Score | Precision | Recall | Specificity | Top 20% Yield (%) | Cumulative Lift | Matriks Konfusi (TN/FP/FN/TP) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Logistic Regression** | **0,7856 [0,7529, 0,8168]** | **0,5633 [0,4991, 0,6299]** | 0,3955 | 0,6514 | 0,2840 | 0,9493 | **47,6%** | **2,38x** | 712 / 38 / 179 / 71 |
| Random Forest | 0,7572 [0,7219, 0,7901] | 0,5348 [0,4723, 0,5959] | 0,3164 | 0,6235 | 0,2120 | 0,9573 | 44,0% | $2,20\times$ | 718 / 32 / 197 / 53 |
| LightGBM | 0,7413 [0,7073, 0,7755] | 0,4901 [0,4271, 0,5596] | 0,4386 | 0,6316 | 0,3360 | 0,9347 | 42,4% | $2,12\times$ | 701 / 49 / 166 / 84 |
| **AutoML XGBoost** | 0,7682 [0,7346, 0,8011] | 0,5496 [0,4804, 0,6128] | 0,3747 | 0,6018 | 0,2720 | 0,9400 | **45,6%** | **2,28x** | 705 / 45 / 182 / 68 |

Pada Tabel 3, *Logistic Regression* menghasilkan skor ROC-AUC tertinggi ($0,7856$), menunjukkan bahwa hubungan linear antara variabel proksi dan risiko laten dalam simulasi ini sangat kuat. *AutoML XGBoost* berperan penting sebagai model pembanding nonlinier utama ($0,7682$, 95% CI $[0,7346, 0,8011]$). Seluruh model menghasilkan nilai PR-AUC ($0,4901$ hingga $0,5633$) yang jauh melampaui garis dasar prevalensi $P(Y=1) = 0,2500$.

Fokus utama pemanfaatan model adalah **pemeringkatan probabilitas risiko (*risk ranking*)**, di mana pemeriksaan pada 20% desil risiko teratas berhasil menjaring **45,6% hingga 47,6% total ketidakpatuhan**. Kurva ROC dan PR disajikan pada Gambar 2 dan Gambar 3.

![Kurva ROC Komparatif](/images/figure2_roc_auc_curve.png)  
*Gambar 2. Kurva ROC Komparatif pada Data Uji Independen (300 DPI).*

![Kurva Precision-Recall](/images/figure3_pr_auc_curve.png)  
*Gambar 3. Kurva Precision-Recall Komparatif terhadap Garis Dasar Prevalensi (300 DPI).*

### 4.2 Studi Ablasi Fitur Bertahap (*Feature Ablation Study*)
Tabel 4 dan Gambar 5 menyajikan hasil evaluasi ablasi fitur.

**Tabel 4. Hasil Studi Ablasi Fitur Menggunakan Model XGBoost**

| Konfigurasi Fitur | ROC-AUC | PR-AUC (vs Base 0,25) | Top 20% Decile Yield (%) | Cumulative Lift | Temuan Empiris |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **1. Data SPT Mandiri Saja** | 0,5641 | 0,3192 | 27,2% | $1,36\times$ | Pelaporan mandiri semata memiliki daya pembeda yang sangat terbatas |
| **2. + Transaksi Digital (Gateway & GMV)** | 0,7348 | 0,5197 | 43,6% | $2,18\times$ | Peningkatan substansial (+0,1707 AUC); menangkap volume peredaran usaha |
| **3. + Data Logistik Pengiriman** | 0,7667 | 0,5455 | 46,0% | $2,30\times$ | Peningkatan diskriminasi tertinggi melalui verifikasi pergerakan barang fisik |
| **4. Model Penuh (+ Indikator Makro BPS)** | **0,7684** | **0,5467** | **45,2%** | **2,26x** | Memberikan konteks makro wilayah dan menjaga stabilitas pemeringkatan |

![Hasil Studi Ablasi](/images/figure5_ablation_study_bars.png)  
*Gambar 5. Perbandingan Skor ROC-AUC pada Studi Ablasi Fitur (300 DPI).*

Berdasarkan Tabel 4:
a. Pelaporan SPT mandiri semata tidak memadai (ROC-AUC $0,5641$).
b. Penambahan data transaksi perbankan dan logistik memberikan lonjakan performa terbesar (ROC-AUC naik ke $0,7667$).
c. Penambahan indikator makroekonomi BPS memberikan kontribusi marginal kecil namun menjaga stabilitas pemeringkatan desil dengan ROC-AUC $0,7684$.

### 4.3 Analisis Efisiensi Desil Audit (*Audit Yield*)
Gambar 4 menampilkan kurva tangkapan kumulatif berdasarkan desil risiko.

![Kurva Keuntungan Kumulatif per Desil](/images/figure4_cumulative_gains_decile.png)  
*Gambar 4. Kurva Keuntungan Kumulatif Temuan Audit per Desil Risiko (300 DPI).*

Dengan memprioritaskan pemeriksaan pada **Top 20% kelompok berisiko tertinggi (Desil 1 dan 2)**, sistem berhasil menjaring **45,2% hingga 47,6% dari total potensi ketidakpatuhan**, menghasilkan faktor pengali *cumulative lift* sebesar **$2,26\times$ hingga $2,38\times$** dibandingkan pemilihan audit acak (20%).

### 4.4 Uji Ketahanan Spasial dan Sensitivitas Bobot DGP
Tabel 5 merangkum hasil uji sensitivitas model terhadap variasi bobot parameter laten pada DGP.

**Tabel 5. Hasil Uji Sensitivitas Spesifikasi Parameter Bobot Laten DGP**

| Skenario Bobot Laten DGP $(\delta_{\text{cash}} / \delta_{\text{inv}} / \delta_{\text{log}})$ | Karakteristik Skenario | Logistic Regression ROC-AUC | XGBoost ROC-AUC |
| :--- | :--- | :---: | :---: |
| **Skenario A (0,40 / 0,35 / 0,25)** | Baseline Seimbang | 0,7804 | 0,7531 |
| **Skenario B (0,25 / 0,50 / 0,25)** | Dominan Distorsi Inventaris | 0,7430 | 0,6931 |
| **Skenario C (0,30 / 0,25 / 0,45)** | Dominan Anomali Logistik | 0,7681 | 0,7648 |

Validasi geografis berulang lintas pasangan provinsi holdout pada Gambar 8 menghasilkan skor stabil dengan rata-rata **$0,7643 \pm 0,0321$**. Hasil pada Tabel 5 membuktikan bahwa urutan keunggulan integrasi fitur tetap konsisten di bawah berbagai variasi bobot parameter laten.

![Uji Ketahanan Spasial](/images/figure8_geographical_holdout.png)  
*Gambar 8. Evaluasi Ketahanan Spasial Lintas Pasangan Provinsi Holdout (300 DPI).*

### 4.5 Atribusi Prediktif Berbasis SHAP dan Matriks Konfusi
Gambar 6 dan Gambar 7 menampilkan atribusi nilai SHAP dan matriks konfusi ternormalisasi.

![SHAP Beeswarm Plot](/images/figure6_shap_beeswarm.png)  
*Gambar 6. Distribusi Nilai SHAP: Kontribusi Fitur terhadap Prediksi Risiko (300 DPI).*

![Matriks Konfusi Ternormalisasi](/images/figure7_confusion_matrix.png)  
*Gambar 7. Normalized Confusion Matrix Model XGBoost (300 DPI).*

Nilai SHAP mengonfirmasi bahwa rasio pembayaran digital dan keterlacakan logistik merupakan variabel dengan kontribusi prediktif tertinggi. Spesifisitas sebesar **$94,0\%$** menunjukkan tingkat *false-positive rate* yang relatif rendah pada ambang klasifikasi yang digunakan.

---

## 5. KESIMPULAN DAN REKOMENDASI

### 5.1 Kesimpulan
Penelitian ini berhasil menyusun kerangka tolok ukur simulasi non-sirkular yang memisahkan variabel laten temuan audit dari fitur-fitur masukan teramati. Studi ablasi membuktikan bahwa pelaporan mandiri wajib pajak tidak memadai untuk mendeteksi risiko (ROC-AUC $0,5641$), sedangkan integrasi data gerbang pembayaran dan logistik secara substansial meningkatkan kualitas pemeringkatan risiko (ROC-AUC $0,7667$ dan Top 20% Decile Yield $46,0\%$). Model linier *Logistic Regression* memberikan kinerja diskriminasi tertinggi ($0,7856$), sementara *AutoML XGBoost* menyediakan alternatif nonlinier yang kompetitif ($0,7682$). Validasi spasial berulang mengonfirmasi stabilitas model lintas provinsi ($0,7643 \pm 0,0321$), dan uji sensitivitas DGP membuktikan ketahanan struktur pemeringkatan. Analisis SHAP memberikan transparansi atribusi prediktif guna mendukung tata kelola AI yang akuntabel.

### 5.2 Rekomendasi Kebijakan
a. **Interoperabilitas Data Transaksi dan Logistik:** Memprioritaskan penguatan integrasi data pihak ketiga (perbankan, gerbang pembayaran, dan ekspedisi logistik) sebagai pilar utama pengawasan kepatuhan ekonomi digital.
b. **Pemanfaatan Model sebagai Alat Pemeringkat Prioritas (*Risk Ranking Tool*):** Menggunakan skor probabilitas model murni sebagai instrumen penyaring prioritas pemeriksaan (*decision support system*), bukan penentu sanksi hukum otomatis, guna mendukung prinsip akuntabilitas dalam pemrosesan data.
c. **Validasi Berkala Lintas Wilayah:** Melakukan evaluasi berkala terhadap indikator regional BPS guna memastikan bobot kontekstual wilayah tidak menimbulkan bias kedaerahan.

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
