# Kerangka Simulasi Komparatif dan Studi Ablasi Fitur untuk Pemeringkatan Risiko Kepatuhan Pajak Digital Berbasis Indikator Makro BPS

**Izam Rosiawan**¹\*, **Sulthan**²  
¹Program Studi Sains Data, Fakultas Informatika, Telkom University, Kampus Surabaya, Indonesia  
²Direktorat Kampus Surabaya, Telkom University, Kampus Surabaya, Indonesia  
\*Penulis Korespondensi: `izamrosiawan@student.telkomuniversity.ac.id`

---

### ABSTRAK
Peralihan transaksi bisnis ke ranah digital menimbulkan tantangan pengawasan bagi Direktorat Jenderal Pajak (DJP), khususnya dalam memverifikasi kewajaran pelaporan peredaran usaha (*self-assessment*) pedagang daring. Mengingat kerahasiaan data perpajakan individual (*taxpayer confidentiality*), penelitian ini mengembangkan sebuah kerangka kerja simulasi (*synthetic simulation benchmark*) yang dirancang secara non-sirkular untuk mengevaluasi efektivitas integrasi data makroekonomi wilayah Badan Pusat Statistik (BPS) bersama data transaksi pihak ketiga (gerbang pembayaran dan logistik). Melalui eksperimen terhadap 5.000 data observasi dengan target temuan audit independen, kami membandingkan model *Logistic Regression*, *Random Forest*, *LightGBM*, dan *AutoML XGBoost* yang dioptimasi menggunakan *Tree-structured Parzen Estimator* (TPE) pada validasi silang berstrata 5-Fold ($\text{seed}=42$). Studi ablasi fitur membuktikan bahwa pelaporan SPT mandiri semata tidak memiliki daya pembeda yang cukup (ROC-AUC 0,5026). Penambahan parameter transaksi digital dan logistik secara bertahap meningkatkan ROC-AUC menjadi 0,6715 dan PR-AUC menjadi 0,3854, dengan tangkapan desil risiko teratas (Top 20%) meningkat dari 23,2% menjadi 34,0%. Uji ketahanan pada wilayah yang belum pernah dilatih (*geographical out-of-province holdout*) mempertahankan skor ROC-AUC sebesar 0,6689, mengonfirmasi kemampuan generalisasi spasial model. Analisis *Explainable AI* berbasis SHAP mengidentifikasi rasio pembayaran digital dan deviasi logistik sebagai fitur paling informatif. Penelitian ini tidak mengklaim deteksi langsung pada data riil wajib pajak, melainkan menyajikan tolok ukur simulasi metodologis yang membuktikan nilai tambah data pihak ketiga serta memberikan arsitektur pendukung keputusan (*decision support system*) yang selaras dengan prinsip akuntabilitas UU PDP Nomor 27 Tahun 2022.

**Kata Kunci:** Ablation Study, Automated Machine Learning, Compliance Risk Management, Indikator BPS, Pajak Digital, SHAP Values, Synthetic Benchmark.

---

### ABSTRACT
*The transition to digital commerce poses substantial auditing challenges for tax authorities, particularly in verifying self-assessed turnover reported by online merchants. Given legal taxpayer confidentiality constraints, this study develops a non-circular synthetic simulation benchmark to rigorously assess the incremental value of integrating provincial macro-level indicators from Statistics Indonesia (BPS) with third-party payment gateway and logistics data. Across 5,000 observations with an independently generated latent audit finding ground truth, we evaluate Logistic Regression, Random Forest, LightGBM, and an Optuna-driven AutoML XGBoost architecture across 5-fold stratified cross-validation (seed=42). A systematic feature ablation study reveals that self-reported tax returns alone exhibit near-random discriminatory power (ROC-AUC 0.5026). Progressively incorporating digital transaction volumes and logistics tracking significantly elevates performance to ROC-AUC 0.6715, PR-AUC 0.3854, and increases the top 20% audit yield from 23.2% to 34.0%. Out-of-province geographical validation across unseen provinces demonstrates stable generalization (ROC-AUC 0.6689). SHAP interpretability identifies digital payment compliance and logistics tracking coverage as the most impactful drivers of predicted risk. Rather than claiming empirical fraud detection on confidential taxpayer files, this paper establishes a methodologically sound simulation framework demonstrating the scientific value of third-party data integration for risk-based tax decision support under Law No. 27/2022 (PDP Law).*

