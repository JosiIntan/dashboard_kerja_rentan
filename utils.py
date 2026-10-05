"""
utils.py: fungsi bantu yang dipakai di SEMUA halaman.

CATATAN PERUBAHAN (v4 -> v6.1)
- [v6.1] Font Plotly diberi tanda kutip (akar masalah kotak label tidak pas), kartu tidak lagi memotong isi,
        kolom bertumpuk di layar < 900 px, teks SVG, poles UI. Lihat juga komponen.py (icicle interaktif).
- [v5] sumber_link(): judul tautan ditulis lengkap di konten.py (tanpa awalan "Publikasi BPS" otomatis).
- [v5] Ikon tautan yang muncul saat judul di-hover disembunyikan (CSS stHeaderActionElements).
- [v5] legenda_level() dihapus: keterangan akar/level 1/level 2 tidak dipakai lagi.
- [v5] Gaya kartu kabupaten (badge, bar perbandingan) dan ubin angka 3 kolom untuk halaman 6.
- [v6] judul_halaman(): judul + subjudul dengan garis tiga warna (palet data) di sisinya.
- [v6] T(): tinggi grafik mengikuti pilihan "Ukuran grafik" di sidebar (Kompak/Normal/Besar), agar tiap halaman
       bisa dimuat dalam satu layar. Ubah angka dasarnya di tiap halaman bila perlu.
- [v6] CSS_BARU (aktif bila UI_BARU=True di konten.py): latar berlapis, kartu dengan garis atas tiga warna dan
       bayangan berlapis, dock navigasi melayang, tombol utama bergradasi, animasi masuk SATU kali.
- [v6] Responsif: kolom bertumpuk di layar kecil, navigasi bawah tidak pernah turun baris.
"""
from pathlib import Path

import pandas as pd
import streamlit as st

from konten import UI_BARU

DATA = Path(__file__).parent / "data" / "processed"

# --- Palet Okabe-Ito (aman untuk 3 jenis buta warna) ---
BIRU, ORANYE, HIJAU, VERMILION, ABU = "#0072B2", "#E69F00", "#009E73", "#D55E00", "#9AA5B1"
NAVY = "#14213D"
KATEGORI = [BIRU, ORANYE, HIJAU]

# Warna per level hierarki (halaman 2 dan 3 memakai warna yang sama)
WARNA_ROOT = "#D9D9D9"
WARNA_LEVEL = {1: BIRU, 2: HIJAU, 3: ORANYE}
TEKS_LEVEL = {0: "#1A1A1A", 1: "#FFFFFF", 2: "#FFFFFF", 3: "#1A1A1A"}

URUTAN_HALAMAN = [
    ("pages/1_Pendahuluan.py", "Pendahuluan"),
    ("pages/2_Definisi_Bekerja.py", "Definisi Bekerja"),
    ("pages/3_Penduduk_Bekerja.py", "Penduduk Bekerja"),
    ("pages/4_Pekerjaan_Layak.py", "Pekerjaan Layak"),
    ("pages/5_Profil_Provinsi.py", "Profil Provinsi"),
    ("pages/6_Papua_Pegunungan.py", "Papua Pegunungan"),
    ("pages/7_Kesimpulan.py", "Kesimpulan"),
]

# Pilihan ukuran grafik (sidebar, dibuat di app.py). 1.0 dirancang untuk layar laptop ~ 720 px tinggi.
UKURAN = {"Kompak": 0.85, "Normal": 1.0, "Besar": 1.2}


def T(px: int) -> int:
    """Tinggi grafik (piksel) setelah dikalikan skala ukuran yang dipilih pengguna."""
    pilihan = st.session_state.get("ukuran_tampilan", "Normal")
    return int(px * UKURAN.get(pilihan, 1.0))


@st.cache_data
def muat(nama: str) -> pd.DataFrame:
    p = DATA / nama
    if not p.exists():
        st.error(f"Berkas `data/processed/{nama}` tidak ditemukan.")
        st.stop()
    return pd.read_csv(p)


