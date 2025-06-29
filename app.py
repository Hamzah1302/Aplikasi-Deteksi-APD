import streamlit as st
from ultralytics import YOLO
import cv2
import tempfile
import numpy as np
import os

# --- KONFIGURASI HALAMAN STREAMLIT ---
st.set_page_config(
    page_title="Deteksi APD | Smart Industrial Safety",
    page_icon="👷",
    layout="wide"
)

# --- JUDUL DAN DESKRIPSI APLIKASI ---
st.title("👷 Smart Helmet & Vest Detection System")
st.write("""
Aplikasi ini menggunakan model **YOLOv8** untuk mendeteksi Alat Pelindung Diri (APD) 
dan menghitung jumlah pelanggaran secara *real-time*. Model sudah dimuat secara otomatis.
""")

# --- FUNGSI UNTUK MEMUAT MODEL (PENTING!) ---
@st.cache_resource # Ini adalah dekorator Streamlit untuk caching, agar model hanya di-load sekali.
def load_yolo_model(model_path):
    """
    Memuat model YOLO dari path yang diberikan. Fungsi ini di-cache untuk performa.
    """
    try:
        model = YOLO(model_path)
        return model
    except FileNotFoundError:
        st.error(f"Error: File model tidak ditemukan di '{model_path}'.")
        st.error("Pastikan file 'best.pt' berada di folder yang sama dengan 'app.py' saat Anda mendeploy.")
        return None
    except Exception as e:
        st.error(f"Gagal memuat model: {e}")
        return None

# --- FUNGSI UNTUK MEMPROSES STREAM VIDEO/WEBCAM ---
def process_video_stream(source, model, confidence):
    """
    Memproses stream video dari file atau webcam, melakukan deteksi,
    menghitung objek, dan menampilkan hasilnya.
    """
    cap = cv2.VideoCapture(source)
    if not cap.isOpened():
        st.error("Gagal membuka sumber video/webcam.")
        return

    # Buat placeholder untuk video dan statistik
    col1, col2 = st.columns([3, 1])
    with col1:
        st_frame = st.empty()
    with col2:
        st_stats = st.empty()

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            st.info("Stream video berakhir atau file selesai diproses.")
            break

        # Lakukan deteksi pada setiap frame
        results = model.predict(frame, conf=confidence, verbose=False)
        annotated_frame = frame.copy()
        
        person_count = 0
        helmet_count = 0
        vest_count = 0

        # Iterasi melalui hasil deteksi
        for r in results:
            annotated_frame = r.plot() # Menggambar bounding box
            boxes = r.boxes
            for box in boxes:
                cls_id = int(box.cls[0])
                # Mengubah nama kelas ke huruf kecil untuk konsistensi
                class_name = model.names[cls_id].lower()
                
                # --- PERBAIKAN LOGIKA PENGHITUNGAN ---
                if class_name == "person":
                    person_count += 1
                elif class_name == "helmet":
                    helmet_count += 1
                elif class_name == "vest":
                    vest_count += 1
        
        # --- LOGIKA BARU: MENENTUKAN JUMLAH ORANG EFEKTIF ---
        effective_person_count = max(person_count, helmet_count, vest_count)
        
        helmet_warning = effective_person_count > helmet_count
        vest_warning = effective_person_count > vest_count
        
        st_frame.image(annotated_frame, channels="BGR", use_container_width=True)

        with st_stats:
            st.subheader("📊 Statistik Real-Time")
            st.metric("Orang Terdeteksi (Efektif)", effective_person_count)
            
            # Tampilkan metrik helm dengan status
            st.metric("Helm Terdeteksi", f"{helmet_count}/{effective_person_count}", 
                      delta="PELANGGARAN!" if helmet_warning else "Aman", 
                      delta_color="inverse" if helmet_warning else "normal")
            
            # Tampilkan metrik rompi dengan status
            st.metric("Rompi Terdeteksi", f"{vest_count}/{effective_person_count}", 
                      delta="PELANGGARAN!" if vest_warning else "Aman", 
                      delta_color="inverse" if vest_warning else "normal")

            # Berikan peringatan spesifik untuk setiap jenis pelanggaran
            if helmet_warning:
                st.warning("⚠️ PELANGGARAN HELM: Terdeteksi ada pekerja tidak memakai helm!", icon="⛑️")
            
            if vest_warning:
                st.warning("⚠️ PELANGGARAN ROMPI: Terdeteksi ada pekerja tidak memakai rompi!", icon="🦺")

    cap.release()

