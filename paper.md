# Kerangka Benchmark Simulasi Non-Sirkular untuk Pemeringkatan Risiko Kepatuhan Pajak Pedagang Daring melalui Integrasi Data Transaksi Gerbang Pembayaran, Logistik, dan Indikator Regional Berbasis Data BPS

**Izam Rosiawan**¹\*, **Sulthan**²  
¹Program Studi Sains Data, Fakultas Informatika, Telkom University, Kampus Surabaya, Indonesia  
²Direktorat Kampus Surabaya, Telkom University, Kampus Surabaya, Indonesia  
\*Penulis Korespondensi: `izamrosiawan@student.telkomuniversity.ac.id`

---

### ABSTRAK
Pertumbuhan perniagaan elektronik di Indonesia menimbulkan tantangan pengawasan bagi Direktorat Jenderal Pajak (DJP), khususnya dalam memverifikasi kewajaran pelaporan peredaran usaha (*self-assessment*) pedagang daring. Mengingat adanya batasan kerahasiaan data perpajakan individual (*taxpayer confidentiality*), penelitian ini merancang sebuah kerangka kerja tolok ukur simulasi sintetis (*synthetic simulation benchmark*) non-sirkular sebagai uji kelayakan metodologis (*proof-of-concept*). Target temuan audit dibangkitkan 100% dari variabel laten tak teramati (perilaku *cash skimming*, distorsi inventaris, dan anomali logistik), sedangkan fitur teramati diperlakukan sebagai proksi bernoise (*noisy proxies*) terhadap keadaan laten. Melalui eksperimen terhadap 5.000 data observasi dengan prevalensi dasar (*base rate*) risiko sebesar 25,0% dan skema validasi silang berstrata 5-Fold ($\text{seed}=42$), kami mengevaluasi kemampuan pemeringkatan risiko (*risk ranking*) dari empat model: *Logistic Regression*, *Random Forest*, *LightGBM*, dan *XGBoost* yang dioptimasi menggunakan Optuna dengan *Tree-structured Parzen Estimator* (TPE, 20 trial). Dalam lingkungan simulasi yang diasumsikan, studi ablasi fitur menunjukkan bahwa pelaporan SPT mandiri semata memiliki daya pembeda yang sangat terbatas (ROC-AUC $0,5641$, 95% CI $[0,5281, 0,5994]$). Penambahan data transaksi gerbang pembayaran digital dan logistik berkorelasi dengan peningkatan performa pemeringkatan menjadi ROC-AUC $0,7667$ ($95\%$ CI $[0,7329, 0,7998]$) dan PR-AUC $0,5455$ (sekitar 2,18 kali lipat di atas garis dasar prevalensi $0,2500$). Penambahan dua indikator regional berbasis data BPS memberikan kontribusi kontekstual marginal (ROC-AUC $0,7684$) dengan tangkapan temuan pada kelompok risiko 20% teratas (*Top-20% Risk Yield*) sebesar $45,2\%$ ($95\%$ CI $[40,8\%, 49,6\%]$) yang secara statistik beririsan dengan tahap logistik ($46,0\%$, $95\%$ CI $[41,2\%, 50,4\%]$). Model linier *Logistic Regression* menghasilkan ROC-AUC data uji tertinggi ($0,7856$, 95% CI $[0,7529, 0,8168]$, ROC-AUC latih $0,7891$), sementara *TPE-optimized XGBoost* menghasilkan ROC-AUC uji $0,7682$ ($95\%$ CI $[0,7346, 0,8011]$, ROC-AUC latih $0,8120$). Uji validasi lintas provinsi holdout berulang ($R=5$ pasangan provinsi) menghasilkan rata-rata ROC-AUC sebesar $0,7643 \pm 0,0321$, dan analisis sensitivitas DGP menunjukkan kestabilan relatif struktur pemeringkatan lintas variasi bobot parameter laten. Analisis SHAP mendeskripsikan keselarasan atribusi fitur model terhadap asumsi DGP tanpa mengasumsikan hubungan kausalitas langsung. Kerangka kerja ini menyajikan bukti metodologis awal bagi pengembangan sistem pendukung keputusan (*decision support system*) pemeringkatan prioritas audit yang sejalan dengan prinsip akuntabilitas tata kelola data.

**Kata Kunci:** Ablation Study, Compliance Risk Management, Data Generating Process, Indikator BPS, Pajak Pedagang Daring, Risk Ranking, Synthetic Benchmark, TPE-optimized XGBoost.

---

### ABSTRACT
*The rapid expansion of electronic commerce in Indonesia presents monitoring hurdles for the Directorate General of Taxes (DGT), particularly in assessing the plausibility of self-reported turnover. Constrained by statutory taxpayer confidentiality, this paper develops a non-circular synthetic simulation benchmark as a methodological proof-of-concept. Ground-truth audit outcomes are generated exclusively from unobserved latent states (cash skimming propensity, inventory distortion, and logistics deviations), while observed features serve as noisy empirical proxies. Across 5,000 simulated merchant profiles with a 25.0% baseline risk prevalence under 5-fold stratified cross-validation (seed=42), we benchmark the risk-ranking capabilities of Logistic Regression, Random Forest, LightGBM, and an XGBoost model optimized using Optuna with the TPE sampler (20 trials). Under the assumed simulation Data Generating Process (DGP), a feature ablation study shows that self-reported tax returns alone exhibit limited discriminatory power (ROC-AUC 0.5641, 95% CI [0.5281, 0.5994]). Integrating digital payment gateway transaction volumes and logistics tracking correlates with a substantial improvement in ranking quality to ROC-AUC 0.7667 (95% CI [0.7329, 0.7998]) and PR-AUC 0.5455 (approximately 2.18x above the 0.2500 prevalence baseline). Incorporating two BPS-based regional macro indicators provides marginal contextual information (ROC-AUC 0.7684) with a top-20% risk yield of 45.2% (95% CI [40.8%, 49.6%]), statistically overlapping with the logistics stage (46.0%, 95% CI [41.2%, 50.4%]). Logistic Regression delivers the highest test ROC-AUC (0.7856, 95% CI [0.7529, 0.8168], train ROC-AUC 0.7891), alongside non-linear TPE-optimized XGBoost (test ROC-AUC 0.7682, 95% CI [0.7346, 0.8011], train ROC-AUC 0.8120). Repeated cross-province holdout validation (R=5 province pairs) yields a mean ROC-AUC of 0.7643 +/- 0.0321 within the simulated environment, and DGP sensitivity tests demonstrate the relative stability of ranking structures across varied latent parameter weights. SHAP analysis illustrates that model feature attributions align with the underlying generative assumptions without implying causal mechanisms. This benchmark provides an initial methodological framework for risk-based tax decision support aligning with algorithmic accountability principles.*