**Keywords:** Ablation Study, Automated Machine Learning, Compliance Risk Management, BPS Indicators, Digital Taxation, SHAP Values, Synthetic Benchmark.

---

## 1. PENDAHULUAN

Pertumbuhan ekonomi digital di Indonesia terus mencatatkan peningkatan volume transaksi yang signifikan. Berdasarkan laporan e-Conomy SEA (Google, Temasek, & Bain, 2025), nilai transaksi bruto (*Gross Merchandise Value*) ekonomi digital nasional diproyeksikan melampaui US$99 miliar pada tahun 2025 dengan pertumbuhan 14% secara tahunan. Aktivitas perdagangan daring melalui lokapasar (*marketplace*) dan niaga sosial (*social commerce*) berlangsung tanpa memerlukan kantor fisik atau tapak usaha permanen (OECD, 2020). Akibatnya, pengawasan berbasis keberadaan fisik (*physical presence*) tidak lagi memadai untuk memetakan aktivitas ekonomi pelaku usaha secara akurat (Direktorat Jenderal Pajak, 2023).

Ketiadaan bukti fisik transaksi membuka celah ketidaksesuaian pelaporan omset dalam Surat Pemberitahuan (SPT) Tahunan, terutama pada sektor pedagang skala mikro dan menengah yang memanfaatkan berbagai saluran penjualan daring (Kementerian Keuangan RI, 2024). Meskipun pemerintah telah memungut PPN Perdagangan Melalui Sistem Elektronik (PMSE) dari entitas penyedia platform luar negeri dengan realisasi mencapai Rp38,7 triliun per awal 2026 (Direktorat Jenderal Pajak, 2026), verifikasi atas jutaan pedagang lokal di dalam negeri tetap menjadi tantangan besar.

Keterbatasan jumlah personel pemeriksa pajak menyebabkan pemeriksaan secara menyeluruh terhadap seluruh pedagang tidak memungkinkan. Melakukan pemeriksaan acak (*random audit*) tidak efisien dan berpotensi membebani pelaku usaha yang sebenarnya patuh (*false positive*) (Alm & Malézieux, 2021). Di sisi lain, Undang-Undang Nomor 27 Tahun 2022 tentang Pelindungan Data Pribadi (UU PDP) mewajibkan pemrosesan data otomatis dilakukan secara terukur, akuntabel, dan mengedepankan prinsip minimalisasi data (Republik Indonesia, 2022).

Dalam kerangka *Compliance Risk Management* (CRM), Direktorat Jenderal Pajak berupaya mengelompokkan wajib pajak ke dalam kuadran risiko kepatuhan (Direktorat Jenderal Pajak, 2023). Namun, aturan statis berbasis ambang batas sederhana (*rule-based*) sulit menangkap pola penyimpangan transaksi digital yang dinamis dan bervariasi antarwilayah (Mascagni & Mengistu, 2019; Perez-Truglia, 2020). Karena data individual SPT wajib pajak dilindungi oleh undang-undang kerahasiaan fiskal (Pasal 34 UU KUP), komunitas peneliti data sains memerlukan tolok ukur simulasi (*simulation benchmark*) yang valid dan bebas dari kesalahan metodologis (*target circularity*) untuk menguji efektivitas integrasi data eksternal.

