"""
PINTU MASUK APLIKASI (router). Jalankan dengan:  streamlit run app.py

CATATAN PERUBAHAN
- [v5] Memakai st.navigation supaya tab pertama bernama "Pendahuluan", bukan "app".
- [v6] Sidebar (tersembunyi secara default, buka lewat panah kecil di kiri atas) berisi pilihan
       "Ukuran grafik": Kompak / Normal / Besar. Pilihan ini mengalikan tinggi semua grafik (lihat utils.T)
       supaya tiap halaman muat satu layar di laptop kecil maupun layar besar/proyektor.
"""
import streamlit as st

from utils import UKURAN, URUTAN_HALAMAN

st.set_page_config(page_title="Bekerja Saja Belum Cukup", page_icon="📊",
                   layout="wide", initial_sidebar_state="collapsed")

with st.sidebar:
    st.radio("Ukuran grafik", list(UKURAN), index=1, key="ukuran_tampilan",
             help="Pilih Kompak bila halaman terpotong di layar kecil, Besar untuk layar lebar atau proyektor.")

halaman = [st.Page(path, title=judul, default=(i == 0)) for i, (path, judul) in enumerate(URUTAN_HALAMAN)]
st.navigation(halaman).run()
