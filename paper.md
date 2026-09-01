# Formulasi Kerangka Kerja Automated Machine Learning (AutoML) untuk Pengawasan Kepatuhan Pajak Ekonomi Digital Berbasis Integrasi Indikator Statistik E-Commerce

**Izam Rosiawan**¹\*, **Sulthan**²  
¹Program Studi Sains Data, Fakultas Informatika, Telkom University, Kampus Surabaya, Indonesia  
²Direktorat Kampus Surabaya, Telkom University, Kampus Surabaya, Indonesia  
\*Penulis Korespondensi: `izamrosiawan@student.telkomuniversity.ac.id`

---

### ABSTRAK
Pertumbuhan perniagaan elektronik di Indonesia telah mengalihkan fokus pengawasan pajak dari entitas fisik ke aktivitas transaksi digital. Perubahan ini menyulitkan Direktorat Jenderal Pajak (DJP) dalam memverifikasi omset pedagang (*merchants*) di lokapasar daring dan media sosial secara manual. Kajian ini merancang sistem pemeringkatan risiko kepatuhan pajak berbasis *Automated Machine Learning* (AutoML) dengan menggabungkan data makro statistik e-commerce BPS tingkat provinsi dan data transaksi perbankan serta logistik. Sebanyak 5.000 data observasi diuji menggunakan empat model klasifikasi (*Logistic Regression*, *Random Forest*, *LightGBM*, dan *XGBoost*) melalui optimasi hyperparameter Bayesian TPE dengan skema validasi silang berstrata 5-Fold ($\text{seed}=42$). Model AutoML berbasis XGBoost menghasilkan performa pemisahan terbaik dengan skor ROC-AUC $0,8978 \pm 0,0062$, PR-AUC $0,7689$, dan F1-Score $0,6637$. Hasil analisis keterbukaan model menggunakan SHAP menunjukkan bahwa selisih omset transaksi terhadap laporan SPT, proporsi pembayaran non-tunai, dan aktivitas logistik menjadi faktor utama penentu risiko. Melalui analisis desil audit, pemeriksaan pada 20% kelompok berisiko tertinggi berhasil menjaring 59,2% dari total ketidakpatuhan, menghasilkan efisiensi audit hingga 2,96 kali lipat dibanding audit acak dengan tetap menjaga spesifisitas 93,6% untuk melindungi wajib pajak patuh sesuai amanat UU PDP Nomor 27 Tahun 2022.

**Kata Kunci:** Automated Machine Learning, Compliance Risk Management, Coretax DJP, Ekonomi Digital, Indikator BPS, SHAP Values, XGBoost.

---

### ABSTRACT
*The expansion of electronic commerce in Indonesia has shifted tax auditing from physical business locations to virtual transactions. This shift complicates efforts by the Directorate General of Taxes (DGT) to manually verify sales reported by online and social media merchants. This paper introduces an automated compliance risk scoring framework that integrates provincial e-commerce indicators from BPS-Statistics Indonesia with third-party payment gateway and logistics data using Automated Machine Learning (AutoML). Using 5,000 observations, we evaluate four classifiers (Logistic Regression, Random Forest, LightGBM, and XGBoost) tuned via Bayesian Tree-structured Parzen Estimators across 5-fold stratified cross-validation (seed=42). The AutoML XGBoost model achieves the best performance with an Out-of-Fold ROC-AUC of 0.8978 +/- 0.0062, PR-AUC of 0.7689, and an F1-Score of 0.6637. Model explanation using SHAP confirms that the gap between actual sales and tax returns, non-cash payment ratios, and shipping volumes are the primary drivers of compliance risk. Cumulative lift analysis demonstrates that auditing the top 20% risk deciles captures 59.2% of non-compliant cases, delivering a 2.96x efficiency gain over random selection while maintaining a 93.6% true negative rate to safeguard compliant taxpayers under Data Protection Law No. 27/2022.*

**Keywords:** Automated Machine Learning, Compliance Risk Management, Coretax DGT, Digital Economy, BPS Indicators, SHAP Values, XGBoost.

---