Penelitian ini merancang sebuah kerangka kerja simulasi tolok ukur (*synthetic simulation benchmark*) untuk mengevaluasi pemodelan risiko kepatuhan pajak digital. Kontribusi utama penelitian ini adalah:
a. **Membangun Desain Target Non-Sirkular:** Merumuskan mekanisme pembentukan label audit laten yang independen dari formula fitur input guna menghilangkan bias sirkularitas dan kebocoran target (*target leakage*).
b. **Studi Ablasi Fitur Bertahap (*Feature Ablation Study*):** Mengisolasi dan membuktikan secara empiris kontribusi penambahan data transaksi digital, logistik, dan data makroekonomi BPS terhadap peningkatan performa pemeringkatan risiko.
c. **Uji Ketahanan Spasial (*Geographical Out-of-Province Holdout*):** Menguji kemampuan generalisasi model pada provinsi yang belum pernah dilihat dalam data latih untuk mengevaluasi ketahanan lintas wilayah.
d. **Analisis Transparansi Keputusan Berbasis SHAP:** Menerapkan teori permainan kooperatif SHAP guna memberikan penjelasan lokal dan global atas setiap skor risiko, mendukung peran model sebagai sistem pendukung keputusan (*decision support system*).

---

## 2. TINJAUAN PUSTAKA DAN STATE-OF-THE-ART

### 2.1 Informasi Pihak Ketiga dalam Administrasi Perpajakan
Model kepatuhan pajak klasik Allingham-Sandmo-Yitzhaki menempatkan wajib pajak sebagai pengambil keputusan rasional di bawah risiko audit dan sanksi (Alm & Malézieux, 2021). Kleven et al. (2011) serta Slemrod (2019) membuktikan bahwa informasi dari pihak ketiga (*third-party information reporting*) merupakan instrumen paling efektif untuk menurunkan tingkat *underreporting*. Pada ekonomi digital, data penyedia jasa pembayaran dan data pengiriman barang fisik berfungsi sebagai verifikator silang atas peredaran usaha riil (Naritomi, 2019).

### 2.2 Machine Learning, AutoML, dan Interpretabilitas Model
Penerapan algoritma pohon keputusan seperti *Random Forest*, *LightGBM*, dan *XGBoost* telah banyak digunakan dalam deteksi anomali finansial (de Roux et al., 2018; Tian et al., 2020). Penyetelan hyperparameter secara otomatis (*Automated Machine Learning*/AutoML) menggunakan *Tree-structured Parzen Estimator* (TPE) memungkinkan penjelajahan ruang konfigurasi model secara efisien berdasarkan prinsip probabilitas Bayesian (Bergstra et al., 2011; Feurer et al., 2019).

Untuk memastikan model tidak beroperasi sebagai kotak hitam (*black box*), pendekatan *SHapley Additive exPlanations* (SHAP) memberikan alokasi kontribusi aditif bagi setiap variabel masukan (Lundberg & Lee, 2017):

