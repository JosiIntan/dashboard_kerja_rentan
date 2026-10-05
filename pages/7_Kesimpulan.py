import streamlit as st

from konten import GITHUB_URL, JUDUL, P7_KESIMPULAN, P7_KETERBATASAN, PENULIS
from utils import fmt_id, judul_halaman, kartu, muat, nav_bawah, tengah_vertikal, terapkan_gaya, ubin

terapkan_gaya()
tengah_vertikal()
judul_halaman(JUDUL["p7"])

prov = muat("provinsi_indikator.csv")
pp = prov[prov.provinsi == "Papua Pegunungan"].iloc[0]

kiri, kanan = st.columns([2.4, 1])
with kiri:
    with kartu("kesimpulan"):
        st.markdown(f"<p class='teks-rata' style='font-size:1.02rem;line-height:1.65;margin:0;'>{P7_KESIMPULAN}</p>",
                    unsafe_allow_html=True)
with kanan:
    with kartu("angka"):
        st.markdown("##### Papua Pegunungan dalam angka")
        st.markdown(ubin([
            ("TPAK", f"{fmt_id(pp.tpak)} %", "besar"),
            ("TPT", f"{fmt_id(pp.tpt)} %", "besar"),
            ("Pekerja informal", f"{fmt_id(pp.informal)} %", "besar"),
            ("IPM", fmt_id(pp.ipm), "besar"),
        ], kolom=2), unsafe_allow_html=True)

with kartu("keterbatasan"):
    st.markdown("##### Keterbatasan")
    st.markdown(f"<p class='teks-rata' style='font-size:0.95rem;line-height:1.55;margin:0;'>{P7_KETERBATASAN}</p>",
                unsafe_allow_html=True)

baris = []
baris.append(PENULIS)
st.caption("  \n".join(baris))

nav_bawah("pages/7_Kesimpulan.py")