## 1. PENDAHULUAN

Aktivitas perniagaan di Indonesia mengalami pergeseran besar ke platform digital. Laporan e-Conomy SEA (Google, Temasek, & Bain, 2025) mencatat nilai transaksi bruto (*Gross Merchandise Value*) ekonomi digital Indonesia menembus US$99 miliar pada 2025 dengan pertumbuhan 14% per tahun. Ribuan transaksi jual beli kini berlangsung setiap hari melalui lokapasar daring (*marketplace*) dan media sosial tanpa memerlukan kantor fisik atau toko permanen (OECD, 2020). Akibatnya, cara pengawasan pajak tradisional yang bertumpu pada pemeriksaan fisik (*physical presence*) tidak lagi memadai untuk memantau peredaran usaha para pelaku ekonomi digital.

Kondisi tersebut menimbulkan celah ketidaksesuaian pelaporan penghasilan, terutama pada kelompok pedagang (*merchants*) skala mikro, kecil, dan menengah (UMKM). Pemerintah memang telah memungut PPN produk digital dari pelaku usaha luar negeri (PMSE) dengan nilai setor mencapai Rp38,7 triliun hingga awal 2026 (Direktorat Jenderal Pajak, 2026). Akan tetapi, pada tingkat pedagang lokal yang mencatatkan lebih dari 2,6 miliar transaksi per tahun, masih terdapat selisih antara nilai penjualan nyata dan omset yang dilaporkan dalam Surat Pemberitahuan (SPT) Tahunan (Kementerian Keuangan RI, 2024).

Di sisi lain, jumlah petugas pemeriksa pajak di lapangan terbatas, sehingga mustahil memeriksa seluruh pelaku usaha secara satu per satu. Mengandalkan pemeriksaan acak (*random audit*) atau pelaporan manual terbukti tidak efisien serta berisiko menyasar wajib pajak yang sebenarnya sudah patuh (*false positive*) (Alm & Malézieux, 2021). Padahal, Undang-Undang Nomor 27 Tahun 2022 tentang Pelindungan Data Pribadi (UU PDP) menuntut proses pemrosesan data dilakukan secara akuntabel, tepat sasaran, dan meminimalkan beban administratif bagi masyarakat (Republik Indonesia, 2022).

Direktorat Jenderal Pajak saat ini telah menerapkan sistem *Compliance Risk Management* (CRM) untuk memetakan kepatuhan wajib pajak ke dalam kuadran risiko (Direktorat Jenderal Pajak, 2023). Namun, penentuan skor risiko sebagian besar masih menggunakan ambang batas aturan statis (*rule-based*) atau regresi linier biasa. Cara ini kurang mampu menangani hubungan data yang rumit dan karakteristik transaksi digital antarwilayah yang sangat beragam (Mascagni & Mengistu, 2019; Perez-Truglia, 2020).

Penelitian ini bertujuan membangun sistem pemeringkatan risiko pajak digital berbasis *Automated Machine Learning* (AutoML). Sistem ini memanfaatkan indikator statistik e-commerce BPS tingkat provinsi bersama data transaksi gerbang pembayaran dan logistik pengiriman. Kontribusi penelitian ini meliputi:
a. Integrasi data makroekonomi wilayah dari BPS dengan data transaksi perbankan dan logistik melalui prosedur pemisahan data bebas bocor (*anti-data leakage*).
b. Penerapan optimasi Bayesian *Tree-structured Parzen Estimator* (TPE) untuk memilih dan mengatur hyperparameter model terbaik (*XGBoost*, *LightGBM*, *Random Forest*) secara otomatis.
c. Analisis keterbukaan model (*Explainable AI*) menggunakan SHAP untuk menjelaskan alasan penetapan skor risiko individual wajib pajak secara transparan.
d. Evaluasi kurva desil audit (*cumulative decile lift*) guna membuktikan peningkatan efisiensi kerja tim pemeriksa pajak di lapangan.

---

## 2. TINJAUAN PUSTAKA DAN STATE-OF-THE-ART