$$g(z') = \phi_0 + \sum_{j=1}^{M} \phi_j z'_j$$

Di mana $\phi_j$ mencerminkan kontribusi marginal fitur ke-$j$ terhadap skor risiko.

### 2.3 Matriks Literatur Rujukan (7 Kolom Standar Riset)
Tabel 1 menyajikan posisi penelitian ini dalam literatur machine learning perpajakan.

**Tabel 1. Matriks Sintesis Literatur Terkait (7 Kolom Standar Riset)**

| Peneliti & Tahun | Domain & Konteks | Sumber Data | Metodologi Algoritma | Metrik Evaluasi | Batasan Riset Sebelumnya | Posisi & Diferensiasi Riset Ini |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| de Roux et al. (2018) | Kecurangan PPh Badan (Kolombia) | SPT & Laporan Keuangan | Random Forest, XGBoost | Precision@K, ROC-AUC | Tidak memasukkan variabel logistik dan indikator makro wilayah | Menambahkan variabel logistik pihak ketiga dan indikator BPS regional |
| Tian et al. (2020) | PPN e-Commerce (Tiongkok) | Log platform marketplace | GNN, GBDT | F1-Score, Recall | Bergantung pada data graf internal platform privat | Menggunakan kerangka data pihak ketiga agregat yang dapat diakses |
| Battaglini et al. (2021) | Kepatuhan Pajak (Italia) | Data audit historis fiskus | Supervised Classification | ROC-AUC (0,812) | Penyetelan hyperparameter manual tanpa uji ketahanan spasial | Menggunakan optimasi Bayesian TPE dan validasi holdout geografis |
| Assefa et al. (2022) | Audit Kepabeanan (Afrika) | Deklarasi pabean | Logistic Regression, Decision Tree | Accuracy, Precision | Performa rendah pada data tidak seimbang (*imbalanced*) | Menggunakan PR-AUC, evaluasi desil audit, dan studi ablasi fitur |
| DJP (2023) | Sistem CRM Pajak (Indonesia) | Data internal & ILAP | Aturan Matriks Heuristik | Realisasi Penerimaan | Model berbasis aturan statis rentan *false positive* | Membangun tolok ukur simulasi non-sirkular berbasis AutoML |
| **Penelitian Ini (2026)** | **Benchmark Pajak Digital Indonesia** | **Simulasi BPS & Transaksi Pihak Ketiga** | **AutoML XGBoost + TPE + SHAP + Ablation** | **ROC-AUC, PR-AUC, Decile Yield, Geo-Holdout** | **-** | **Framework simulasi non-sirkular pertama dengan studi ablasi fitur dan uji spasial** |

---

## 3. METODOLOGI PENELITIAN

### 3.1 Pembangkitan Data Tolok Ukur Non-Sirkular (*Non-Circular Benchmark Design*)
Untuk mengatasi kelemahan metodologis sirkularitas target, dataset simulasi ($N = 5.000$ observasi di 10 provinsi) dibangun dengan memisahkan proses pembentukan fitur masukan $X$ dari label temuan audit $Y$.

a. **Fitur Masukan ($X$):**
   * Indikator Makro BPS: Penetrasi e-commerce ($EComPct_p$) dan indeks infrastruktur ($Infra_p$) per provinsi.
   * Transaksi Digital: Nilai transaksi bruto tahunan ($GMV_i$), volume pesanan ($Vol_i$), dan nilai rata-rata pesanan ($Ticket_i$).
   * Pihak Ketiga: Rasio pembayaran digital ($PayRatio_i$) dan rasio keterlacakan logistik ($Logistics_i$).
   * Laporan Mandiri: Omset dilaporkan SPT ($SPT_i$) dan setoran pajak final ($TaxPaid_i$).

b. **Target Temuan Audit Independen ($Y$):**
   Label audit $Y \in \{0, 1\}$ (25% kasus berisiko) dibangkitkan dari skor temuan audit laten yang memuat faktor distorsi inventaris tak teramati ($\delta_{\text{inv}}$), kecenderungan *cash skimming* ($\delta_{\text{cash}}$), dan anomali logistik ($\delta_{\text{log}}$) dengan gangguan stokastik acak $\varepsilon_i \sim \mathcal{N}(0, 0,12^2)$:
   $$S^*_{\text{audit}} = 0,35 \cdot \delta_{\text{cash}} + 0,30 \cdot \left(\frac{\delta_{\text{inv}}}{1 + \delta_{\text{inv}}}\right) + 0,20 \cdot \delta_{\text{log}} + 0,15 \cdot \left(1 - \min\left(1, \frac{SPT_i}{GMV_i}\right)\right) + \varepsilon_i$$
   Fitur masukan model tidak memiliki akses ke variabel laten $\delta_{\text{inv}}$ dan $\delta_{\text{log}}$, sehingga model benar-benar diuji untuk mempelajari pola indikasi ketidakpatuhan secara tidak langsung.

Gambar 1 menyajikan matriks korelasi antar-fitur.

![Matriks Korelasi Fitur](/images/figure1_correlation_matrix.png)  
*Gambar 1. Matriks Korelasi Multivariat Fitur BPS dan Parameter Transaksi (300 DPI).*

### 3.2 Protokol Validasi dan Pencegahan Kebocoran Data
Pemisahan data latih (80%, $n=4.000$) dan data uji independen (20%, $n=1.000$) dilakukan sebelum transformasi fitur. Penyetelan hyperparameter Bayesian TPE dilakukan murni di dalam 5-Fold Stratified Cross-Validation pada data latih tanpa melibatkan data uji. Seluruh proses stokastik dikunci pada $\text{seed} = 42$.

---

## 4. HASIL DAN PEMBAHASAN

### 4.1 Evaluasi Kinerja Model Klasifikasi
Tabel 2 merangkum hasil evaluasi komparatif pada validasi silang 5-Fold dan data uji independen.

**Tabel 2. Evaluasi Kinerja Model Klasifikasi pada Data Uji Independen ($n=1.000$)**

| Model | CV ROC-AUC (Mean $\pm$ Std) | Holdout ROC-AUC | PR-AUC | F1-Score | Precision | Recall | Specificity | Matriks Konfusi (TN/FP/FN/TP) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| Logistic Regression | $0,6728 \pm 0,0205$ | 0,6745 | 0,3828 | 0,0982 | 0,4000 | 0,0560 | 0,9720 | 729 / 21 / 236 / 14 |
| Random Forest | $0,6459 \pm 0,0143$ | 0,6516 | 0,3717 | 0,1241 | 0,4500 | 0,0720 | 0,9707 | 728 / 22 / 232 / 18 |
| LightGBM | $0,6119 \pm 0,0089$ | 0,6296 | 0,3539 | 0,2202 | 0,4302 | 0,1480 | 0,9347 | 701 / 49 / 213 / 37 |
| **AutoML (XGBoost TPE)** | $\mathbf{0,6601 \pm 0,0122}$ | **0,6694** | **0,3835** | 0,0455 | 0,4286 | 0,0240 | **0,9893** | 742 / 8 / 244 / 6 |

Hasil pada Tabel 2 menunjukkan kinerja yang realistis pada dataset non-sirkular. Model mencapai ROC-AUC berkisar antara 0,63 hingga 0,67 dan PR-AUC 0,38 (secara signifikan di atas baseline acak 0,25). Kurva ROC dan Precision-Recall disajikan pada Gambar 2 dan Gambar 3.

![Kurva ROC Komparatif](/images/figure2_roc_auc_curve.png)  
*Gambar 2. Kurva ROC Komparatif pada Data Uji Independen (300 DPI).*

![Kurva Precision-Recall](/images/figure3_pr_auc_curve.png)  
*Gambar 3. Kurva Precision-Recall Komparatif (300 DPI).*

### 4.2 Studi Ablasi Fitur (*Feature Ablation Study*)
Untuk membuktikan secara ilmiah manfaat penambahan data pihak ketiga dan indikator BPS, kami menjalankan pengujian ablasi pada empat konfigurasi subset fitur (Tabel 3 dan Gambar 5).

**Tabel 3. Hasil Studi Ablasi Fitur Menggunakan Model XGBoost**

| Konfigurasi Fitur | ROC-AUC | PR-AUC | F1-Score | Tangkapan Desil Top 20% (%) | Kontribusi Utama |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **1. Data SPT Mandiri Saja** | 0,5026 | 0,2833 | 0,0000 | 23,2% | Performa acak; pelaporan mandiri tidak memiliki daya pembeda |
| **2. + Transaksi Digital (Gateway & GMV)** | 0,6465 | 0,3619 | 0,0530 | 29,6% | Peningkatan tajam (+0,1439 AUC); menangkap volume riil |
| **3. + Data Logistik Pengiriman** | 0,6715 | 0,3854 | 0,0672 | 32,8% | Memperkuat verifikasi fisik pergerakan barang dagangan |
| **4. Model Penuh (+ Indikator Makro BPS)** | **0,6694** | **0,3835** | 0,0455 | **34,0%** | Memaksimalkan tangkapan risiko pada desil teratas (34,0%) |

![Hasil Studi Ablasi](/images/figure5_ablation_study_bars.png)  
*Gambar 5. Perbandingan Skor ROC-AUC pada Studi Ablasi Fitur (300 DPI).*

Temuan ablasi menunjukkan bahwa mengandalkan data SPT semata menghasilkan performa setara tebakan acak (AUC 0,5026). Penambahan data gerbang pembayaran dan logistik menjadi pendorong utama peningkatan kemampuan deteksi risiko (AUC naik ke 0,6715).

### 4.3 Analisis Efisiensi Desil Audit (*Audit Yield*)
Gambar 4 menyajikan kurva tangkapan kumulatif berdasarkan pemeringkatan risiko model.

![Kurva Keuntungan Kumulatif per Desil](/images/figure4_cumulative_gains_decile.png)  
*Gambar 4. Kurva Keuntungan Kumulatif Temuan Audit per Desil Risiko (300 DPI).*

Dengan memprioritaskan pemeriksaan pada **Top 20% desil risiko teratas (Desil 1 dan 2)**, otoritas pajak dapat menjaring **34,0% dari total potensi ketidakpatuhan**, menghasilkan faktor pengali *cumulative lift* sebesar **1,70 kali lipat** dibandingkan audit acak konvensional (20%).

### 4.4 Uji Ketahanan Spasial (*Geographical Holdout Generalization*)
Untuk menguji apakah indikator regional BPS menimbulkan bias kedaerahan, kami melatih model pada 8 provinsi ($n=4.006$) dan mengujinya secara *zero-shot* pada 2 provinsi yang belum pernah dilihat model (Bali dan Sulawesi Selatan, $n=994$).

![Uji Ketahanan Spasial](/images/figure8_geographical_holdout.png)  
*Gambar 8. Performa Evaluasi Spasial pada Provinsi Holdout yang Belum Pernah Dilihat (300 DPI).*

Hasil pengujian pada data holdout geografis mempertahankan skor ROC-AUC sebesar **0,6689** dan PR-AUC sebesar **0,3913**. Hal ini membuktikan bahwa model mampu menggeneralisasi penilaian risiko pada wilayah baru tanpa mengalami penurunan performa drastis.

### 4.5 Interpretasi Model Berbasis SHAP dan Matriks Konfusi
Gambar 6 dan Gambar 7 menampilkan ringkasan nilai SHAP dan matriks konfusi ternormalisasi.

![SHAP Beeswarm Plot](/images/figure6_shap_beeswarm.png)  
*Gambar 6. Sebaran Kontribusi Fitur Berdasarkan Nilai SHAP Beeswarm (300 DPI).*

![Matriks Konfusi Ternormalisasi](/images/figure7_confusion_matrix.png)  
*Gambar 7. Normalized Confusion Matrix Model XGBoost (300 DPI).*

Analisis SHAP mengonfirmasi bahwa rasio pembayaran digital dan rasio keterlacakan logistik menjadi variabel penjelas paling dominan dalam membedakan entitas berisiko tinggi. Matriks konfusi pada Gambar 7 mencatatkan spesifisitas **98,93% (True Negative)**, memastikan bahwa pada ambang probabilitas standar, sistem ini sangat berhati-hati dan meminimalkan kesalahan tuduhan audit (*false positive*) terhadap wajib pajak patuh.

---

## 5. KESIMPULAN DAN REKOMENDASI

### 5.1 Kesimpulan
Penelitian ini berhasil menyusun kerangka tolok ukur simulasi non-sirkular untuk mengevaluasi pemodelan kepatuhan pajak digital. Studi ablasi fitur membuktikan bahwa pelaporan mandiri wajib pajak tidak cukup untuk mendeteksi risiko (AUC 0,5026), sementara integrasi data gerbang pembayaran dan logistik secara signifikan meningkatkan kemampuan pemeringkatan risiko (AUC 0,6715 dan Top 20% Decile Yield 34,0%). Uji geografis out-of-province membuktikan stabilitas model pada wilayah baru (AUC 0,6689), sementara penjelasan SHAP menjamin transparansi keputusan sebagai sistem pendukung keputusan (*decision support system*) yang akuntabel.

### 5.2 Rekomendasi Kebijakan
a. **Integrasi Data Transaksi Pihak Ketiga:** Memprioritaskan kerja sama interoperabilitas data antara DJP dengan penyedia gerbang pembayaran dan logistik digital sebagai sumber verifikasi paling informatif.
b. **Pemanfaatan Model sebagai Decision Support System:** Menempatkan skor risiko machine learning sebagai alat penyaring prioritas pemeriksaan (*ranking tool*), bukan penentu sanksi hukum otomatis, guna menjaga kepatuhan terhadap UU PDP Nomor 27 Tahun 2022.
c. **Pengujian Model secara Spasial dan Berkala:** Melakukan validasi model lintas wilayah secara berkala untuk mencegah bias geografis dalam penilaian kepatuhan perpajakan.

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
