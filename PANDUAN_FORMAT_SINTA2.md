# PANDUAN STRUKTUR DAN FORMAT PENULISAN JURNAL SINTA 2
Bidang: Sains Data, Informatika, dan Sistem Informasi (Standar JNTETI UGM, JTIIK UB, JSI UI, Kinetik)

---

## 1. STRUKTUR UTAMA MANUSKRIP (STANDARD IMRaD)

Format naskah ilmiah untuk jurnal terakreditasi SINTA 2 wajib mengikuti urutan baku berikut:

1. **JUDUL ARTIKEL**
   - Singkat, padat, lugas (maksimal 14–18 kata).
   - Ditulis dalam Bahasa Indonesia dan Bahasa Inggris.
   - Menggambarkan metode utama, objek masalah, dan kontribusi unik penelitian.
   - Format: Center, Bold, 14–16 pt, Title Case.

2. **IDENTITAS PENULIS & AFILIASI**
   - Nama Lengkap Penulis (tanpa gelar akademis).
   - Penulis Korespondensi diberi tanda bintang (*).
   - Nama Program Studi, Fakultas, Universitas, Kota, dan Negara.
   - Alamat Email institusi resmi penulis korespondensi.

3. **ABSTRAK BILINGUAL (INDONESIA & INGGRIS)**
   - Format: 1 Paragraf Utuh (Single Spacing), panjang 150–250 kata.
   - Memuat 4 komponen wajib:
     a. Latar Belakang & Masalah Singkat.
     b. Metode/Arsitektur Algoritma yang diusulkan.
     c. Temuan Kuantitatif Utama (Sebutkan angka metrik: ROC-AUC, Lift, Gap, CI).
     d. Kesimpulan & Implikasi Praktis.
   - **Kata Kunci / Keywords:** 3–5 kata/frasa baku, disusun alfabetis, dipisahkan tanda koma.

4. **1. PENDAHULUAN (INTRODUCTION)**
   - Menggunakan alur piramida terbalik (Deduktif):
     - Paragraf 1: Konteks riil dan nilai strategis masalah.
     - Paragraf 2: Tantangan operasional dan limitasi pengawasan konvensional.
     - Paragraf 3: Penelitian terdahulu (State-of-the-Art) dan **Research Gap**.
     - Paragraf 4: Rumusan Pertanyaan Penelitian (*Research Questions* / RQ1, RQ2, RQ3).
     - Paragraf 5: Rincian Poin Kontribusi Baru (*Novelty Statement* a, b, c, d).

5. **2. TINJAUAN PUSTAKA / METODE TERKAIT**
   - Landasan teori pendukung (Grand Theory).
   - Tinjauan literatur komparatif (disarankan menampilkan **Tabel Matriks Sintesis Literatur 7-Kolom**).

6. **3. METODOLOGI PENELITIAN (RESEARCH METHODOLOGY)**
   - Menjelaskan seluruh alur penelitian secara transparan agar dapat direplikasi (*Reproducibility*):
     - Arsitektur Data / Proses Pembangkitan Data (*Data Generating Process*).
     - Definisi Variabel dan Justifikasi Parameter.
     - Protokol Pemisahan Data (*Data Split*, misal: 80/20 Stratified).
     - Pipeline Algoritma Machine Learning & Penyetelan Hyperparameter (misal: TPE Bayesian).
     - Metrik Evaluasi Statistik (ROC-AUC, PR-AUC, 95% Bootstrap Confidence Interval).

7. **4. HASIL DAN PEMBAHASAN (RESULTS AND DISCUSSION)**
   - Menyajikan data temuan dalam bentuk **Tabel Akademik 3-Garis** dan Grafik Beresolusi Tinggi (300 DPI).
   - Pola interpretasi: **Meaning-First Interpretation** (bukan sekadar membaca angka, melainkan menguraikan *mengapa* algoritma A lebih unggul daripada algoritma B).
   - Studi Ablasi Fitur untuk membuktikan kontribusi tiap kelompok variabel.
   - Evaluasi Keterbukaan Algoritma (SHAP) dan Uji Ketahanan (Cross-Province Holdout).

8. **5. PEMBAHASAN TATA KELOLA & IMPLIKASI (GOVERNANCE & DISCUSSION)**
   - Implikasi regulasi (misal: Kepatuhan UU PDP, enkripsi data, mitigasi bias regional).
   - Pertimbangan biaya kesalahan operasional (*False Positive* vs *False Negative*).
   - Keterbatasan penelitian (*Limitation Statement*).

9. **6. KESIMPULAN DAN REKOMENDASI (CONCLUSION & RECOMMENDATIONS)**
   - Menjawab langsung pertanyaan penelitian (RQ1–RQ3).
   - Rekomendasi kebijakan dan arah riset lanjutan.

10. **PERNYATAAN KETERSEDIAAN DATA & KODE (DATA AND CODE AVAILABILITY)**
    - Tautan repositori publik (GitHub/Zenodo) untuk menjamin prinsip sains terbuka.

11. **DAFTAR PUSTAKA (REFERENCES)**
    - Minimal 20–30 referensi primer.
    - Minimal 80% rujukan terbit dalam 5 tahun terakhir.
    - Gaya sitasi: **IEEE** (penomoran [1], [2]) atau **APA 7th** (Nama, Tahun). Wajib dikelola dengan Reference Manager (Mendeley/Zotero).

---

## 2. KETENTUAN TIPOGRAFI & TATA LETAK

| Parameter Layout | Standar Format SINTA 2 |
| :--- | :--- |
| **Ukuran Kertas** | A4 (210 mm × 297 mm) |
| **Margin Halaman** | Kiri = 2,5 cm, Kanan = 2,5 cm, Atas = 2,5 cm, Bawah = 2,5 cm |
| **Jumlah Kolom** | 1 Kolom (Review Stage) atau 2 Kolom (Camera Ready/JNTETI) |
| **Jenis Font** | Times New Roman (baku) |
| **Ukuran Judul** | 14 pt, Bold, Center |
| **Ukuran Heading 1** | 11–12 pt, Bold, ALL CAPS, Penomoran Angka Romawi atau Arab |
| **Ukuran Heading 2** | 10–11 pt, Bold Italic, Penomoran Abjad atau Sub-desimal (2.1) |
| **Ukuran Teks Isi** | 10–10.5 pt, Justified (Rata Kiri-Kanan), Spasi 1.15 |
| **Indentasi Paragraf**| 0,75–1,0 cm (First Line Indent) |
| **Format Tabel** | **Standar 3-Garis (Three-Line Table)**: Hanya garis horizontal atas, bawah header, dan penutup tabel. Tidak ada garis vertikal. |
| **Format Gambar** | Center, minimal 300 DPI, nomor dan keterangan diletakkan di bawah gambar. |
