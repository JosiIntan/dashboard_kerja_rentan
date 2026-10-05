"""
HALAMAN 2 - DEFINISI BEKERJA

CATATAN PERUBAHAN
- [v5] Legenda akar/level 1/level 2 dihapus. Keterangan bawah diambil dari konten.py (P2_CAPTION).
- [v5] Kotak diagram dilebarkan (0.14 per huruf) supaya teks tidak terpotong lagi.
- [v6.1] Diagram jadi SVG responsif (teks ikut mengecil bersama kotak).
- [v6] Diagram diperbesar karena halaman ini punya ruang kosong; judul memakai judul_halaman().
"""
import streamlit as st

from konten import JUDUL, P2_CAPTION
from utils import (ABU, TEKS_LEVEL, WARNA_LEVEL, WARNA_ROOT, T, judul_halaman, kartu, nav_bawah,
                   tengah_vertikal, terapkan_gaya)

terapkan_gaya()
tengah_vertikal()

kiri, kanan = st.columns([1, 1.55])

with kiri:
    with kartu("definisi"):
        judul_halaman(JUDUL["p2"])
        st.markdown("#### Definisi BPS")
        st.markdown(
            "<div class='sorot teks-rata'>"
            "Bekerja adalah kegiatan ekonomi yang dilakukan dengan maksud memperoleh "
            "atau membantu memperoleh pendapatan atau keuntungan, paling sedikit "
            "<b>1 jam</b> dalam seminggu terakhir.</div>",
            unsafe_allow_html=True)

with kanan:
    # [v6.1] Diagram digambar sebagai SVG: kotak + huruf mengecil BERSAMA di layar kecil, jadi tidak pernah bertabrakan.
    pohon = {
        "Penduduk": ["Usia Kerja", "Bukan Usia Kerja"],
        "Usia Kerja": ["Angkatan Kerja", "Bukan Angkatan Kerja"],
        "Bukan Usia Kerja": [],
        "Angkatan Kerja": ["Bekerja", "Pengangguran"],
        "Bukan Angkatan Kerja": ["Sekolah", "Mengurus RT", "Lainnya"],
        "Bekerja": [], "Pengangguran": [], "Sekolah": [], "Mengurus RT": [], "Lainnya": [],
    }
    FS, JARAK, TINGGI_LEVEL, TINGGI_KOTAK = 0.24, 0.22, 1.5, 0.74      # semua dalam satuan viewBox

    def baris_label(teks):
        """Label panjang dipecah jadi 2 baris di spasi yang paling dekat dengan tengah."""
        kata = teks.split(" ")
        if len(teks) <= 10 or len(kata) == 1:
            return [teks]
        k = min(range(1, len(kata)), key=lambda i: abs(len(" ".join(kata[:i])) - len(" ".join(kata[i:]))))
        return [" ".join(kata[:k]), " ".join(kata[k:])]

    def lebar_label(teks):
        return max(len(b) for b in baris_label(teks)) * FS * 0.64 + 0.45

    posisi = {}

    def letakkan(node, x_kiri):
        anak = pohon[node]
        if not anak:
            posisi[node] = x_kiri + lebar_label(node) / 2
            return x_kiri + lebar_label(node)
        x, xs = x_kiri, []
        for a in anak:
            x = letakkan(a, x)
            xs.append(posisi[a])
            x += JARAK
        posisi[node] = sum(xs) / len(xs)
        return x - JARAK

    lebar_total = letakkan("Penduduk", 0)

    def hitung_level(n, lvl=0):
        d = {n: lvl}
        for a in pohon[n]:
            d.update(hitung_level(a, lvl + 1))
        return d
    level = hitung_level("Penduduk")

    def y_tengah(n):
        return level[n] * TINGGI_LEVEL + TINGGI_KOTAK / 2

    garis, kotak, teks = [], [], []
    for induk, anak in pohon.items():
        for a in anak:
            garis.append(f"<line x1='{posisi[induk]:.3f}' y1='{y_tengah(induk) + TINGGI_KOTAK / 2:.3f}' "
                         f"x2='{posisi[a]:.3f}' y2='{y_tengah(a) - TINGGI_KOTAK / 2:.3f}' stroke='{ABU}' stroke-width='0.035'/>")
    for n in pohon:
        x, y, w, lv = posisi[n], y_tengah(n), lebar_label(n), level[n]
        warna = WARNA_ROOT if lv == 0 else WARNA_LEVEL[lv]
        kotak.append(f"<rect x='{x - w / 2:.3f}' y='{y - TINGGI_KOTAK / 2:.3f}' width='{w:.3f}' height='{TINGGI_KOTAK}' "
                     f"rx='0.09' fill='{warna}'/>")
        b = baris_label(n)
        tspans = "".join(f"<tspan x='{x:.3f}' y='{y + (i - (len(b) - 1) / 2) * FS * 1.15:.3f}'>{t}</tspan>"
                         for i, t in enumerate(b))
        teks.append(f"<text class='svg-teks' font-size='{FS}' font-weight='700' text-anchor='middle' "
                    f"dominant-baseline='central' fill='{TEKS_LEVEL[lv]}'>{tspans}</text>")

    tinggi_vb = 3 * TINGGI_LEVEL + TINGGI_KOTAK
    svg = (f"<svg viewBox='-0.15 -0.15 {lebar_total + 0.3:.3f} {tinggi_vb + 0.3:.3f}' role='img' "
           f"aria-label='Diagram struktur klasifikasi ketenagakerjaan' "
           f"style='display:block;margin:0 auto;width:100%;height:auto;max-height:{T(420)}px'>"
           + "".join(garis) + "".join(kotak) + "".join(teks) + "</svg>")
    with kartu("pohon"):
        st.markdown(svg, unsafe_allow_html=True)
        st.caption(P2_CAPTION)

nav_bawah("pages/2_Definisi_Bekerja.py")