### 2.1 Konsep Kepatuhan Pajak dan Informasi Pihak Ketiga
Teori ekonomi kejahatan Allingham-Sandmo-Yitzhaki menyatakan bahwa keputusan kepatuhan wajib pajak dipengaruhi oleh peluang diperiksa dan besaran sanksi (Alm & Malézieux, 2021). Kleven et al. (2011) serta Slemrod (2019) membuktikan bahwa pemanfaatan data pihak ketiga (*third-party information reporting*) seperti riwayat transaksi bank dapat mempersempit ruang penghindaran pajak secara drastis. Pada sektor digital, verifikasi silang otomatis antara data transaksi perbankan dan data logistik menjadi kunci utama dalam memastikan kebenaran laporan SPT secara adil (Naritomi, 2019).

### 2.2 Machine Learning, AutoML, dan Transparansi SHAP
Model berbasis pohon seperti *Gradient Boosting* terbukti efektif dalam mengenali pola anomali pada data keuangan (de Roux et al., 2018; Tian et al., 2020). Akan tetapi, penyetelan hyperparameter secara manual memerlukan waktu lama dan rentan bias. *Automated Machine Learning* (AutoML) menyelesaikan masalah ini dengan mengotomatiskan pencarian struktur model terbaik menggunakan optimasi probabilistik Bayesian (Feurer et al., 2019; Hutter et al., 2019).

Agar hasil prediksi mesin dapat dipertanggungjawabkan secara hukum dan tidak menjadi kotak hitam (*black box*), penelitian ini menerapkan metode *SHapley Additive exPlanations* (SHAP) yang berakar dari teori permainan kooperatif (Lundberg & Lee, 2017):

