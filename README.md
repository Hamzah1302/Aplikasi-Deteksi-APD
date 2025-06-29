# Smart Helmet & Vest Detection System (Aplikasi Deteksi APD)

Aplikasi berbasis web yang dibangun menggunakan Streamlit dan YOLOv8 untuk mendeteksi penggunaan Alat Pelindung Diri (APD) seperti helm dan rompi pada pekerja secara *real-time*. Sistem ini dapat menganalisis gambar, video, atau input dari webcam untuk memastikan kepatuhan terhadap standar keselamatan di lingkungan kerja.

**[Lihat Aplikasi Langsung](https://aplikasi-deteksi-apd.streamlit.app/)**

## 🌟 Fitur Utama

- **Deteksi Real-Time**: Menganalisis gambar, file video (MP4, AVI), dan stream webcam secara langsung.
- **Model YOLOv8**: Menggunakan model deteksi objek YOLOv8 yang canggih untuk akurasi tinggi.
- **Statistik Pelanggaran**: Menghitung jumlah pekerja, helm, dan rompi yang terdeteksi, serta secara otomatis mengidentifikasi jumlah pelanggaran.
- **Antarmuka Interaktif**: Dibuat dengan Streamlit, menyediakan antarmuka yang ramah pengguna untuk mengunggah file dan melihat hasil.
- **Pengaturan Fleksibel**: Pengguna dapat menyesuaikan ambang batas kepercayaan (confidence threshold) untuk deteksi.

## 🛠️ Teknologi yang Digunakan

- **Bahasa Pemrograman**: Python
- **Framework Aplikasi Web**: Streamlit
- **Model Deteksi Objek**: Ultralytics YOLOv8
- **Pemrosesan Gambar**: OpenCV
- **Pustaka Lainnya**: NumPy

## 🚀 Cara Menjalankan Secara Lokal

Untuk menjalankan aplikasi ini di komputer lokal Anda, ikuti langkah-langkah berikut:

### 1. Prasyarat

- **Python 3.8+**
- **pip** (manajer paket Python)
- Opsional: Git untuk kloning repositori.
- **Dependensi Sistem (untuk beberapa lingkungan Linux)**:

```bash
sudo apt-get update && sudo apt-get install -y libgl1-mesa-glx
```

### 2. Kloning Repositori & Instalasi Dependensi

```bash
# Kloning repositori (atau unduh file secara manual)
git clone https://github.com/hamzah1302/aplikasi-deteksi-apd.git
cd aplikasi-deteksi-apd

# (Disarankan) Buat dan aktifkan virtual environment
python -m venv venv
source venv/bin/activate  # Untuk Windows: venv\Scripts\activate

# Instal pustaka Python yang dibutuhkan
pip install -r requirements.txt
```

### 3. Unduh Model

Aplikasi ini memerlukan file bobot model YOLOv8 yang telah dilatih.

- Unduh file `best.pt`.
- **Penting**: Letakkan file `best.pt` di dalam direktori root proyek (folder yang sama dengan file `app.py`).

### 4. Jalankan Aplikasi Streamlit

Setelah semua dependensi terinstal dan model sudah diletakkan di folder yang benar, jalankan perintah berikut dari terminal Anda:

```bash
streamlit run app.py
```

Aplikasi akan terbuka secara otomatis di browser web default Anda.

## 📦 Dependensi Proyek

### Dependensi Python

Daftar pustaka Python yang diperlukan tercantum dalam `requirements.txt`:

- `streamlit`
- `ultralytics`
- `opencv-python-headless`
- `numpy>=1.26.0`

### Dependensi Sistem

Untuk deployment di platform seperti Streamlit Community Cloud, paket sistem tambahan mungkin diperlukan:

- `libgl1-mesa-glx`

## 📄 Struktur File

```
.
├── app.py              # Kode utama aplikasi Streamlit
├── best.pt             # File model YOLOv8 (perlu diunduh)
├── requirements.txt    # Dependensi Python untuk pip
├── packages.txt        # Dependensi sistem untuk Streamlit Cloud
└── README.md
```

## 👨‍💻 Kontributor

- **Hamzah** - hamzah1302
