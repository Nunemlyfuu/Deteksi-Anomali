# Deteksi-Anomali
An assignment for one of my courses, it is an anomaly detection using a classification

# 📊 Analisis Kemiripan Paket Pengadaan (SiRUP)

## 📌 Deskripsi Proyek

Proyek ini bertujuan untuk menganalisis kemiripan paket pengadaan berdasarkan data dari SiRUP (Sistem Informasi Rencana Umum Pengadaan). Analisis dilakukan menggunakan pendekatan **similarity berbasis teks** dan **klasifikasi sederhana dengan weighted scoring**.

Fokus utama:

* Mengidentifikasi paket dengan **nama yang mirip**
* Menemukan kasus **“mirip tapi berbeda”**
* Melakukan analisis terhadap **perbedaan anggaran dan atribut organisasi**

---

## 🧠 Metodologi

### A. Pre-processing & Similarity Labelling

1. **Data Cleaning**

   * Normalisasi nama kolom
   * Cleaning teks pada kolom *Nama Paket*:

     * Lowercase
     * Hapus simbol
     * Normalisasi spasi

2. **Similarity Calculation**

   * Menggunakan:

     * **TF-IDF Vectorization**
     * **Cosine Similarity**
   * Hanya menggunakan **Nama Paket** (sesuai instruksi tugas)

3. **Threshold**

   * Similarity > 0.8 → kandidat *mirip*
   * ≤ 0.8 → dianggap *tidak mirip*

4. **Semi-Manual Labelling**

   * Sample ±30 data
   * Label:

     * `mirip`
     * `tidak`

---

### B. Klasifikasi dengan Weighted Scoring

Karena dataset tidak memiliki kolom *uraian pekerjaan* dan *metode pengadaan*, maka digunakan atribut alternatif:

| Fitur        | Tipe                      | Bobot |
| ------------ | ------------------------- | ----- |
| Nama Paket   | Text (Cosine Similarity)  | 0.6   |
| K/L/PD       | Categorical (Exact Match) | 0.2   |
| Satuan Kerja | Categorical (Exact Match) | 0.2   |

#### Formula:

```
Final Score = 
0.6 × Nama Similarity +
0.2 × K/L/PD Match +
0.2 × Satuan Kerja Match
```

#### Klasifikasi:

* `Final Score > 0.8` → **mirip**
* lainnya → **tidak**

#### Alasan Pembobotan:

* **Nama Paket (0.6)** → representasi utama pengadaan
* **K/L/PD (0.2)** → menunjukkan instansi
* **Satuan Kerja (0.2)** → unit pelaksana yang lebih spesifik

Pendekatan ini dipilih karena:

* Sederhana
* Mudah diinterpretasikan
* Tidak membutuhkan data training besar

---

### C. Analisis & Visualisasi

Analisis difokuskan pada kasus:

## 🔥 “Mirip tapi Berbeda”

Kriteria:

* Similarity tinggi (mirip)
* Namun:

  * **Perbedaan anggaran > 50%**
  * atau **berbeda instansi / satker**

#### Perhitungan:

```
Budget Difference = |A - B| / max(A, B)
```

---

## 📊 Hasil Analisis

### 1. Distribusi Perbedaan Anggaran

* Mayoritas kasus berada pada rentang **70% – 95%**
* Terdapat kasus mendekati **100% perbedaan**

### 2. Insight Utama

> Paket dengan nama yang mirip tidak selalu memiliki anggaran yang serupa.

Interpretasi:

* Perbedaan skala proyek
* Perbedaan lokasi
* Perbedaan lingkup pekerjaan
* Penamaan yang terlalu umum

---

## 📁 Struktur Project

```
/project
│
├── sirup_merged.csv
├── similar_pairs_nama.csv
├── label_sample.csv
├── final_classification.csv
├── anomaly_cases.csv
│
├── pre_processing.py
├── weighted_scoring.py
├── analysis.py
│
└── README.md
```

---

## ⚙️ Cara Menjalankan

### 1. Pre-processing & Similarity

```
python pre_processing.py
```

Output:

* `similar_pairs_nama.csv`
* `label_sample.csv`

---

### 2. Weighted Scoring

```
python weighted_scoring.py
```

Output:

* `final_classification.csv`

---

### 3. Analisis

```
python analysis.py
```

Output:

* `anomaly_cases.csv`
* Visualisasi histogram

---

## 🎯 Kesimpulan

* Similarity berbasis nama efektif untuk menemukan kandidat paket mirip
* Namun:

  * Tidak cukup untuk memahami karakteristik pengadaan
* Dibutuhkan kombinasi fitur tambahan (instansi, satker)
* Ditemukan banyak kasus:

  * **Nama mirip, anggaran sangat berbeda**

---

## 📱 Output Publikasi (Instagram)

Highlight:

* “Nama Sama ≠ Anggaran Sama”
* Perbandingan paket mirip dengan perbedaan signifikan
* Visualisasi distribusi anggaran

---

## 👨‍💻 Author

Najwan Firdaus

---

## 📌 Catatan

Proyek ini dibuat untuk keperluan akademik dalam analisis data pengadaan berbasis similarity dan klasifikasi sederhana.
