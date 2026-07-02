import streamlit as st
import pandas as pd
from datetime import datetime

# Konfigurasi Halaman
st.set_page_config(page_title="Rapor & Jurnal Guru - Pak Dimas", layout="wide")

# Judul Aplikasi
st.title("📝 Aplikasi Manajemen Kelas & Penilaian Kurikulum Merdeka")
st.subheader("Oleh: Dimas Fajar Ariyanto Putra, S.Pd. | SMA Negeri 13 Banjarmasin")
st.markdown("---")

# Inisialisasi Data Menggunakan Session State (Agar data tidak hilang saat aplikasi di-refresh di sesi yang sama)
if 'data_murid' not in st.session_state:
    st.session_state.data_murid = pd.DataFrame(columns=["NISN", "Nama Murid", "Kelas"])
if 'daftar_hadir' not in st.session_state:
    st.session_state.daftar_hadir = pd.DataFrame(columns=["Tanggal", "Nama Murid", "Status"])
if 'cp_tp_atp' not in st.session_state:
    st.session_state.cp_tp_atp = pd.DataFrame(columns=["Elemen CP", "Tujuan Pembelajaran (TP)", "Alur (ATP)"])
if 'nilai' not in st.session_state:
    st.session_state.nilai = pd.DataFrame(columns=["Nama Murid", "Jenis Asesmen", "TP / Materi", "Nilai"])
if 'catatan' not in st.session_state:
    st.session_state.catatan = pd.DataFrame(columns=["Nama Murid", "Tanggal", "Catatan Perkembangan"])

# Menu Navigasi di Sidebar
menu = st.sidebar.selectbox(
    "Pilih Menu Aplikasi:",
    ["👥 Data Murid", "📅 Daftar Hadir", "📘 CP, TP, & ATP", "💯 Input Nilai", "📝 Catatan Murid"]
)

# ----------------------------------------------------
# 1. MENU: DATA MURID
# ----------------------------------------------------
if menu == "👥 Data Murid":
    st.header("👥 Manajemen Data Murid")
    
    with st.form("form_murid", clear_on_submit=True):
        nisn = st.text_input("NISN / NIS")
        nama = st.text_input("Nama Lengkap Murid")
        kelas = st.selectbox("Kelas", ["X-1", "X-2", "XI-Fase F1", "XI-Fase F2", "XII-1", "XII-2"])
        submit_murid = st.form_submit_button("Simpan Data Murid")
        
        if submit_murid and nama and nisn:
            baru = pd.DataFrame([{"NISN": nisn, "Nama Murid": nama, "Kelas": kelas}])
            st.session_state.data_murid = pd.concat([st.session_state.data_murid, baru], ignore_index=True)
            st.success(f"Data {nama} berhasil ditambahkan!")

    st.subheader("Daftar Murid Terdaftar")
    st.dataframe(st.session_state.data_murid, use_container_width=True)

# ----------------------------------------------------
# 2. MENU: DAFTAR HADIR
# ----------------------------------------------------
elif menu == "📅 Daftar Hadir":
    st.header("📅 Input Daftar Hadir Siswa")
    
    if st.session_state.data_murid.empty:
        st.warning("Silakan isi data murid terlebih dahulu di menu 'Data Murid'.")
    else:
        tanggal = st.date_input("Tanggal Hari Ini", datetime.now())
        
        st.write("Isi Kehadiran:")
        kehadiran_list = []
        for index, row in st.session_state.data_murid.iterrows():
            status = st.radio(f"{row['Nama Murid']} ({row['Kelas']})", ["Hadir", "Sakit", "Izin", "Alpa"], key=f"absen_{index}", horizontal=True)
            kehadiran_list.append({"Tanggal": tanggal, "Nama Murid": row['Nama Murid'], "Status": status})
            
        if st.button("Simpan Presensi Hari Ini"):
            baru_hadir = pd.DataFrame(kehadiran_list)
            st.session_state.daftar_hadir = pd.concat([st.session_state.daftar_hadir, baru_hadir], ignore_index=True)
            st.success("Daftar hadir berhasil disimpan!")
            
    st.subheader("Rekap Presensi")
    st.dataframe(st.session_state.daftar_hadir, use_container_width=True)