def fmt_id(v: float, desimal: int = 2) -> str:
    """Format angka gaya Indonesia: 1234.5 -> '1.234,50'."""
    s = f"{v:,.{desimal}f}"
    return s.replace(",", "§").replace(".", ",").replace("§", ".")


def gaya_plot(fig, tinggi: int, margin=None):
    """Gaya Plotly seragam: latar putih, pemisah angka Indonesia, font sama dengan halaman."""
    fig.update_layout(
        template="plotly_white", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        height=tinggi, separators=",.",
        margin=margin or dict(l=10, r=10, t=10, b=10),
        font=dict(family='"Source Sans 3", "Segoe UI", sans-serif', color="#1A1A1A"),   # [v6.1] tanda kutip wajib
    )
    return fig


# =====================================================================================
# CSS DASAR (selalu aktif)
# =====================================================================================
CSS_DASAR = """
@import url('https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,500;12..96,700&family=Source+Sans+3:wght@400;600;700&display=swap');

html, body, .stApp, .stMarkdown, button, input, select, textarea {
    font-family: 'Source Sans 3', 'Segoe UI', system-ui, sans-serif;
}
h1, h2, h3, h4, h5 {
    font-family: 'Bricolage Grotesque', 'Source Sans 3', system-ui, sans-serif !important;
    color: #14213D; letter-spacing: -0.015em;
}
h5 { font-weight: 600 !important; margin: 0 0 0.3rem !important; padding: 0 !important; }

.stApp { background: linear-gradient(180deg, #E4EFF7 0, #F4F7FA 340px) no-repeat, #F4F7FA; }
header[data-testid="stHeader"] { background: transparent; }
[data-testid="stToolbar"], footer, #MainMenu { display: none !important; }

.block-container { max-width: 1100px; margin: 0 auto; padding: 1.4rem 1rem 6rem; }
div[data-testid="stVerticalBlock"] > div { gap: 0.5rem; }

/* Ikon tautan yang muncul saat judul di-hover: disembunyikan */
[data-testid="stHeaderActionElements"], .stMarkdown h1 a, .stMarkdown h2 a, .stMarkdown h3 a,
.stMarkdown h4 a, .stMarkdown h5 a { display: none !important; }

.teks-rata { text-align: justify; }
.block-container a { color: inherit !important; text-decoration: underline !important; }

/* ---------- Judul halaman + subjudul ---------- */
.jh { display: flex; gap: 0.85rem; align-items: stretch; margin: 0 0 0.6rem; }
.jh-bar { flex: 0 0 5px; border-radius: 4px;
          background: linear-gradient(180deg, #0072B2 0 34%, #009E73 34% 67%, #E69F00 67%); }
.jh-judul { margin: 0 !important; padding: 0 !important; line-height: 1.12 !important;
            font-size: clamp(1.3rem, 2.8vw, 1.8rem) !important; font-weight: 700 !important; }
.jh-sub { margin: 0.28rem 0 0; color: #566377; font-size: 0.98rem; line-height: 1.45; max-width: 95ch; }

/* ---------- Kartu ---------- */
[class*="st-key-kartu"] {
    background: #FFFFFF; border: 1px solid #E3E9F0; border-radius: 16px; padding: 0.9rem 1.1rem 1.4rem;
    box-shadow: 0 1px 2px rgba(20,33,61,0.05), 0 10px 28px -14px rgba(20,33,61,0.18);
}

/* ---------- Kotak sorotan ---------- */
.sorot { border-left: 4px solid #0072B2; background: #EAF3FA; border-radius: 4px 12px 12px 4px;
         padding: 0.7rem 1rem; font-size: 0.97rem; line-height: 1.5; color: #14213D; }
.sorot.merah { border-left-color: #D55E00; background: #FCEFE6; }

/* ---------- Alur halaman pertama ---------- */
.alur { display: flex; justify-content: center; align-items: center; flex-wrap: wrap; gap: 0.45rem; margin: 0.3rem 0 0.6rem; }
.alur .langkah { background: #FFFFFF; border: 1px solid #D5E2EE; color: #14213D; border-radius: 999px;
                 padding: 0.28rem 0.95rem; font-weight: 600; font-size: 0.93rem; }
.alur .panah { color: #9AA5B1; font-size: 1.05rem; }

/* ---------- Ubin angka ---------- */
.metrik-grid { display: grid; grid-template-columns: repeat(var(--kol, 3), 1fr); gap: 0.45rem; }
.metrik { background: #F4F8FB; border: 1px solid #E3E9F0; border-radius: 12px; padding: 0.45rem 0.65rem; min-width: 0; }
.metrik span { display: block; font-size: 0.72rem; color: #5A6778; line-height: 1.2; }
.metrik b { display: block; font-family: 'Bricolage Grotesque', sans-serif; font-size: clamp(0.9rem, 1.5vw, 1.08rem);
            line-height: 1.2; color: #14213D; overflow-wrap: anywhere; }
.metrik.utama { background: #EAF3FA; border-color: #BFD9EC; }
.metrik.besar b { font-size: 1.5rem; }
.metrik.besar { padding: 0.7rem 0.9rem; }

/* ---------- Kartu detail kabupaten ---------- */
.kab-judul { display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; gap: 0.3rem 0.6rem; margin-bottom: 0.5rem; }
.kab-judul b { min-width: 0; overflow-wrap: anywhere; font-family: 'Bricolage Grotesque', sans-serif; font-size: 1.15rem; color: #14213D; line-height: 1.2; }
.badge { display: inline-block; border-radius: 999px; padding: 0.12rem 0.65rem; font-size: 0.72rem; font-weight: 600; text-align: center; }
.badge.hijau { background: #DDF3EA; color: #00694B; }
.badge.kuning { background: #FCF0D2; color: #7A5200; }
.badge.merah { background: #FBE3D4; color: #8F3C00; }
.bar { position: relative; height: 9px; border-radius: 999px; background: #E6EDF4; margin: 0.55rem 0 0.2rem; }
.bar .isi { height: 100%; border-radius: 999px; background: #0072B2; }
.bar .tanda { position: absolute; top: -4px; width: 3px; height: 17px; border-radius: 2px; background: #D55E00; }
.bar-ket { font-size: 0.74rem; color: #5A6778; display: flex; justify-content: space-between; gap: 0.5rem; }

/* ---------- Legenda ukuran gelembung peta ---------- */
.gel-legenda { display: flex; align-items: center; flex-wrap: wrap; gap: 0.35rem 1rem; font-size: 0.8rem; color: #2D3748; margin-top: 0.3rem; }
.gel-legenda .item { display: inline-flex; align-items: center; gap: 0.35rem; }
.gel { display: inline-block; border-radius: 50%; background: rgba(230,159,0,0.62); border: 1.5px solid #fff; box-shadow: 0 0 0 1px rgba(0,0,0,0.18); }

.stButton button { border-radius: 999px; font-weight: 600; }

/* ---------- Navigasi bawah ---------- */
.st-key-nav_bawah { position: fixed; bottom: 0; left: 0; right: 0; background: rgba(255,255,255,0.94);
                    backdrop-filter: blur(6px); border-top: 1px solid #E2E8F0; padding: 0.5rem 2rem; z-index: 999; }
.st-key-nav_bawah [data-testid="stHorizontalBlock"] { flex-wrap: nowrap !important; gap: 0.5rem; align-items: center; }
.st-key-nav_bawah [data-testid="stColumn"], .st-key-nav_bawah [data-testid="column"] { min-width: 0 !important; }
.st-key-nav_bawah .stButton button { max-width: 100%; }
.st-key-nav_bawah .stButton button p { white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.titik { text-align: center; margin: 0 !important; line-height: 1; }
.st-key-nav_bawah [data-testid="stMarkdownContainer"] { margin: 0 !important; }
.titik i { display: inline-block; width: 8px; height: 8px; border-radius: 50%; background: #CBD5E0; margin: 0 4px; }
.titik i.aktif { width: 22px; border-radius: 6px; background: #0072B2; }

/* ---------- [v6.1] Layar menengah/kecil: kolom bertumpuk lebih awal agar grafik tidak sempit ---------- */
@media (max-width: 900px) {
    .teks-rata { text-align: left; }
    [data-testid="stHorizontalBlock"] { flex-wrap: wrap !important; }
    [data-testid="stColumn"], [data-testid="column"] { min-width: 100% !important; flex: 1 1 100% !important; }
    .st-key-nav_bawah [data-testid="stHorizontalBlock"] { flex-wrap: nowrap !important; }
    .st-key-nav_bawah [data-testid="stColumn"], .st-key-nav_bawah [data-testid="column"] { min-width: 0 !important; flex: 1 1 0 !important; }
}
[class*="st-key-kartu"] [data-testid="stMarkdownContainer"] p:last-child { margin-bottom: 0; }

/* [v6.1] Teks pada SVG (diagram halaman 2, circle packing halaman 3) dan hover lingkaran */
.svg-teks { font-family: 'Source Sans 3', 'Segoe UI', system-ui, sans-serif; }
.cp-svg circle:hover { stroke: #14213D !important; stroke-width: 0.014 !important; cursor: pointer; }

/* ---------- Layar kecil ---------- */
@media (max-width: 700px) {
    .block-container { padding: 0.9rem 0.75rem 6rem; }
    .st-key-nav_bawah { padding: 0.4rem 0.6rem; }
    .st-key-nav_bawah .stButton button p { font-size: 0.8rem; }
    .titik { display: none; }
    .metrik-grid { grid-template-columns: repeat(2, 1fr); }
    .alur .langkah { font-size: 0.8rem; padding: 0.2rem 0.65rem; }
    [class*="st-key-kartu"] { padding: 0.7rem 0.75rem; }
}
"""

