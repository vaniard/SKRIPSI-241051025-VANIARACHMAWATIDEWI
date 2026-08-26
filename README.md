# Analisis Sentimen Ulasan Aplikasi Gojek

**Repository Skripsi — 241051025 Vania Rachmawati Dewi**

Repository ini berisi source code, dataset, notebook, dan dashboard yang digunakan dalam penelitian skripsi mengenai **analisis sentimen ulasan pengguna aplikasi Gojek**.

Penelitian ini memanfaatkan data ulasan pengguna sebagai sumber informasi untuk mengetahui kecenderungan sentimen yang terdapat pada ulasan aplikasi Gojek. Data yang diperoleh melalui proses scraping kemudian melalui tahapan pembersihan data, pengolahan teks, analisis sentimen, serta penyajian hasil analisis dalam bentuk visualisasi dan dashboard interaktif.

---

## 🚀 Live Dashboard

Hasil analisis telah diimplementasikan ke dalam dashboard interaktif menggunakan **Streamlit**.

### 🌐 Akses Dashboard

👉 **[Buka Dashboard Analisis Sentimen Ulasan Aplikasi Gojek](https://skripsi-241051025-vaniarachmawatidewi-dp7sfijsxynsjkxclp8efr.streamlit.app/)**

Dashboard digunakan untuk membantu menampilkan hasil pengolahan dan analisis data ulasan secara lebih interaktif sehingga informasi yang diperoleh dapat lebih mudah dipahami.

---

## 📌 Tujuan Penelitian

Penelitian ini bertujuan untuk melakukan analisis terhadap ulasan pengguna aplikasi Gojek dengan memanfaatkan teknik pengolahan data dan analisis teks.

Secara umum, penelitian mencakup beberapa tahapan berikut:

1. Mengumpulkan data ulasan pengguna aplikasi Gojek.
2. Melakukan preprocessing dan pembersihan data ulasan.
3. Melakukan pengolahan teks untuk mempersiapkan data analisis.
4. Melakukan analisis sentimen terhadap ulasan pengguna.
5. Mengelompokkan dan menganalisis hasil ulasan berdasarkan kategori yang digunakan dalam penelitian.
6. Menampilkan hasil analisis dalam bentuk visualisasi.
7. Mengembangkan dashboard interaktif sebagai media penyajian hasil penelitian.

---

## 🔄 Alur Penelitian

```text
Data Ulasan Aplikasi Gojek
          │
          ▼
       Scraping
          │
          ▼
    Data Cleaning
          │
          ▼
   Text Preprocessing
          │
          ▼
    Analisis Sentimen
          │
          ▼
  Kategorisasi Ulasan
          │
          ▼
     Visualisasi Data
          │
          ▼
   Dashboard Streamlit
```

---

## 📂 Struktur Repository

```text
SKRIPSI-241051025-VANIARACHMAWATIDEWI/
│
├── dashboard/
│   └── File-file aplikasi dashboard Streamlit
│
├── Analisis_Sentimen_Ulasan_Aplikasi_Gojek_Skripsi_Vania.ipynb
│   └── Notebook utama analisis sentimen
│
├── Scraping_Data_Ulasan_Aplikasi_Gojek.ipynb
│   └── Notebook proses pengumpulan/scraping data ulasan
│
├── clean_data_ulasan_gojek_baru.csv
│   └── Dataset ulasan yang telah melalui proses pembersihan
│
├── ulasan_gojek_kategori.csv
│   └── Dataset ulasan yang telah dilengkapi hasil kategorisasi
│
├── requirements.txt
│   └── Daftar library/dependency yang digunakan
│
└── README.md
    └── Dokumentasi repository
```

Struktur tersebut sesuai dengan file yang tersedia pada repository GitHub.

---

## 🧰 Teknologi dan Library

Penelitian dan implementasi dashboard menggunakan beberapa teknologi dan library Python, antara lain:

| Teknologi / Library  | Kegunaan                                 |
| -------------------- | ---------------------------------------- |
| **Python**           | Bahasa pemrograman utama                 |
| **Jupyter Notebook** | Eksplorasi dan pengolahan data           |
| **Pandas**           | Manipulasi dan pengolahan dataset        |
| **NumPy**            | Operasi numerik                          |
| **Scikit-learn**     | Pemrosesan dan analisis machine learning |
| **Sastrawi**         | Preprocessing teks Bahasa Indonesia      |
| **Requests**         | Pengambilan data                         |
| **Matplotlib**       | Visualisasi data                         |
| **Seaborn**          | Visualisasi data statistik               |
| **WordCloud**        | Visualisasi kata yang sering muncul      |
| **Streamlit**        | Pengembangan dashboard interaktif        |

Library yang digunakan juga tercantum pada `requirements.txt` repository.

---

## 📊 Dataset

Repository menyediakan beberapa dataset yang digunakan dalam proses penelitian:

### 1. `clean_data_ulasan_gojek_baru.csv`

Dataset ulasan yang telah melalui proses pembersihan data dan digunakan sebagai salah satu sumber dalam tahapan analisis.

### 2. `ulasan_gojek_kategori.csv`

Dataset ulasan yang telah dilengkapi dengan informasi kategorisasi untuk mendukung analisis lebih lanjut.

> **Catatan:** Dataset yang digunakan dalam penelitian merupakan data ulasan pengguna aplikasi Gojek yang dikumpulkan untuk keperluan penelitian akademik.

---

## 📓 Notebook

### Scraping Data

File:

```text
Scraping_Data_Ulasan_Aplikasi_Gojek.ipynb
```

Notebook ini digunakan untuk proses pengumpulan data ulasan aplikasi Gojek sebelum data masuk ke tahapan pengolahan dan analisis.

### Analisis Sentimen

File:

```text
Analisis_Sentimen_Ulasan_Aplikasi_Gojek_Skripsi_Vania.ipynb
```

Notebook ini merupakan notebook utama yang digunakan dalam proses analisis data ulasan dan analisis sentimen penelitian.

---

## 📈 Dashboard

Dashboard dikembangkan menggunakan **Streamlit** untuk menyajikan hasil analisis secara interaktif.

Melalui dashboard, pengguna dapat melihat hasil pengolahan data dan visualisasi yang dihasilkan dari penelitian tanpa harus menjalankan seluruh proses analisis melalui Jupyter Notebook.

### Dashboard Online

👉 **https://skripsi-241051025-vaniarachmawatidewi-dp7sfijsxynsjkxclp8efr.streamlit.app/**

---

## 💻 Instalasi dan Menjalankan Project

Untuk menjalankan project secara lokal, pastikan Python telah terpasang pada komputer.

### 1. Clone Repository

```bash
git clone https://github.com/vaniard/SKRIPSI-241051025-VANIARACHMAWATIDEWI.git
```

### 2. Masuk ke Folder Project

```bash
cd SKRIPSI-241051025-VANIARACHMAWATIDEWI
```

### 3. Install Library

Disarankan menggunakan virtual environment.

```bash
python -m venv venv
```

Aktifkan virtual environment.

**Windows:**

```bash
venv\Scripts\activate
```

**Linux/macOS:**

```bash
source venv/bin/activate
```

Kemudian install seluruh dependency:

```bash
pip install -r requirements.txt
```

### 4. Menjalankan Dashboard

Masuk ke folder dashboard:

```bash
cd dashboard
```

Kemudian jalankan aplikasi Streamlit:

```bash
streamlit run app.py
```

> Nama file utama dashboard dapat disesuaikan dengan file `.py` yang terdapat di dalam folder `dashboard`.

---

## 🧪 Tahapan Pengolahan Data

Secara umum, pengolahan data dalam penelitian dilakukan melalui beberapa tahapan:

### 1. Data Collection

Mengumpulkan ulasan pengguna aplikasi Gojek sebagai data penelitian.

### 2. Data Cleaning

Membersihkan data dari elemen yang tidak diperlukan agar data lebih siap digunakan dalam proses analisis.

### 3. Text Preprocessing

Melakukan persiapan data teks, termasuk proses normalisasi dan preprocessing Bahasa Indonesia dengan bantuan library yang relevan.

### 4. Analisis Sentimen

Melakukan proses klasifikasi atau pelabelan sentimen terhadap ulasan pengguna berdasarkan metode yang digunakan dalam penelitian.

### 5. Kategorisasi

Melakukan pengelompokan ulasan berdasarkan kategori yang digunakan pada penelitian.

### 6. Visualisasi

Hasil pengolahan data divisualisasikan menggunakan grafik dan WordCloud untuk membantu memahami pola yang terdapat dalam data.

### 7. Dashboard

Hasil akhir kemudian disajikan melalui dashboard interaktif berbasis Streamlit.

---

## 📋 Hasil yang Disajikan

Hasil penelitian dapat digunakan untuk melihat berbagai informasi dari data ulasan pengguna, seperti:

* Distribusi sentimen ulasan.
* Perbandingan hasil sentimen.
* Distribusi kategori ulasan.
* Kata-kata yang sering muncul.
* Visualisasi hasil analisis.
* Informasi ringkas mengenai data ulasan.
* Hasil analisis yang disajikan secara interaktif melalui dashboard.

---

## 🎓 Informasi Skripsi

**Nama:** Vania Rachmawati Dewi

**NIM:** 241051025

**Jenis:** Skripsi

**Topik:** Analisis Sentimen Ulasan Aplikasi Gojek

**Platform Dashboard:** Streamlit

---

## 📚 Repository

Source code dan seluruh file penelitian dapat diakses melalui repository GitHub berikut:

👉 **[GitHub Repository](https://github.com/vaniard/SKRIPSI-241051025-VANIARACHMAWATIDEWI)**

---

## 🌐 Demo

**Dashboard Streamlit:**

👉 **[Live Demo Dashboard](https://skripsi-241051025-vaniarachmawatidewi-dp7sfijsxynsjkxclp8efr.streamlit.app/)**

---

## 👩‍💻 Author

**Vania Rachmawati Dewi**

NIM: **241051025**

Repository ini dibuat sebagai bagian dari pelaksanaan penelitian skripsi.

---

## 📄 Lisensi

Project ini dibuat untuk keperluan **akademik dan penelitian skripsi**.

Penggunaan, pengembangan, maupun distribusi ulang kode dan dataset harap memperhatikan sumber data serta tujuan penggunaannya.