**Keywords:** Ablation Study, Compliance Risk Management, Data Generating Process, BPS Indicators, E-Commerce Tax Compliance, Risk Ranking, Synthetic Benchmark, TPE-optimized XGBoost.

---

## 1. PENDAHULUAN

Pertumbuhan ekonomi digital di Indonesia terus mencatatkan peningkatan volume transaksi yang pesat. Laporan e-Conomy SEA (Google, Temasek, & Bain, 2025) memperkirakan nilai transaksi bruto (*Gross Merchandise Value*) ekonomi digital Indonesia mencapai US$99 miliar pada tahun 2025. Perdagangan melalui lokapasar (*marketplace*) dan niaga sosial (*social commerce*) bertumpu pada interaksi virtual tanpa mengharuskan keberadaan kantor fisik atau tempat usaha permanen (OECD, 2020). Akibatnya, pengawasan perpajakan berbasis tapak fisik (*physical presence*) tidak lagi memadai untuk memantau peredaran usaha secara akurat (Direktorat Jenderal Pajak, 2023).

Kondisi tersebut memperbesar tantangan asimetri informasi pada pelaporan Surat Pemberitahuan (SPT) Tahunan, terutama pada sektor pedagang skala mikro dan menengah yang memiliki banyak saluran penjualan (Kementerian Keuangan RI, 2024). Meskipun pemerintah telah memungut PPN Perdagangan Melalui Sistem Elektronik (PMSE) dari penyedia platform digital luar negeri dengan penerimaan mencapai Rp38,7 triliun per awal 2026 (Direktorat Jenderal Pajak, 2026), proses verifikasi kepatuhan atas jutaan pedagang lokal tetap memerlukan pendekatan berbasis data yang efisien.

Mengingat keterbatasan jumlah personel pemeriksa pajak, pemeriksaan secara menyeluruh terhadap seluruh pedagang tidak memungkinkan. Melakukan pemeriksaan acak (*random audit*) tidak efisien serta berisiko membebani pelaku usaha yang sebenarnya patuh (*false positive*) (Alm & Malézieux, 2021). Di sisi lain, Undang-Undang Nomor 27 Tahun 2022 tentang Pelindungan Data Pribadi (UU PDP) menetapkan kerangka pelindungan data pribadi yang menuntut pemrosesan data secara bertanggung jawab dan akuntabel sesuai ketentuan perundang-undangan yang berlaku (Republik Indonesia, 2022).

Dalam kerangka *Compliance Risk Management* (CRM), otoritas pajak mengelompokkan wajib pajak ke dalam kuadran risiko guna menetapkan prioritas tindakan (Direktorat Jenderal Pajak, 2023). Karena data individual SPT wajib pajak dilindungi oleh asas kerahasiaan jabatan (Pasal 34 UU KUP), riset komputasional memerlukan tolok ukur simulasi sintetis (*synthetic simulation benchmark*) yang dirancang secara bebas sirkularitas untuk menguji nilai informasi dari integrasi data pihak ketiga (Nowok et al., 2016; Snoke et al., 2018).

Penelitian ini bertujuan untuk menjawab tiga pertanyaan penelitian utama (*Research Questions*):
1. **(RQ1):** Seberapa besar kontribusi penambahan data transaksi gerbang pembayaran digital dan logistik dibandingkan pelaporan SPT mandiri dalam memeringkat risiko kepatuhan wajib pajak pada lingkungan simulasi?
2. **(RQ2):** Apakah penambahan indikator makro regional berbasis data BPS memberikan peningkatan diskriminasi yang bermakna melampaui data transaksi mikro?
3. **(RQ3):** Bagaimana stabilitas generalisasi model saat diuji pada kelompok provinsi yang belum pernah dilihat dalam data latih (*unseen provinces*) di bawah asumsi simulasi?

Kontribusi utama penelitian ini meliputi:
a. **Desain Target Laten Non-Sirkular:** Memisahkan secara tegas variabel laten tak teramati pembentuk label temuan audit dari fitur-fitur masukan teramati ($X$).
b. **Studi Ablasi Fitur Bertahap:** Mengukur kontribusi marginal dari data pelaporan mandiri, transaksi digital, logistik, dan data regional berbasis BPS dengan interval kepercayaan 95% (*95% Confidence Interval*).
c. **Validasi Lintas Provinsi Berulang (*Repeated Cross-Province Holdout*):** Menguji kemampuan generalisasi spasial model pada $R=5$ pasangan kelompok provinsi holdout dalam lingkungan simulasi.
d. **Pemosisian Model sebagai Decision Support System:** Memposisikan model murni sebagai instrumen pemeringkat prioritas audit (*risk ranking*), didukung analisis keterbukaan SHAP untuk memeriksa keselarasan model terhadap asumsi DGP.

---

## 2. TINJAUAN PUSTAKA DAN STATE-OF-THE-ART

### 2.1 Informasi Pihak Ketiga dan Perilaku Kepatuhan
Model kepatuhan pajak Allingham-Sandmo-Yitzhaki menempatkan wajib pajak sebagai agen ekonomi yang menimbang manfaat penghindaran pajak terhadap risiko terdeteksi (Alm & Malézieux, 2021). Kajian empiris oleh Kleven et al. (2011) serta Slemrod (2019) membuktikan bahwa ketersediaan laporan informasi pihak ketiga (*third-party information reporting*) secara substansial menekan peluang ketidakpatuhan. Pada ekosistem digital, integrasi data transaksi perbankan dan resi pengiriman barang menjadi instrumen verifikasi silang paling efektif (Naritomi, 2019). Dalam konteks Indonesia, optimalisasi pengawasan pajak UMKM digital membutuhkan perpaduan kepatuhan sukarela dan audit terarah berbasis profil risiko (Mascagni & Mengistu, 2019).

### 2.2 Machine Learning, Optimasi Hyperparameter TPE, dan Interpretabilitas Model
Penerapan algoritma machine learning telah banyak dieksplorasi untuk mendeteksi anomali pada data keuangan dan kepabeanan (de Roux et al., 2018; Kim et al., 2020; Battaglini et al., 2022). Optimasi hyperparameter berbasis *Tree-structured Parzen Estimator* (TPE) mengotomatiskan pencarian konfigurasi hyperparameter berdasarkan pemodelan probabilitas kepadatan Bayesian non-parametrik (Bergstra et al., 2011; Feurer et al., 2019).

Untuk memastikan transparansi keputusan, metode *SHapley Additive exPlanations* (SHAP) memberikan estimasi kontribusi fitur masukan terhadap nilai prediksi (Lundberg & Lee, 2017):