# =====================================================================================
# CSS BARU (aktif bila UI_BARU = True): tidak flat, berlapis, ada kedalaman
# =====================================================================================
CSS_BARU = """
/* Latar: tiga cahaya lembut dengan warna palet data (biru, oranye, hijau) */
.stApp {
    background:
        radial-gradient(900px 420px at 6% -6%, rgba(0,114,178,0.17), transparent 62%),
        radial-gradient(720px 400px at 100% 2%, rgba(230,159,0,0.15), transparent 62%),
        radial-gradient(900px 520px at 50% 112%, rgba(0,158,115,0.11), transparent 62%),
        #F2F6FA !important;
}

/* Satu-satunya animasi otomatis: halaman masuk perlahan, sekali saat dibuka */
@keyframes masuk { from { opacity: 0; } to { opacity: 1; } }   /* hanya opacity: transform akan menggeser navigasi fixed */
.block-container { animation: masuk 0.5s ease-out both; }
@media (prefers-reduced-motion: reduce) { .block-container { animation: none; } }

/* Kartu: garis atas tiga warna, tepi tipis, bayangan berlapis berwarna biru */
[class*="st-key-kartu"] {
    position: relative; overflow: visible;   /* [v6.1] visible: isi yang menjorok tidak lagi terpotong */
    background: linear-gradient(180deg, #FFFFFF 0%, #FBFDFF 100%);
    border: 1px solid rgba(20,33,61,0.07); border-radius: 18px; padding: 1.1rem 1.25rem 1.6rem;
    box-shadow: 0 1px 2px rgba(20,33,61,0.06),
                0 12px 24px -12px rgba(20,33,61,0.18),
                0 30px 60px -30px rgba(0,114,178,0.30);
}
[class*="st-key-kartu"]::before {
    content: ""; position: absolute; left: 0; right: 0; top: 0; height: 4px; border-radius: 18px 18px 0 0;
    background: linear-gradient(90deg, #0072B2 0 34%, #009E73 34% 67%, #E69F00 67%);
}

/* Kotak sorotan dengan gradasi halus */
.sorot { background: linear-gradient(90deg, #E3F0FA, #F1F7FC); box-shadow: 0 6px 14px -10px rgba(0,114,178,0.5); }
.sorot.merah { background: linear-gradient(90deg, #FCE6D6, #FDF3EB); box-shadow: 0 6px 14px -10px rgba(213,94,0,0.5); }

/* Ubin angka: gradasi tipis, ubin utama bergaris biru di kiri */
.metrik { background: linear-gradient(180deg, #FFFFFF, #F1F6FB); box-shadow: 0 1px 2px rgba(20,33,61,0.05); }
.metrik.utama { background: linear-gradient(180deg, #F2F9FF, #E1EFFA); border-left: 3px solid #0072B2; }

/* Hero halaman pertama: lingkaran-lingkaran lembut (mengulang motif circle packing di halaman 3) */
.st-key-hero {
    position: relative; overflow: hidden; border-radius: 26px; padding: 1.5rem 1.2rem 0.7rem;
    background: linear-gradient(135deg, #FFFFFF 0%, #EBF4FB 100%);
    border: 1px solid rgba(20,33,61,0.07);
    box-shadow: 0 14px 30px -18px rgba(20,33,61,0.28);
}
.st-key-hero::before {
    content: ""; position: absolute; inset: 0; pointer-events: none;
    background:
        radial-gradient(circle at 95% 16%, rgba(0,114,178,0.18) 0 64px, transparent 65px),
        radial-gradient(circle at 88% 74%, rgba(230,159,0,0.24) 0 34px, transparent 35px),
        radial-gradient(circle at 4% 80%, rgba(0,158,115,0.19) 0 54px, transparent 55px),
        radial-gradient(circle at 11% 15%, rgba(230,159,0,0.17) 0 24px, transparent 25px),
        radial-gradient(circle at 80% 12%, rgba(0,158,115,0.15) 0 16px, transparent 17px);
}
.st-key-hero > * { position: relative; }

/* Tombol: utama bergradasi biru, sekunder putih bergaris */
.stButton button[kind="primary"] {
    background: linear-gradient(135deg, #0A84C8, #005B8F); border: none; color: #fff;
    box-shadow: 0 8px 18px -8px rgba(0,91,143,0.7); transition: transform 0.15s ease, box-shadow 0.15s ease;
}
.stButton button[kind="primary"]:hover { transform: translateY(-1px); box-shadow: 0 12px 22px -8px rgba(0,91,143,0.8); }
.stButton button[kind="secondary"] { background: rgba(255,255,255,0.9); border: 1px solid #CBD9E6; }

/* Pilihan (selectbox): putih bersudut bulat */
div[data-baseweb="select"] > div { border-radius: 12px; background: #FFFFFF; border-color: #D5E2EE;
                                   box-shadow: 0 4px 10px -6px rgba(20,33,61,0.25); }

/* Navigasi bawah menjadi dock melayang */
.st-key-nav_bawah {
    left: 50%; right: auto; bottom: 12px; transform: translateX(-50%);
    width: min(1100px, calc(100vw - 24px)); border: 1px solid rgba(20,33,61,0.08); border-radius: 22px;
    background: rgba(255,255,255,0.82); backdrop-filter: blur(14px) saturate(1.4);
    box-shadow: 0 14px 34px -12px rgba(20,33,61,0.38); padding: 0.4rem 0.9rem;
}

/* ---------- [v6.1] Poles tambahan ---------- */
::selection { background: rgba(0,114,178,0.22); }
::-webkit-scrollbar { width: 10px; height: 10px; }
::-webkit-scrollbar-thumb { background: #C5D3E0; border-radius: 8px; border: 2px solid #F2F6FA; }
section[data-testid="stSidebar"] { background: linear-gradient(180deg, #F8FBFE, #E8F1F8); }
[data-testid="stCaptionContainer"] { color: #64748B; }
.jh-bar { box-shadow: 0 0 16px rgba(0,114,178,0.35); }
.titik i.aktif { background: linear-gradient(90deg, #0072B2, #009E73); }
.metrik { transition: transform 0.15s ease, box-shadow 0.15s ease; }
.metrik:hover { transform: translateY(-2px); box-shadow: 0 10px 18px -10px rgba(20,33,61,0.35); }
.mark { background: linear-gradient(transparent 62%, rgba(230,159,0,0.38) 62%); padding: 0 0.12em; }
"""


