import circlify
import streamlit as st
import streamlit.components.v1 as components

from komponen import icicle_zoom
from konten import JUDUL, P3_INTRO, SUMBER
from utils import (TEKS_LEVEL, WARNA_LEVEL, WARNA_ROOT, T, fmt_id, judul_halaman, kartu, muat, nav_bawah,
                   sumber_link, terapkan_gaya)

terapkan_gaya()

tren = muat("nasional_tren.csv")
tren["tahun"] = tren["tahun"].astype(int)

kol_judul, kol_tahun = st.columns([3.2, 1])
with kol_judul:
    judul_halaman(JUDUL["p3"], P3_INTRO)
with kol_tahun:
    tahun_pilih = st.selectbox("Tahun", sorted(tren.tahun.unique(), reverse=True), index=0, format_func=str)
r = tren[tren.tahun == tahun_pilih].iloc[0]
total = r.penduduk

STRUKTUR = {
    "Penduduk": (0, {
        "Usia Kerja": (1, {
            "Angkatan Kerja": (2, {"Bekerja": (3, {}), "Pengangguran": (3, {})}),
            "Bukan Angkatan Kerja": (2, {"Sekolah": (3, {}), "Mengurus RT": (3, {}), "Lainnya": (3, {})}),
        }),
        "Bukan Usia Kerja": (1, {}),
    }),
}
NILAI = {
    "Penduduk": total,
    "Usia Kerja": r.usia_bekerja, "Bukan Usia Kerja": r.bukan_usia_kerja,
    "Angkatan Kerja": r.angkatan_kerja, "Bukan Angkatan Kerja": r.bukan_angkatan_kerja,
    "Bekerja": r.bekerja, "Pengangguran": r.penganggur,
    "Sekolah": r.sekolah, "Mengurus RT": r.mengurus_rt, "Lainnya": r.lainnya,
}
LEVEL = {}


def daftar(nama, info):
    LEVEL[nama] = info[0]
    for a, i in info[1].items():
        daftar(a, i)


daftar("Penduduk", STRUKTUR["Penduduk"])

TINGGI = T(320)


def pecah_label(nama, radius):
    """Pilih pemenggalan baris + ukuran huruf (satuan viewBox SVG) agar teks muat di dalam lingkaran."""
    kata = nama.split(" ")
    kandidat = [[nama]] + [[" ".join(kata[:k]), " ".join(kata[k:])] for k in range(1, len(kata))]
    terbaik = None
    for baris in kandidat:
        lebar_em = max(len(b) for b in baris) * 0.6
        fs = min(0.078, 0.78 * 2 * radius / lebar_em, 0.62 * 2 * radius / (1.2 * len(baris)))
        if terbaik is None or fs > terbaik[1]:
            terbaik = (baris, fs)
    return terbaik


c1, c2 = st.columns(2)

# ===================== KIRI: CIRCLE PACKING (SVG responsif) =====================
with c1:
    def ke_circlify(nama, info):
        node = {"id": nama, "datum": NILAI[nama]}
        if info[1]:
            node["children"] = [ke_circlify(a, i) for a, i in info[1].items()]
        return node

    circles = circlify.circlify([ke_circlify("Penduduk", STRUKTUR["Penduduk"])], show_enclosure=False,
                                target_enclosure=circlify.Circle(x=0, y=0, r=1))
    lingkaran, huruf = [], []
    for circ in sorted(circles, key=lambda c: -c.r):              # besar dulu, kecil di atasnya
        if circ.ex is None:
            continue
        nama = circ.ex["id"]
        lv = LEVEL[nama]
        warna = WARNA_ROOT if lv == 0 else WARNA_LEVEL[lv]
        tip = (f"{nama}&#10;{fmt_id(NILAI[nama], 0)} jiwa&#10;"
               f"{fmt_id(NILAI[nama] / total * 100, 1)}% dari total")
        lingkaran.append(f"<circle cx='{circ.x:.4f}' cy='{-circ.y:.4f}' r='{circ.r:.4f}' fill='{warna}' "
                         f"stroke='#fff' stroke-width='0.012'><title>{tip}</title></circle>")
        if lv == 3:                                                # hanya daun terkecil yang diberi teks
            baris, fs = pecah_label(nama, circ.r)
            tspans = "".join(
                f"<tspan x='{circ.x:.4f}' y='{-circ.y + (i - (len(baris) - 1) / 2) * fs * 1.15:.4f}'>{b}</tspan>"
                for i, b in enumerate(baris))
            huruf.append(f"<text class='svg-teks' font-size='{fs:.4f}' font-weight='700' text-anchor='middle' "
                         f"dominant-baseline='central' fill='{TEKS_LEVEL[lv]}' style='pointer-events:none'>{tspans}</text>")
    svg_cp = (f"<svg class='cp-svg' viewBox='-1.03 -1.03 2.06 2.06' role='img' aria-label='Circle packing penduduk' "
              f"style='display:block;margin:0 auto;width:100%;height:auto;max-height:{TINGGI + 70}px'>"
              + "".join(lingkaran) + "".join(huruf) + "</svg>")
    with kartu("circle"):
        st.markdown("##### Circle Packing")
        st.markdown(svg_cp, unsafe_allow_html=True)


# ===================== KANAN: ICICLE INTERAKTIF (zoom saat klik + breadcrumb + angka di kiri) =====================
def ke_pohon(nama, info):
    return {"name": nama, "value": float(NILAI[nama]), "children": [ke_pohon(a, i) for a, i in info[1].items()]}


with c2:
    with kartu("icicle"):
        st.markdown("##### Icicle")
        components.html(icicle_zoom(ke_pohon("Penduduk", STRUKTUR["Penduduk"]), TINGGI), height=TINGGI + 100,
                        scrolling=False)

sumber_link(*SUMBER["p3"])

nav_bawah("pages/3_Penduduk_Bekerja.py")