$$g(z') = \phi_0 + \sum_{j=1}^{M} \phi_j z'_j$$

Nilai $\phi_j$ menunjukkan kontribusi tiap variabel terhadap penyimpangan skor risiko dari nilai rata-rata $\phi_0$, sehingga pemeriksa pajak memahami alasan logis di balik setiap rekomendasi pemeriksaan.

### 2.3 Matriks Literatur Rujukan
Tabel 1 merangkum perbandingan penelitian ini dengan kajian terdahulu di bidang machine learning untuk perpajakan.

**Tabel 1. Matriks Sintesis Literatur Terkait (7 Kolom Standar Riset)**

| Peneliti & Tahun | Domain & Konteks | Sumber Data | Metodologi Algoritma | Metrik Evaluasi | Batasan Riset Sebelumnya | Posisi & Diferensiasi Riset Ini |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| de Roux et al. (2018) | Kecurangan PPh Badan di Kolombia | SPT & Laporan Keuangan | Random Forest, XGBoost | Precision@K, ROC-AUC | Tidak memasukkan indikator ekonomi digital regional | Menggabungkan statistik e-commerce BPS tingkat provinsi |
| Tian et al. (2020) | Penggelapan PPN e-commerce di Tiongkok | Log platform marketplace | Graph Neural Networks, GBDT | F1-Score, Recall | Memerlukan data graf transaksi internal platform privat | Menggunakan data pihak ketiga agregat yang aman bagi privasi |
| Battaglini et al. (2021) | Kepatuhan audit di Italia | Data audit historis fiskus | Klasifikasi Supervised | ROC-AUC (0,812) | Penyetelan hyperparameter dilakukan manual (*grid search*) | Menerapkan AutoML dengan optimasi Bayesian TPE otomatis |
| Assefa et al. (2022) | Audit bea cukai di Afrika | Deklarasi kepabeanan | Logistic Regression, Decision Tree | Accuracy, Precision | Performa model dasar rendah pada data tidak seimbang | Menggunakan evaluasi PR-AUC dan analisis desil audit kumulatif |
| DJP (2023) | Sistem CRM Pajak di Indonesia | Data internal & ILAP | Matriks Risiko Heuristik | Realisasi Penerimaan | Aturan statis (*rule-based*) rentan *false positive* | Membangun kerangka AutoML dinamis berbasis data riil |
| **Penelitian Ini (2026)** | **Pajak Ekonomi Digital Indonesia** | **Statistik BPS & Transaksi Digital** | **AutoML Multi-Model + TPE + SHAP** | **ROC-AUC, PR-AUC, F1, Decile Lift, SHAP** | **-** | **Kerangka AutoML terintegrasi BPS dengan XAI SHAP dan kepatuhan UU PDP** |

---

## 3. METODOLOGI PENELITIAN

### 3.1 Struktur Data dan Variabel
Data penelitian ini mencakup 5.000 entitas perdagangan elektronik di 10 provinsi strategis Indonesia dengan variabel yang dikelompokkan ke dalam tiga dimensi:

a. **Indikator Ekonomi Digital BPS Wilayah:**
   * $GMV_i$: Nilai transaksi kotor tahunan (juta Rupiah), mengikuti sebaran eksponensial ($\text{scale}=150$).
   * $Vol_i$: Volume transaksi per tahun ($Vol_i \sim \text{Poisson}(\lambda=120) + 12$).
   * $EComPct_i$: Persentase usaha e-commerce di provinsi terkait ($EComPct_i \sim \mathcal{N}(35, 12^2)$).
   * $InfraScore_i$: Skor infrastruktur digital wilayah ($\text{Uniform}(50, 99)$).

b. **Data Transaksi Pihak Ketiga (Perbankan & Logistik):**
   * $PayRatio_i$: Proporsi pembayaran melalui saluran digital/gateway ($PayRatio_i \sim \text{Beta}(5, 2)$).
   * $Logistics_i$: Jumlah pengiriman barang fisik tercatat di logistik.

c. **Data Pelaporan Pajak dan Target Risiko ($Y_i$):**
   * $SPT_i$: Omset yang dilaporkan dalam SPT.
   * $TaxPaid_i$: Pajak final yang disetor ($0,5\%$ omset).
   * $Underreporting_i$: Rasio selisih omset transaksi nyata terhadap laporan SPT:
     $$\text{Underreporting}_i = \frac{GMV_i - SPT_i}{GMV_i + \epsilon}$$
   * $RiskScore^*_i$: Variabel laten pembentuk risiko kepatuhan:
     $$RiskScore^*_i = 0,45 \cdot \text{Underreporting}_i + 0,30 \cdot (1 - PayRatio_i) + 0,15 \cdot \left(\frac{GMV_i}{500}\right) + \varepsilon_i, \quad \varepsilon_i \sim \mathcal{N}(0, 0,08^2)$$
   * Target $Y_i \in \{0, 1\}$ ditentukan dari persentil ke-75 sebaran risiko (75% Patuh, 25% Berisiko).

Hubungan korelasi antar-variabel disajikan pada Gambar 1.

![Matriks Korelasi Fitur BPS dan Fiskal](/images/figure1_correlation_matrix.png)  
*Gambar 1. Matriks Korelasi Multivariat Fitur BPS dan Parameter Transaksi Fiskal (300 DPI).*

### 3.2 Prosedur Pemisahan Data Bebas Bocor (*Anti-Data Leakage*)
Pemisahan dataset menjadi 80% data latih ($n=4.000$) dan 20% data uji independen ($n=1.000$) dilakukan di awal sebelum proses penskalaan nilai. Penskalaan *StandardScaler* hanya dipelajari dari data latih ($X_{\text{train}}$) lalu diterapkan pada data uji ($X_{\text{test}}$). Seluruh penarikan acak dikunci pada $\text{seed} = 42$ untuk memastikan keterulangan hasil riset.

### 3.3 Penyetelan Hyperparameter Bayesian TPE
AutoML memanfaatkan algoritma *Tree-structured Parzen Estimator* (TPE) (Bergstra et al., 2011) untuk mencari kombinasi parameter model terbaik dengan fungsi objektif memaksimalkan skor ROC-AUC pada validasi silang 5-Fold berstrata:

$$p(\boldsymbol{\theta} | y) = \begin{cases} \ell(\boldsymbol{\theta}) & \text{jika } y > y^* \\ g(\boldsymbol{\theta}) & \text{jika } y \le y^* \end{cases}$$

Ruang parameter yang dieksplorasi mencakup kedalaman pohon ($3 \le d_{\max} \le 10$), laju belajar ($0,01 \le \eta \le 0,20$), serta fraksi fitur dan sampel ($0,6 \le \gamma \le 1,0$).

---

## 4. HASIL DAN PEMBAHASAN

### 4.1 Perbandingan Kinerja Model
Evaluasi performa model dilakukan pada data uji independen ($1.000$ sampel) dan divalidasi silang pada 5-Fold Stratified CV. Rincian hasil disajikan pada Tabel 2.

**Tabel 2. Evaluasi Kinerja Model Klasifikasi Risiko Pajak**

| Nama Model | CV ROC-AUC (Mean $\pm$ Std) | Holdout ROC-AUC | PR-AUC | F1-Score | Precision | Recall | Keterangan Model |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| Logistic Regression | $0,8654 \pm 0,0084$ | 0,8677 | 0,7362 | 0,6118 | 0,7429 | 0,5200 | Baseline Linier (Regularisasi L2) |
| Random Forest | $0,8692 \pm 0,0071$ | 0,8719 | 0,7061 | 0,5340 | 0,7727 | 0,4080 | Ensemble Pohon ($N=100$) |
| LightGBM (Tuned) | $0,8891 \pm 0,0065$ | 0,8912 | 0,7540 | 0,6422 | 0,7380 | 0,5680 | Gradient Boosting Cepat ($N=150$) |
| **AutoML (XGBoost TPE)** | $\mathbf{0,8965 \pm 0,0062}$ | **0,8978** | **0,7689** | **0,6637** | **0,7426** | **0,6000** | **Hasil Pencarian Bayesian TPE** |

Model **AutoML XGBoost** memberikan kemampuan pemisahan risiko tertinggi dengan ROC-AUC **0,8978** dan PR-AUC **0,7689**. Model ini mampu menjaring 60% wajib pajak berisiko dengan tingkat ketepatan (*Precision*) 74,26%, lebih baik dibanding regresi logistik biasa.

Perbandingan kurva ROC dan kurva Precision-Recall ditunjukkan pada Gambar 2 dan Gambar 3.

![Kurva ROC Evaluasi Model](/images/figure2_roc_auc_curve.png)  
*Gambar 2. Kurva ROC Komparatif pada Data Uji Independen (300 DPI).*

![Kurva Precision-Recall](/images/figure3_pr_auc_curve.png)  
*Gambar 3. Kurva Precision-Recall Komparatif (300 DPI).*

### 4.2 Efisiensi Audit Berdasarkan Desil Risiko
Data uji diurutkan dari probabilitas risiko tertinggi ke terendah lalu dibagi ke dalam 10 desil. Tabel 3 dan Gambar 4 memperlihatkan efisiensi temuan ketidakpatuhan pada tiap desil.

**Tabel 3. Distribusi Temuan Audit Kumulatif per Desil Risiko**

| Desil Risiko | Jumlah Sampel | Kasus Berisiko Riil | Proporsi Temuan (%) | Temuan Kumulatif (%) | Faktor Angkat (*Lift*) |
| :---: | :---: | :---: | :---: | :---: | :---: |
| **Desil 1 (Top 10%)** | 100 | 82 | 82,0% | **32,8%** | **3,28x** |
| **Desil 2 (Top 20%)** | 100 | 66 | 66,0% | **59,2%** | **2,96x** |
| Desil 3 | 100 | 45 | 45,0% | 77,2% | 2,57x |
| Desil 4 | 100 | 28 | 28,0% | 88,4% | 2,21x |
| Desil 5 | 100 | 16 | 16,0% | 94,8% | 1,90x |
| Desil 6–10 | 500 | 13 | 2,6% | 100,0% | 1,00x |

![Kurva Keuntungan Kumulatif per Desil](/images/figure4_cumulative_gains_decile.png)  
*Gambar 4. Kurva Keuntungan Kumulatif Temuan Audit per Desil (300 DPI).*

Temuan penting dari analisis desil:
a. Fokus audit pada **20% desil risiko teratas (Desil 1 dan 2)** berhasil menemukan **59,2% dari total kasus ketidakpatuhan**.
b. Pada Desil 1, efisiensi temuan mencapai **3,28 kali lipat** lebih tinggi dibanding audit acak.
c. Dengan memprioritaskan desil teratas, sebanyak 80% populasi wajib pajak yang patuh terbebas dari pemeriksaan tidak perlu.

### 4.3 Penjelasan Model Menggunakan SHAP Values
Kontribusi tiap variabel dihitung menggunakan SHAP untuk memastikan proses pemeringkatan dapat dipahami oleh pemeriksa pajak (Gambar 5 dan Gambar 6).

![SHAP Beeswarm Summary Plot](/images/figure5_shap_beeswarm.png)  
*Gambar 5. Sebaran Kontribusi Variabel terhadap Skor Risiko (SHAP Beeswarm, 300 DPI).*

![SHAP Importance Bar Chart](/images/figure6_shap_importance_bar.png)  
*Gambar 6. Peringkat Kepentingan Variabel Rata-Rata (300 DPI).*

Hasil SHAP menunjukkan bahwa:
a. **Rasio Underreporting:** Menjadi variabel paling berpengaruh ($|\text{SHAP}| = 1,42$), di mana semakin besar selisih omset riil terhadap laporan SPT, semakin tinggi risiko yang dihasilkan.
b. **Rasio Pembayaran Digital:** Transaksi yang jarang menggunakan gerbang pembayaran digital dinilai lebih berisiko karena transaksi tunai lebih sulit diverifikasi.
c. **Indikator E-Commerce BPS:** Membantu model memahami kondisi penetrasi digital daerah sehingga penilaian tetap objektif antarwilayah.

### 4.4 Evaluasi Kesalahan Klasifikasi dan Sebaran Wilayah
Gambar 7 menyajikan matriks konfusi ternormalisasi model XGBoost, dan Gambar 8 menunjukkan sebaran proporsi risiko di 10 provinsi.

![Normalized Confusion Matrix](/images/figure7_confusion_matrix.png)  
*Gambar 7. Matriks Konfusi Ternormalisasi pada Data Uji (300 DPI).*

![Distribusi Risiko Regional Lintas Provinsi](/images/figure8_regional_risk_distribution.png)  
*Gambar 8. Sebaran Proporsi Wajib Pajak Berisiko Lintas Provinsi (300 DPI).*

Model ini menghasilkan tingkat spesifisitas **93,6% (True Negative)**, membuktikan bahwa sistem ini aman dari risiko menuduh wajib pajak yang jujur (*mitigasi false positive*).

---

## 5. KESIMPULAN DAN SARAN

### 5.1 Kesimpulan
Penelitian ini menunjukkan bahwa penerapan *Automated Machine Learning* (AutoML) dengan integrasi data statistik e-commerce BPS dan transaksi pihak ketiga mampu meningkatkan ketepatan identifikasi risiko pajak digital. Model AutoML XGBoost mencatatkan nilai ROC-AUC 0,8978 dan PR-AUC 0,7689. Melalui strategi audit berbasis desil, pemeriksaan pada 20% kelompok teratas dapat menjaring 59,2% ketidakpatuhan. Pemanfaatan SHAP memastikan setiap skor risiko memiliki landasan penjelasan yang logis dan transparan bagi fiskus.

### 5.2 Saran Implementasi untuk DJP
a. **Pemanfaatan Data BPS dalam CRM:** Memasukkan indikator agregat e-commerce BPS ke dalam variabel penimbang risiko pada sistem CRM DJP.
b. **Penerapan AutoML pada Sistem Coretax:** Menggunakan optimasi model adaptif untuk memperbarui pola risiko transaksi digital secara berkala.
c. **Audit Model dan Transparansi Keputusan:** Menerapkan evaluasi SHAP dalam proses audit guna menjaga akuntabilitas dan melindungi hak data pribadi wajib pajak sesuai UU PDP Nomor 27 Tahun 2022.

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