def terapkan_gaya():
    """WAJIB dipanggil di baris pertama tiap halaman."""
    css = CSS_DASAR + (CSS_BARU if UI_BARU else "")
    st.markdown("<style>" + css + "</style>", unsafe_allow_html=True)


def tengah_vertikal():
    """Untuk halaman pendek: pusatkan isi secara vertikal supaya tidak menggantung di atas."""
    st.markdown("""
        <style>
        .block-container { min-height: calc(100vh - 90px); display: flex; flex-direction: column; justify-content: center; }
        </style>
    """, unsafe_allow_html=True)


def judul_halaman(judul: str, sub: str = ""):
    """Judul + subjudul dengan garis tiga warna di sisi kiri. Teks diisi dari konten.py."""
    sub_html = f"<p class='jh-sub'>{sub}</p>" if sub else ""
    st.markdown(
        f"<div class='jh'><div class='jh-bar'></div>"
        f"<div><h2 class='jh-judul'>{judul}</h2>{sub_html}</div></div>",
        unsafe_allow_html=True)


def kartu(nama: str):
    """Kartu putih. Pemakaian: `with kartu('grafik'): ...` (nama harus unik per halaman)."""
    return st.container(key=f"kartu_{nama}")


def ubin(item, kolom: int = 3, kelas_umum: str = ""):
    """HTML ubin angka. item = [(label, nilai_teks, kelas_tambahan), ...]."""
    isi = "".join(f"<div class='metrik {kelas_umum} {k}'><span>{lab}</span><b>{val}</b></div>"
                  for lab, val, k in item)
    return f"<div class='metrik-grid' style='--kol:{kolom}'>{isi}</div>"


def sumber_link(judul: str, url: str, tanggal: str):
    st.caption(f"Sumber: [{judul}]({url}) (Diakses tanggal {tanggal}).")


def nav_bawah(halaman_ini: str):
    """Tombol Kembali / Lanjut + indikator titik, menempel di dasar layar."""
    idx = [h[0] for h in URUTAN_HALAMAN].index(halaman_ini)
    with st.container(key="nav_bawah"):
        kiri, tengah, kanan = st.columns([1.3, 2, 1.3])
        with kiri:
            if idx > 0:
                if st.button(f"← {URUTAN_HALAMAN[idx - 1][1]}"):
                    st.switch_page(URUTAN_HALAMAN[idx - 1][0])
        with tengah:
            titik = "".join(f"<i class='{'aktif' if i == idx else ''}'></i>" for i in range(len(URUTAN_HALAMAN)))
            st.markdown(f"<p class='titik'>{titik}</p>", unsafe_allow_html=True)
        with kanan:
            if idx < len(URUTAN_HALAMAN) - 1:
                if st.button(f"{URUTAN_HALAMAN[idx + 1][1]} →", type="primary", use_container_width=True):
                    st.switch_page(URUTAN_HALAMAN[idx + 1][0])