# ----------------------------------------------------
# 3. MENU: CP, TP, & ATP
# ----------------------------------------------------
elif menu == "📘 CP, TP, & ATP":
    st.header("📘 Capaian, Tujuan, & Alur Tujuan Pembelajaran")
    
    with st.form("form_kurikulum", clear_on_submit=True):
        elemen = st.selectbox("Elemen Capaian Pembelajaran (CP) Bahasa Indonesia", 
                              ["Menyimak", "Membaca dan Memirsa", "Berbicara dan Presentasi", "Menulis"])
        tp = st.text_area("Tujuan Pembelajaran (TP)", placeholder="Contoh: Peserta didik mampu mengevaluasi gagasan dan pandangan berdasarkan teks monolog...")
        atp = st.text_input("Alur Tujuan Pembelajaran (Urutan/Kode ATP)", placeholder="Contoh: ATP 11.1")
        submit_kur = st.form_submit_button("Simpan Target Pembelajaran")
        
        if submit_kur and tp and atp:
            baru_kur = pd.DataFrame([{"Elemen CP": elemen, "Tujuan Pembelajaran (TP)": tp, "Alur (ATP)": atp}])
            st.session_state.cp_tp_atp = pd.concat([st.session_state.cp_tp_atp, baru_kur], ignore_index=True)
            st.success("Target Kurikulum Berhasil Ditambahkan!")
            
    st.subheader("Matriks CP, TP, dan ATP")
    st.dataframe(st.session_state.cp_tp_atp, use_container_width=True)

# ----------------------------------------------------
# 4. MENU: INPUT NILAI
# ----------------------------------------------------
elif menu == "💯 Input Nilai":
    st.header("💯 Input Nilai Formatif & Sumatif")
    
    if st.session_state.data_murid.empty:
        st.warning("Silakan isi data murid terlebih dahulu.")
    else:
        with st.form("form_nilai", clear_on_submit=True):
            murid_pilihan = st.selectbox("Pilih Murid", st.session_state.data_murid["Nama Murid"].tolist())
            jenis_asesmen = st.selectbox("Jenis Asesmen", ["Formatif (Tugas/Kuis)", "Sumatif Lingkup Materi", "Sumatif Akhir Semester"])
            
            # Mengambil referensi ATP jika ada
            if not st.session_state.cp_tp_atp.empty:
                materi_pilihan = st.selectbox("Berdasarkan ATP / Kode TP", st.session_state.cp_tp_atp["Alur (ATP)"].tolist())
            else:
                materi_pilihan = st.text_input("Materi / Kompetensi (Isi manual jika menu CP/TP kosong)")
                
            nilai_angka = st.number_input("Nilai (0-100)", min_value=0, max_value=100, value=80)
            submit_nilai = st.form_submit_button("Simpan Nilai")
            
            if submit_nilai:
                baru_nilai = pd.DataFrame([{"Nama Murid": murid_pilihan, "Jenis Asesmen": jenis_asesmen, "TP / Materi": materi_pilihan, "Nilai": nilai_angka}])
                st.session_state.nilai = pd.concat([st.session_state.nilai, baru_nilai], ignore_index=True)
                st.success(f"Nilai untuk {murid_pilihan} berhasil direkam.")
                
    st.subheader("Buku Nilai Guru")
    st.dataframe(st.session_state.nilai, use_container_width=True)

# ----------------------------------------------------
# 5. MENU: CATATAN MURID
# ----------------------------------------------------
elif menu == "📝 Catatan Murid":
    st.header("📝 Catatan Jurnal & Perkembangan Murid")
    
    if st.session_state.data_murid.empty:
        st.warning("Silakan isi data murid terlebih dahulu.")
    else:
        with st.form("form_catatan", clear_on_submit=True):
            murid_pilihan_catat = st.selectbox("Pilih Murid", st.session_state.data_murid["Nama Murid"].tolist())
            tgl_catat = st.date_input("Tanggal Kejadian", datetime.now())
            isi_catatan = st.text_area("Catatan Perilaku / Progres Akademik", placeholder="Contoh: Menunjukkan peningkatan pesat dalam menulis teks opini, namun perlu bimbingan pada struktur konjungsi.")
            submit_catatan = st.form_submit_button("Simpan Catatan Jurnal")
            
            if submit_catatan and isi_catatan:
                baru_catat = pd.DataFrame([{"Nama Murid": murid_pilihan_catat, "Tanggal": tgl_catat, "Catatan Perkembangan": isi_catatan}])
                st.session_state.catatan = pd.concat([st.session_state.catatan, baru_catat], ignore_index=True)
                st.success(f"Catatan untuk {murid_pilihan_catat} berhasil disimpan.")
                
    st.subheader("Jurnal Anekdot / Catatan Guru")
    st.dataframe(st.session_state.catatan, use_container_width=True)