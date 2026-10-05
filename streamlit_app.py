import streamlit as st

from utils import UKURAN, URUTAN_HALAMAN

st.set_page_config(page_title="Bekerja Saja Belum Cukup", page_icon="📊",
                   layout="wide", initial_sidebar_state="collapsed")

with st.sidebar:
    st.radio("Ukuran grafik", list(UKURAN), index=1, key="ukuran_tampilan",
             help="Pilih Kompak bila halaman terpotong di layar kecil, Besar untuk layar lebar atau proyektor.")

halaman = [st.Page(path, title=judul, default=(i == 0)) for i, (path, judul) in enumerate(URUTAN_HALAMAN)]
st.navigation(halaman).run()