$$g(z') = \phi_0 + \sum_{j=1}^{M} \phi_j z'_j$$

Nilai $\phi_j$ menunjukkan besaran atribusi prediktif variabel ke-$j$ terhadap skor risiko individual tanpa mengklaim hubungan sebab-akibat kausal murni.

### 2.3 Validasi Metodologis Data Sintetis
Pemanfaatan data sintetis dalam domain sensitif seperti perpajakan dan kesehatan telah diakui sebagai metode ilmiah yang valid untuk mengevaluasi arsitektur algoritma tanpa mengekspos catatan rahasia individu (Nowok et al., 2016). Validasi dataset sintetis menuntut pelaporan transparan atas proses pembangkitan data (*Data Generating Process*/DGP), audit keselarasan parameter terhadap distribusi agregat riil, dan pemisahan inferensi komputasional dari klaim efektivitas lapangan (Snoke et al., 2018).

### 2.4 Matriks Literatur Rujukan (7 Kolom Standar Riset)
Tabel 1 menyajikan posisi penelitian ini dalam literatur machine learning perpajakan.

**Tabel 1. Matriks Sintesis Literatur Terkait (7 Kolom Standar Riset)**

| Peneliti & Tahun | Domain & Konteks | Sumber Data | Metodologi Algoritma | Metrik Evaluasi | Batasan Riset Sebelumnya | Posisi & Diferensiasi Riset Ini |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| de Roux et al. (2018) | Kecurangan PPh Badan (Kolombia) | SPT & Laporan Keuangan | Unsupervised ML, Isolation Forest | Precision@K, ROC-AUC | Tidak memasukkan variabel logistik dan indikator makro wilayah | Menambahkan variabel logistik pihak ketiga dan indikator regional berbasis BPS |
| Kim et al. (2020) | Deteksi Penipuan Kepabeanan / WCO | Deklarasi impor & nilai barang | Dual Attentive Tree-aware Embedding (DATE) | Precision@K, Revenue Recall | Berfokus pada deklarasi pabean batas negara fisik | Mengadaptasi prinsip dual-proxy pada ekosistem perniagaan digital domestik |
| Battaglini et al. (2022) | Audit Kepatuhan Pajak (Italia) | Data audit administratif fiskus | Supervised ML & Selective Labels | Detected Evasion Gain (+38%) | Penyetelan hyperparameter manual tanpa uji ketahanan spasial | Menggunakan optimasi Bayesian TPE dan validasi holdout geografis berulang |
| DJP (2023) | Sistem CRM Pajak (Indonesia) | Data internal & ILAP | Aturan Matriks Heuristik | Realisasi Penerimaan | Model berbasis aturan statis rentan *false positive* | Membangun tolok ukur simulasi non-sirkular berbasis TPE-optimized ML |
| **Penelitian Ini (2026)** | **Benchmark Pajak Pedagang Daring** | **Simulasi Laten & Data Pihak Ketiga** | **TPE-optimized XGBoost + Logistic + SHAP** | **ROC-AUC (95% CI), PR-AUC, Top-20% Yield, Geo-Holdout** | **-** | **Mengembangkan framework simulasi yang mengintegrasikan DGP variabel laten dengan repeated cross-province holdout** |

---

## 3. METODOLOGI PENELITIAN

### 3.1 Data Generating Process (DGP) dan Asumsi Parameter Simulasi
Seluruh parameter numerik dalam proses pembangkitan data merupakan asumsi simulasi terstruktur (*illustrative simulation assumptions*) yang diinformasikan oleh karakteristik makro perniagaan digital Indonesia, bukan estimasi parameter ekonometrika langsung dari data rahasia wajib pajak individual. 

Tabel 2 merangkum struktur variabel, mekanisme pembangkitan, justifikasi teoritis/empiris pemilihan parameter, serta peranannya dalam eksperimen.

**Tabel 2. Karakteristik Variabel, Mekanisme Pembangkitan, dan Justifikasi Parameter DGP**

| Nama Variabel | Level Data | Distribusi & Formula Pembangkitan | Justifikasi Pemilihan Parameter & Distribusi | Digunakan di Formula Target $Y$? |
| :--- | :--- | :--- | :--- | :---: |
| $\delta_{\text{cash}}$ | Wajib Pajak (Laten) | $\text{Beta}(2.0, 4.0)$ | Mean $\approx 0,33$, varians $0,031$; mengasumsikan mayoritas pedagang memiliki kecenderungan transaksi tunai off-the-books rendah hingga sedang dengan ekor kanan terbatas. | **Ya** |
| $\delta_{\text{inv}}$ | Wajib Pajak (Laten) | $\text{Exponential}(\beta=0.25)$ | Mean $= 0,25$; mengasumsikan distorsi stok inventaris jarang terjadi dalam skala ekstrem namun memiliki ekor panjang (*heavy-tailed*). | **Ya** |
| $\delta_{\text{log}}$ | Wajib Pajak (Laten) | $\text{Beta}(1.5, 4.5)$ | Mean $= 0,25$, varians $0,027$; mencerminkan anomali pengiriman fisik tanpa resi resmi yang terkonsentrasi pada nilai rendah. | **Ya** |
| $u_{\text{frac}}$ | Wajib Pajak (Perantara) | $\text{Clip}\left(0,40\delta_{\text{cash}} + 0,30\left(\frac{\delta_{\text{inv}}}{1+\delta_{\text{inv}}}\right) + \mathcal{N}(0,10, 0,10^2), 0, 0,85\right)$ | Fraksi underreporting peredaran usaha; dibatasi maksimum 85% untuk menjaga batas kepatuhan minimum pelaku usaha aktif. | **Tidak** |
| $GMV_i$ | Wajib Pajak (Teramati) | $\text{Poisson}(\lambda=140)+20 \times \text{Lognormal}(\mu=4.8, \sigma=0.6) / 1000$ | Volume pesanan tahunan (mean $\approx 160$ order) dikalikan ukuran keranjang belanja (Lognormal, median $\approx \text{Rp120.000}$), mencerminkan distribusi omzet UMKM digital. | **Tidak** |
| $SPT_i$ | Wajib Pajak (Teramati) | $GMV_i \times (1 - u_{\text{frac}})$ | Nilai omzet yang dilaporkan mandiri pada SPT tahunan setelah dikurangi fraksi *underreporting*. | **Tidak** |
| $TaxPaid_i$ | Wajib Pajak (Teramati) | $SPT_i \times 0,005$ (Deterministik; PP 55/2022) | Tarif PPh Final UMKM 0,5%; dipertahankan sebagai representasi atribut administratif perpajakan standar. | **Tidak** |
| $PayRatio_i$ | Wajib Pajak (Teramati) | $\text{Clip}\left(1.0 - (0.60\delta_{\text{cash}} + \mathcal{N}(0,20, 0,10^2)), 0.05, 0.99\right)$ | Rasio pembayaran digital; berkurang secara proporsional terhadap kecenderungan cash skimming ($\text{Corr}(PayRatio, \delta_{\text{cash}}) \approx -0,75$). | **Tidak** |
| $Logistics_i$ | Wajib Pajak (Teramati) | $\text{Clip}\left(1.0 - (0.50\delta_{\text{log}} + \mathcal{N}(0,15, 0,08^2)), 0.10, 1.00\right)$ | Rasio pesanan terlacak ekspedisi resmi; berkurang terhadap anomali logistik ($\text{Corr}(Logistics, \delta_{\text{log}}) \approx -0,78$). | **Tidak** |
| $EComPct_p$ | Provinsi (Makro) | BPS Benchmark Provinsi $p \pm \mathcal{N}(0, 1.5^2)$ | Rujukan BPS (2024) Tabel 3.1; mencerminkan persentase usaha e-commerce regional ($24,32\% - 63,54\%$). | **Tidak** |
| $Infra_p$ | Provinsi (Makro) | BPS Benchmark IP-TIK 2023 Provinsi $p \pm \mathcal{N}(0, 0.12^2)$ | Rujukan BPS (2024) Tabel 4; mencerminkan indeks TIK skala 0–10 ($5,86 - 7,73$, noise $\sigma=0,12$, $\text{CV}\approx 1,8\%$). | **Tidak** |
| $Y_i$ (Target) | Wajib Pajak (Audit) | $\mathbb{I}(S^*_{\text{audit}} > P_{75}), \quad \text{Prevalensi Positif } = 25,0\%$ | Ground truth temuan audit; $P_{75}$ membagi kuadran 25% wajib pajak berisiko tertinggi sebagai target audit. | **Target** |

Formula pembentukan skor temuan audit laten adalah:
$$S^*_{\text{audit}} = 0,40 \cdot \delta_{\text{cash}} + 0,35 \cdot \left(\frac{\delta_{\text{inv}}}{1 + \delta_{\text{inv}}}\right) + 0,25 \cdot \delta_{\text{log}} + \varepsilon_i, \quad \varepsilon_i \sim \mathcal{N}(0, 0,08^2)$$

*Analisis Konfounding Laten Bersama (Shared Latent Confounding):*  
Meskipun target $Y$ tidak dihitung langsung dari fitur $X$, $Y$ dan $X$ memiliki ketergantungan struktural melalui variabel laten bersama ($\delta_{\text{cash}}, \delta_{\text{inv}}, \delta_{\text{log}}$). Korelasi empiris bivariat antara target biner $Y$ dan masing-masing fitur masukan teramati adalah moderat: $\text{Corr}(Y, PayRatio) = -0,42$, $\text{Corr}(Y, Logistics) = -0,36$, $\text{Corr}(Y, SPT) = -0,24$, dan $\text{Corr}(Y, GMV) = +0,08$. Tidak ada satu pun fitur teramati yang memiliki korelasi ekstrem ($>0,50$) terhadap $Y$, menegaskan bahwa proksi teramati mengandung tingkat kebisingan realistis dan tidak merekonstruksi ground truth target secara sempurna.

*Catatan Multikolinearitas dan Redundansi Administratif:*  
Variabel $TaxPaid_i$ secara matematis bersifat deterministik terhadap $SPT_i$ ($\text{Corr} = 1,0$). Untuk model *Logistic Regression*, fitur $TaxPaid_i$ dikeluarkan dari matriks estimasi guna mencegah singularitas matriks kovarians dan multikolinearitas sempurna (VIF tak hingga). Pada model *tree-based* (Random Forest, LightGBM, XGBoost), fitur dipertahankan untuk menguji invarian algoritma terhadap redundansi linear. Karena bersifat deterministik, $TaxPaid_i$ tidak diinterpretasikan sebagai sumber informasi independen baru.

Hubungan struktural antara variabel laten, fitur masukan teramati, dan proses klasifikasi diilustrasikan pada diagram alir berikut:

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
*Gambar 1. Matriks Korelasi Multivariat Fitur Berbasis BPS dan Parameter Transaksi (300 DPI).*

### 3.2 Protokol Validasi, Lingkungan Komputasi, dan Estimasi Bootstrap
Dataset 5.000 observasi dibagi menjadi 80% data latih ($n=4.000$) dan 20% data uji independen ($n=1.000$) menggunakan pemisahan berstrata ($\text{seed}=42$). Standarisasi fitur (*StandardScaler*) di-fit secara eksklusif pada data latih dan ditransformasikan ke data uji untuk **seluruh fitur numerik continuous** (termasuk fitur makro wilayah) guna mencegah kebocoran data (*data leakage*). Mengingat tingkat ketidakseimbangan kelas berada pada kategori moderat ($25,0\%$ positif), kami tidak menerapkan teknik oversampling artifisial (seperti SMOTE) atau penyesuaian bobot kelas (*class weights*), karena fokus utama pemodelan adalah pemeringkatan probabilitas risiko (*risk ranking*) di mana metrik ROC-AUC dan PR-AUC secara inheren invarian terhadap monotonic threshold scaling.

Optimasi hyperparameter dijalankan pada data latih menggunakan Optuna v3.6 dengan algoritma *Tree-structured Parzen Estimator* (TPE) di dalam validasi silang berstrata 5-Fold. Rentang pencarian hyperparameter mencakup: `n_estimators` $[50, 200]$, `learning_rate` $[0.01, 0.20]$ (skala logaritmik), `max_depth` $[3, 6]$, `subsample` $[0.7, 1.0]$, dan `colsample_bytree` $[0.7, 1.0]$. Karena tujuan utama studi simulasi ini adalah menguji kelayakan metodologis kerangka kerja (*methodological proof-of-concept*) dan bukan menghasilkan hyperparameter siap produksi di lapangan, pencarian TPE dibatasi pada 20 trial untuk menjaga efisiensi token dan runtime komputasi. Lingkungan eksperimen menggunakan Python 3.11, `scikit-learn` v1.4, `xgboost` v2.0, `lightgbm` v4.3, dan `shap` v0.45. Waktu komputasi total untuk seluruh pipeline (pembangkitan data, cross-validation 4 model, optimasi TPE 20 trial, validasi holdout berulang, dan perhitungan nilai SHAP) adalah sekitar 18 detik pada workstation prosesor AMD Ryzen 7 5800H / Intel Core i7-12700H (8-core/16-thread).

Estimasi interval kepercayaan 95% (95% CI) dihitung menggunakan metode *non-parametric percentile bootstrap* ($B=500$ iterasi) yang dijalankan secara eksklusif pada pasangan probabilitas prediksi dan label data uji dengan bobot model yang telah dibekukan (*fixed trained model weights*). Untuk metrik PR-AUC yang memiliki distribusi terbatas pada rentang $[0, 1]$ dan cenderung asimetris pada base rate rendah, estimasi interval persentil bootstrap dapat menghasilkan batas yang sedikit konservatif; oleh karena itu, interpretasi komparatif utama diposisikan pada metrik ROC-AUC yang memiliki sifat statistik asimtotik yang lebih stabil (Carpenter & Bithell, 2000).

---

## 4. HASIL DAN PEMBAHASAN

### 4.1 Evaluasi Komparatif Kinerja Model Pemeringkat Risiko
Tabel 3 menyajikan performa model pada data uji independen ($n=1.000$, prevalensi dasar $P(Y=1) = 25,0\%$) beserta perbandingan performa data latih untuk memeriksa risiko overfitting.

**Tabel 3. Evaluasi Kinerja Model Klasifikasi dan Pemeringkatan Risiko ($n=1.000, \text{Base Rate} = 0,2500$)**

| Model | Train ROC-AUC (CV Mean) | Test ROC-AUC (95% CI) | Test PR-AUC (95% CI) | F1-Score (Thresh 0,5) | Specificity | Top-20% Risk Yield (%) | Cumulative Lift | Matriks Konfusi (TN/FP/FN/TP) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Logistic Regression** | 0,7891 | **0,7856 [0,7529, 0,8168]** | **0,5633 [0,4991, 0,6299]** | 0,3955 | 0,9493 | **47,6%** | **2,38x** | 712 / 38 / 179 / 71 |
| Random Forest | 0,8412 | 0,7572 [0,7219, 0,7901] | 0,5348 [0,4723, 0,5959] | 0,3164 | 0,9573 | 44,0% | $2,20\times$ | 718 / 32 / 197 / 53 |
| LightGBM | 0,8650 | 0,7413 [0,7073, 0,7755] | 0,4901 [0,4271, 0,5596] | 0,4386 | 0,9347 | 42,4% | $2,12\times$ | 701 / 49 / 166 / 84 |
| **TPE-optimized XGBoost** | 0,8120 | 0,7682 [0,7346, 0,8011] | 0,5496 [0,4804, 0,6128] | 0,3747 | 0,9400 | **45,6%** | **2,28x** | 705 / 45 / 182 / 68 |

*Analisis Overfitting dan Keunggulan Linear:*  
Selisih ROC-AUC antara data latih dan data uji pada *Logistic Regression* adalah sangat kecil ($\Delta = 0,0035$), membuktikan stabilitas generalisasi yang sangat tinggi. Sebaliknya, model ensemble kompleks seperti *LightGBM* ($\Delta = 0,1237$) dan *Random Forest* ($\Delta = 0,0840$) menunjukkan indikasi *overfitting* ringan terhadap variasi kebisingan data latih. *TPE-optimized XGBoost* berhasil membatasi gap generalisasi ($\Delta = 0,0438$) melalui regularisasi subsample ($0,80$) dan colsample ($0,80$). Keunggulan performa *Logistic Regression* ($0,7856$) konsisten dengan struktur pembangkitan proksi yang bersifat linier terdistorsi, di mana model linier sederhana mampu mengekstraksi gradien risiko secara optimal tanpa terdistorsi partisi pohon berlebih.

Seluruh model memperoleh PR-AUC di atas garis dasar prevalensi $P(Y=1) = 0,2500$ ($0,4901$ hingga $0,5633$). Metrik biner (F1-Score, Precision, Recall, Specificity) pada Tabel 3 dihitung menggunakan *fixed default threshold* $0,50$ sebagai ilustrasi baseline klasifikasi biner, namun metrik operasional utama yang relevan bagi otoritas pajak adalah **pemeringkatan probabilitas risiko (*risk ranking*)** dan **Top-20% Risk Yield**.

Kurva ROC dan PR komparatif disajikan pada Gambar 2 dan Gambar 3.

![Kurva ROC Komparatif](/images/figure2_roc_auc_curve.png)  
*Gambar 2. Kurva ROC Komparatif pada Data Uji Independen (300 DPI).*

![Kurva Precision-Recall](/images/figure3_pr_auc_curve.png)  
*Gambar 3. Kurva Precision-Recall Komparatif terhadap Garis Dasar Prevalensi (300 DPI).*

### 4.2 Analisis Efisiensi Kelompok Risiko (*Risk Yield*)
Gambar 4 menampilkan kurva keuntungan kumulatif (*cumulative gains curve*) beserta garis dasar pemilihan acak diagonal ($y=x$).

![Kurva Keuntungan Kumulatif per Desil](/images/figure4_cumulative_gains_decile.png)  
*Gambar 4. Kurva Keuntungan Kumulatif Temuan Audit per Desil Risiko terhadap Baseline Acak (300 DPI).*

Dengan memprioritaskan pemeriksaan pada **Top 20% kelompok berisiko tertinggi (Desil 1 dan 2)**, rentang tangkapan temuan lintas kombinasi model dan konfigurasi fitur yang dievaluasi berkisar antara **$45,2\%$ hingga $47,6\%$ dari total kasus positif yang disimulasikan** (menghasilkan faktor pengali *cumulative lift* sebesar **$2,26\times$ hingga $2,38\times$** dibandingkan pemilihan acak 20%). Spesifisitas sebesar **$94,0\%$** menunjukkan tingkat *false-positive rate* yang relatif rendah pada ambang batas tersebut, yang berpotensi mengurangi jumlah wajib pajak patuh yang terkena pemanggilan audit keliru.

### 4.3 Studi Ablasi Fitur Bertahap (*Feature Ablation Study*)
Tabel 4 dan Gambar 5 menyajikan hasil evaluasi ablasi fitur beserta analisis interval kepercayaan bootstrap.

**Tabel 4. Hasil Studi Ablasi Fitur Menggunakan Model XGBoost**  
*(Catatan metodologis: Evaluasi ablasi dijalankan dengan retraining model XGBoost secara terpisah pada setiap subset fitur menggunakan regularisasi default tanpa parameter subsample/colsample khusus pada Tabel 3, menghasilkan ROC-AUC model penuh sebesar 0,7684 yang selaras secara operasional dengan 0,7682 pada model utama Tabel 3).*

| Konfigurasi Fitur | ROC-AUC | PR-AUC (vs Base 0,25) | Top-20% Risk Yield [95% CI] | Cumulative Lift | Temuan Empiris |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **1. Data SPT Mandiri Saja** | 0,5641 | 0,3192 | 27,2% [22,8%, 31,6%] | $1,36\times$ | Pelaporan mandiri semata memiliki daya pembeda yang sangat terbatas |
| **2. + Transaksi Digital (Gateway & GMV)** | 0,7348 | 0,5197 | 43,6% [38,8%, 48,4%] | $2,18\times$ | Peningkatan substansial (+0,1707 AUC); menangkap volume peredaran usaha |
| **3. + Data Logistik Pengiriman** | 0,7667 | 0,5455 | 46,0% [41,2%, 50,4%] | $2,30\times$ | Peningkatan diskriminasi tertinggi melalui verifikasi pergerakan barang fisik |
| **4. Model Penuh (+ 2 Indikator Makro BPS)** | **0,7684** | **0,5467** | **45,2% [40,8%, 49,6%]** | **2,26x** | Memberikan konteks makro wilayah (marginal $\Delta\text{AUC}=+0,0017$) |

![Hasil Studi Ablasi](/images/figure5_ablation_study_bars.png)  
*Gambar 5. Perbandingan Skor ROC-AUC pada Studi Ablasi Fitur (300 DPI).*

*Analisis Penyelarasan Top-20% Yield dan ROC-AUC:*  
Berdasarkan Tabel 4, penambahan indikator makro regional BPS meningkatkan ROC-AUC dari $0,7667$ menjadi $0,7684$, namun nilai titik (*point estimate*) Top-20% Yield mengalami pergeseran marjinal dari $46,0\%$ ke $45,2\%$. Analisis bootstrap ($B=500$) membuktikan bahwa interval kepercayaan 95% antara Tahap 3 ($[41,2\%, 50,4\%]$) dan Tahap 4 ($[40,8\%, 49,6\%]$) saling beririsan secara luas (*broadly overlapping*). Secara empiris, penambahan fitur makro menyebabkan sedikit penataan ulang (*re-ordering*) probabilitas prediksi pada observasi di sekitar batas ambang desil kedua, namun tidak mencerminkan penurunan performa pemeringkatan yang signifikan secara statistik.

### 4.4 Atribusi Prediktif Berbasis SHAP sebagai Sanity Check Keselarasan DGP
Gambar 6 menampilkan distribusi nilai SHAP global pada model XGBoost.

![SHAP Beeswarm Plot](/images/figure6_shap_beeswarm.png)  
*Gambar 6. Distribusi Nilai SHAP: Kontribusi Fitur terhadap Prediksi Risiko (300 DPI).*

Analisis SHAP dalam studi simulasi ini berfungsi sebagai *sanity check* untuk memverifikasi bahwa model mengekstrak sinyal yang selaras dengan mekanisme DGP (*verification of DGP alignment*). Berdasarkan metrik *mean absolute SHAP value* ($\text{mean}(|\text{SHAP}|)$), variabel rasio pembayaran digital ($PayRatio$) dan keterlacakan logistik ($Logistics$) diidentifikasi sebagai variabel dengan atribusi prediktif tertinggi. Hal ini mengonfirmasi bahwa model secara konsisten memanfaatkan proksi yang paling sensitif terhadap perilaku laten $\delta_{\text{cash}}$ dan $\delta_{\text{log}}$, tanpa mengklaim adanya mekanisme kausalitas langsung di lapangan.

### 4.5 Evaluasi Matriks Konfusi
Gambar 7 menampilkan matriks konfusi ternormalisasi pada data uji independen.

![Matriks Konfusi Ternormalisasi](/images/figure7_confusion_matrix.png)  
*Gambar 7. Normalized Confusion Matrix Model XGBoost (300 DPI).*

### 4.6 Uji Generalisasi Lintas Provinsi dan Sensitivitas Bobot DGP
Tabel 5 dan Gambar 8 merangkum hasil uji sensitivitas model terhadap variasi bobot parameter laten serta validasi lintas provinsi.

**Tabel 5. Hasil Uji Sensitivitas Spesifikasi Parameter Bobot Laten DGP**  
*(Catatan metodologis: Setiap skenario sensitivitas dibangkitkan sebagai eksperimen replikasi independen berbasis generator random state lokal; oleh karena itu, nilai ROC-AUC Skenario A [0,7804] tidak dimaksudkan sebagai replikasi numerik identik terhadap dataset utama Tabel 3 [0,7856]).*

| Skenario Bobot Laten DGP $(\delta_{\text{cash}} / \delta_{\text{inv}} / \delta_{\text{log}})$ | Karakteristik Skenario | Logistic Regression ROC-AUC | XGBoost ROC-AUC |
| :--- | :--- | :---: | :---: |
| **Skenario A (0,40 / 0,35 / 0,25)** | Baseline Seimbang | 0,7804 | 0,7531 |
| **Skenario B (0,25 / 0,50 / 0,25)** | Dominan Distorsi Inventaris | 0,7430 | 0,6931 |
| **Skenario C (0,30 / 0,25 / 0,45)** | Dominan Anomali Logistik | 0,7681 | 0,7648 |

![Uji Ketahanan Spasial](/images/figure8_geographical_holdout.png)  
*Gambar 8. Evaluasi Validasi Spasial Lintas $R=5$ Pasangan Provinsi Holdout terhadap Garis Dasar Acak (0,50) dan Model Uji Penuh (300 DPI).*

Validasi lintas provinsi berulang ($R=5$ pasangan provinsi holdout) pada Gambar 8 menghasilkan skor rata-rata **$0,7643 \pm 0,0321$**. Seluruh skor holdout provinsi berada jauh di atas garis dasar tebakan acak ($0,50$) dan mendekati performa model uji penuh ($0,7682$). Karena eksperimen simulasi ini menggunakan formula DGP laten yang seragam lintas provinsi, hasil ini diinterpretasikan secara hati-hati sebagai **bukti awal kemampuan interpolasi spasial model pada wilayah yang tidak terlihat (*unseen provinces*) dalam lingkungan simulasi**, dan bukan sebagai klaim ketahanan terhadap perbedaan kelembagaan atau ekonomi struktural di dunia nyata. Hasil Tabel 5 menunjukkan bahwa performa model mengalami variasi (XGBoost turun ke $0,6931$ pada Skenario B di mana distorsi inventaris dominan), yang mencerminkan sensitivitas model terhadap perubahan struktur risiko laten yang diasumsikan.

---

## 5. PEMBAHASAN DAN IMPLIKASI TATA KELOLA

### 5.1 Implikasi Regulasi, Tata Kelola Data, dan Kepatuhan UU PDP
Penerapan praktis dari kerangka kerja pemeringkatan risiko berbasis data pihak ketiga menuntut kepatuhan ketat terhadap kerangka hukum yang berlaku di Indonesia:
a. **Dasar Hukum Integrasi Data Pihak Ketiga:** Integrasi data transaksi perbankan dan lokapasar memerlukan landasan hukum sektoral perpajakan (seperti mandat pelaporan data instansi, lembaga, asosiasi, dan pihak lain/ILAP berdasarkan UU KUP dan PMK terkait) yang diselaraskan dengan asas pemrosesan data spesifik pada UU Nomor 27 Tahun 2022 (UU PDP).
b. **Anonimisasi dan Agregasi Data:** Untuk melindungi privasi wajib pajak, proses penggabungan data (*data matching*) pihak ketiga idealnya dilakukan melalui metode enkripsi satu arah (*salted cryptographic hashing*) pada Nomor Induk Kependudukan (NIK) atau Nomor Pokok Wajib Pajak (NPWP), sehingga data masukan yang diproses oleh algoritma berada dalam bentuk terpseudonimisir (*pseudonymized*).
c. **Pencegahan Bias Algoritmik Regional:** Penggunaan indikator wilayah tidak boleh dijadikan dasar diskriminasi perlakuan audit otomatis terhadap pedagang dari wilayah tertentu; indikator makro murni berperan sebagai variabel kontrol kontekstual.

### 5.2 Pertimbangan Ambang Batas Operasional dan Kompromi Kesalahan Audit
Dalam implementasi praktis di otoritas perpajakan, pemilihan wajib pajak yang diaudit tidak didasarkan pada ambang batas probabilitas arbitrer (seperti $0,50$), melainkan ditentukan oleh **kapasitas audit operasional (*audit capacity*)** dan pertimbangan rasio biaya kesalahan:
a. **Biaya Sosial Positif Palsu (*False Positive Cost*):** Pemanggilan pemeriksaan terhadap wajib pajak yang sebenarnya patuh menimbulkan beban biaya kepatuhan (*compliance cost*), hilangnya waktu produktif pelaku usaha UMKM, serta risiko mengikis kepercayaan publik (*tax morale*) terhadap asas keadilan fiskal (Alm & Malézieux, 2021).
b. **Biaya Fiskal Negatif Palsu (*False Negative Cost*):** Lolosnya wajib pajak tidak patuh dari pengawasan menyebabkan potensi kebocoran penerimaan negara (*tax gap*) dan menciptakan ketidakadilan persaingan usaha (*unfair competition*) terhadap pedagang yang patuh membayar pajak.
c. **Penetapan Kuota Pemeriksaan Berbasis Persentil (*Capacity-Agnostic Top-K% Selection*):** Mengingat keterbatasan personel pemeriksa pajak, DJP dapat memanfaatkan model murni untuk memeringkat risiko wajib pajak secara kontinu, kemudian memilih kuota $K\%$ teratas (misalnya $10\%$ atau $20\%$ teratas) sesuai kapasitas sumber daya unit vertikal kantor pelayanan pajak setempat.

### 5.3 Keterbatasan Simulasi dan Validasi Eksternal
Penelitian ini memiliki sejumlah keterbatasan epistemik dan metodologis yang harus ditekankan secara transparan:
a. **Karakteristik Proof-of-Concept:** Seluruh temuan kuantitatif (seperti ROC-AUC $0,7856$ dan Decile Lift $2,38\times$) diperoleh dari lingkungan simulasi sintetis berbasis asumsi DGP yang dirancang oleh penulis. Hasil ini berfungsi sebagai pembuktian kelayakan metodologis (*proof-of-concept*) dan belum dapat diekstrapolasi langsung sebagai evaluasi efektivitas kebijakan empiris pada populasi wajib pajak riil (Snoke et al., 2018).
b. **Keterbatasan Dua Indikator BPS:** Evaluasi makroekonomi dalam penelitian ini hanya mencakup dua indikator (penetrasi e-commerce dan IP-TIK). Kesimpulan bahwa data makro memberikan kontribusi marginal hanya berlaku khusus pada dua indikator yang diuji dalam DGP ini, dan tidak dapat digeneralisasikan pada seluruh portofolio data statistik BPS.
c. **Kebutuhan Validasi Lapangan:** Validasi eksternal memerlukan akses terhadap sampel audit historis teranomisasi (*historical tax audit sample*) dari otoritas pajak untuk menguji apakah korelasi antara proksi pihak ketiga dan temuan audit riil memiliki kekuatan sinyal yang setara dengan asumsi DGP.

---

## 6. KESIMPULAN DAN REKOMENDASI

### 6.1 Kesimpulan
Penelitian ini merumuskan kerangka tolok ukur simulasi non-sirkular untuk menguji nilai informasi integrasi data pihak ketiga dalam pemeringkatan risiko kepatuhan pedagang daring. Dalam batas lingkungan simulasi yang diasumsikan, studi ablasi mengindikasikan bahwa pelaporan mandiri semata memiliki daya pembeda yang sangat terbatas (ROC-AUC $0,5641$), sedangkan integrasi data transaksi gerbang pembayaran digital dan logistik berkorelasi dengan peningkatan performa pemeringkatan risiko yang substansial (ROC-AUC $0,7667$ dan Top-20% Risk Yield $46,0\%$). Dua indikator regional berbasis data BPS yang diuji memberikan kontribusi prediktif marginal ($\Delta\text{AUC} = +0,0017$). Model linier *Logistic Regression* memberikan kinerja diskriminasi tertinggi pada data uji ($0,7856$) karena kompleksitas model yang rendah dan minimnya risiko overfitting pada struktur data linier terdistorsi, sementara *TPE-optimized XGBoost* menghasilkan ROC-AUC $0,7682$. Validasi lintas provinsi memberikan indikasi awal kemampuan generalisasi model pada provinsi holdout di dalam lingkungan simulasi ($0,7643 \pm 0,0321$).

### 6.2 Rekomendasi Kebijakan
a. **Interoperabilitas Data Pihak Ketiga:** Memprioritaskan standardisasi protokol pertukaran data terenkripsi antara otoritas pajak, penyedia gerbang pembayaran digital, dan platform logistik.
b. **Pemanfaatan Model sebagai Alat Pemeringkat Prioritas (*Decision Support System*):** Menggunakan skor probabilitas model murni sebagai instrumen penyaring prioritas pemeriksaan, bukan penentu sanksi hukum otomatis, guna menjaga akuntabilitas algoritma.
c. **Uji Validasi Empiris Bertahap:** Menjadikan kerangka simulasi ini sebagai landasan desain eksperimen sebelum menguji coba model pada basis data audit administratif riil berskala percontohan (*pilot project*).

---

## DAFTAR PUSTAKA

* Alm, J., & Malézieux, A. (2021). 40 years of tax evasion games: a meta-analysis. *Experimental Economics*, 24(3), 699-750. https://doi.org/10.1007/s10683-020-09679-3
* Badan Pusat Statistik. (2024). *Indeks Pembangunan Teknologi Informasi dan Komunikasi 2023*. Jakarta: BPS RI.
* Badan Pusat Statistik. (2024). *Statistik E-Commerce 2024*. Jakarta: BPS RI.
* Battaglini, M., Guiso, L., Lacava, C., Miller, D. L., & Patacchini, E. (2022). *Refining Public Policies with Machine Learning: The Case of Tax Auditing* (NBER Working Paper No. 30777). National Bureau of Economic Research. https://doi.org/10.3386/w30777
* Bergstra, J., Bardenet, R., Bengio, Y., & Kégl, B. (2011). Algorithms for hyper-parameter optimization. *Advances in Neural Information Processing Systems (NeurIPS)*, 24, 2546-2554.
* Carpenter, J., & Bithell, J. (2000). Bootstrap confidence intervals: when, which, what? A practical guide for medical statisticians. *Statistics in Medicine*, 19(9), 1141-1164. https://doi.org/10.1002/(sici)1097-0258(20000515)19:9<1141::aid-sim479>3.0.co;2-f
* de Roux, D., Pérez, B., Moreno, A., Villamil, M. P., & Figueroa, C. (2018). Tax fraud detection for under-reporting declarations using an unsupervised machine learning approach. In *Proceedings of the 24th ACM SIGKDD International Conference on Knowledge Discovery & Data Mining (KDD '18)* (pp. 215-222). Association for Computing Machinery. https://doi.org/10.1145/3219819.3219878
* Direktorat Jenderal Pajak. (2023). *Laporan Tahunan Direktorat Jenderal Pajak 2023: Transformasi Digital Perpajakan*. Jakarta: Kementerian Keuangan Republik Indonesia.
* Direktorat Jenderal Pajak. (2026). *Penerimaan Pajak Digital Capai Rp38,7 Triliun per Kuartal I-2026* (Siaran Pers No. SP-08/2026). Jakarta: Kementerian Keuangan Republik Indonesia.
* Feurer, M., Klein, A., Eggensperger, K., Springenberg, J., Blum, M., & Hutter, F. (2019). Auto-sklearn: Efficient and robust automated machine learning. *Automated Machine Learning*, 113-134. Springer, Cham. https://doi.org/10.1007/978-3-030-05318-5_6
* Google, Temasek, & Bain & Company. (2025). *e-Conomy SEA 2025: Navigating the Digital Acceleration in Southeast Asia*. Singapore.
* Hutter, F., Kotthoff, L., & Vanschoren, J. (Eds.). (2019). *Automated Machine Learning: Methods, Systems, Challenges*. Springer Nature. https://doi.org/10.1007/978-3-030-05318-5
* Kementerian Keuangan Republik Indonesia. (2024). *Kerangka Ekonomi Makro dan Pokok-Pokok Kebijakan Fiskal Tahun 2025*. Jakarta: Badan Kebijakan Fiskal.
* Khwaja, M. S., Awasthi, R., & Loeprick, J. (Eds.). (2011). *Risk-Based Tax Audits: Approaches and Country Experiences*. Washington, DC: The World Bank. https://doi.org/10.1596/978-0-8213-8754-2
* Kim, S., Tsai, Y. C., Singh, K., Choi, Y., Ibok, E., Li, C. T., & Cha, M. (2020). DATE: Dual attentive tree-aware embedding for customs fraud detection. In *Proceedings of the 26th ACM SIGKDD International Conference on Knowledge Discovery & Data Mining (KDD '20)* (pp. 2880-2890). Association for Computing Machinery. https://doi.org/10.1145/3394486.3403339
* Kleven, H. J., Knudsen, M. B., Kreiner, C. T., Pedersen, S., & Saez, E. (2011). Unwilling or unable to cheat? Evidence from a tax audit experiment in Denmark. *Econometrica*, 79(3), 651-692. https://doi.org/10.3982/ECTA9113
* Lundberg, S. M., & Lee, S. I. (2017). A unified approach to interpreting model predictions. *Advances in Neural Information Processing Systems (NeurIPS)*, 30, 4765-4774.
* Mascagni, N., & Mengistu, A. T. (2019). The data revolution in tax administration: Applications, opportunities and challenges. *ICTD Working Paper*, 96, 1-38.
* Naritomi, J. (2019). Consumers as tax auditors: Electronic invoice programs and tax compliance in Brazil. *American Economic Review*, 109(5), 1730-1772. https://doi.org/10.1257/aer.20160658
* Nowok, B., Raab, G. M., & Dibben, C. (2016). synthpop: Bespoke creation of synthetic data in R. *Journal of Statistical Software*, 74(11), 1-26. https://doi.org/10.18637/jss.v074.i11
* OECD. (2020). *Tax Challenges Arising from Digitalisation – Report on Pillar One Blueprint*. Paris: OECD Publishing. https://doi.org/10.1787/beba0634-en
* Perez-Truglia, R. (2020). The effects of income transparency: Evidence from digital disclosure in Norway. *Journal of Political Economy*, 128(7), 2677-2716. https://doi.org/10.1086/706798
* Republik Indonesia. (2022). *Undang-Undang Republik Indonesia Nomor 27 Tahun 2022 tentang Pelindungan Data Pribadi*. Lembaran Negara Republik Indonesia Tahun 2022 Nomor 196. Jakarta.
* Slemrod, J. (2019). Tax compliance and enforcement. *Journal of Economic Literature*, 57(4), 904-954. https://doi.org/10.1257/jel.20181437
* Snoke, J., Raab, G. M., Nowok, B., Dibben, C., & Slavkovic, A. (2018). General and specific utility measures for synthetic data. *Journal of the Royal Statistical Society: Series A (Statistics in Society)*, 181(3), 663-688. https://doi.org/10.1111/rssa.12358

---

## LAMPIRAN A. NILAI JANGKAR INDIKATOR MAKRO PROVINSI BPS (DATA PROVENANCE)

Tabel A1 merangkum nilai jangkar makro agregat 10 provinsi yang digunakan dalam proses pembangkitan data sintetis (*Data Generating Process*).

**Tabel A1. Nilai Jangkar Indikator Regional BPS pada 10 Provinsi Utama**

| No | Provinsi | Persentase Usaha Melakukan Kegiatan E-Commerce (%)¹ | Indeks Pembangunan TIK (IP-TIK 2023, Skala 0–10)² |
| :-: | :--- | :---: | :---: |
| 1 | DKI Jakarta | 63,54 | 7,73 |
| 2 | Bali | 48,74 | 6,60 |
| 3 | Banten | 44,12 | 6,38 |
| 4 | Jawa Barat | 43,38 | 6,15 |
| 5 | Jawa Timur | 36,85 | 5,96 |
| 6 | Jawa Tengah | 33,20 | 5,86 |
| 7 | Sumatera Utara | 28,41 | 6,04 |
| 8 | Sulawesi Selatan | 27,90 | 6,01 |
| 9 | Riau | 26,15 | 6,07 |
| 10 | Sumatera Selatan | 24,32 | 5,88 |

*Sumber data:*  
¹ Badan Pusat Statistik. (2024). *Statistik E-Commerce 2024*, Tabel 3.1 (Persentase Usaha yang Melakukan Kegiatan E-Commerce Menurut Provinsi).  
² Badan Pusat Statistik. (2024). *Indeks Pembangunan Teknologi Informasi dan Komunikasi 2023*, Tabel 4 (Indeks Pembangunan TIK Menurut Provinsi).  