# --- FUNGSI UTAMA APLIKASI ---
def main():
    # Path ke model Anda. PENTING: File 'best.pt' harus ada di folder yang sama
    # dengan file app.py ini saat di-deploy.
    MODEL_PATH = "best.pt" 

    # Muat model menggunakan fungsi yang sudah di-cache
    model = load_yolo_model(MODEL_PATH)

    # Jika model gagal dimuat, hentikan aplikasi
    if model is None:
        st.stop()

    # Sidebar untuk pengaturan
    with st.sidebar:
        st.header("⚙️ Pengaturan")
        confidence = st.slider("Ambang Batas Kepercayaan (Confidence)", 0.0, 1.0, 0.5, 0.05)
        st.info(f"✅ Model `{MODEL_PATH}` sudah otomatis dimuat.")
        st.write("---")
        if st.button("📘 Panduan Penggunaan"):
            st.info("""
            - Gunakan webcam atau unggah gambar/video.
            - Sistem akan hitung jumlah pekerja & APD.
            - Pelanggaran = Orang > helm/rompi.
            - Format didukung: JPG, PNG, MP4, AVI.
            """)

    source_option = st.radio("Pilih Sumber Input:", ('Gambar', 'Video', 'Webcam'), horizontal=True)
    st.write("---")

    if source_option == 'Gambar':
        uploaded_file = st.file_uploader("Unggah sebuah gambar...", type=["jpg", "jpeg", "png"])
        if uploaded_file:
            bytes_data = uploaded_file.getvalue()
            image = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)
            
            with st.spinner("🔍 Mendeteksi..."):
                results = model.predict(image, conf=confidence, verbose=False)
                annotated_image = results[0].plot()

                # --- LOGIKA BARU UNTUK STATISTIK GAMBAR ---
                person_count = 0
                helmet_count = 0
                vest_count = 0

                # Iterasi melalui hasil deteksi untuk menghitung objek
                for r in results:
                    boxes = r.boxes
                    for box in boxes:
                        cls_id = int(box.cls[0])
                        class_name = model.names[cls_id].lower()
                        # --- PERBAIKAN LOGIKA PENGHITUNGAN ---
                        if class_name == "person":
                            person_count += 1
                        elif class_name == "helmet":
                            helmet_count += 1
                        elif class_name == "vest":
                            vest_count += 1
                
                # --- LOGIKA BARU: MENENTUKAN JUMLAH ORANG EFEKTIF ---
                effective_person_count = max(person_count, helmet_count, vest_count)
                
                helmet_warning = effective_person_count > helmet_count
                vest_warning = effective_person_count > vest_count
                # --- AKHIR LOGIKA BARU ---

            # Layout baru untuk menampilkan gambar dan statistik
            col1, col2 = st.columns([3, 1])
            with col1:
                st.image(annotated_image, caption="✅ Hasil Deteksi", channels="BGR", use_container_width=True)
            
            with col2:
                st.subheader("📊 Statistik Gambar")
                st.metric("Orang Terdeteksi (Efektif)", effective_person_count)
                
                st.metric("Helm Terdeteksi", f"{helmet_count}/{effective_person_count}", 
                          delta="PELANGGARAN!" if helmet_warning else "Aman", 
                          delta_color="inverse" if helmet_warning else "normal")
                
                st.metric("Rompi Terdeteksi", f"{vest_count}/{effective_person_count}", 
                          delta="PELANGGARAN!" if vest_warning else "Aman", 
                          delta_color="inverse" if vest_warning else "normal")

                if helmet_warning:
                    st.warning("⚠️ PELANGGARAN HELM: Terdeteksi ada pekerja tidak memakai helm!", icon="⛑️")
                
                if vest_warning:
                    st.warning("⚠️ PELANGGARAN ROMPI: Terdeteksi ada pekerja tidak memakai rompi!", icon="🦺")

    elif source_option == 'Video':
        uploaded_file = st.file_uploader("Unggah sebuah video...", type=["mp4", "mov", "avi"])
        if uploaded_file:
            tfile = tempfile.NamedTemporaryFile(delete=False)
            tfile.write(uploaded_file.read())
            video_path = tfile.name
            process_video_stream(video_path, model, confidence)
            os.remove(video_path) # Hapus file video sementara setelah selesai

    elif source_option == 'Webcam':
        st.info("Klik tombol di bawah untuk mulai webcam:")
        if st.button("📷 Mulai Deteksi Webcam"):
            process_video_stream(0, model, confidence)

if __name__ == "__main__":
    main()
