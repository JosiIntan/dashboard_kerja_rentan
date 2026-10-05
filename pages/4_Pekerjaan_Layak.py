"""
HALAMAN 4 - PEKERJAAN LAYAK

CATATAN PERUBAHAN
- [v5] Satu matriks 9 x 9 segitiga bawah; sel Jam<35 x Informal disorot, titik lain dipudarkan; versi diperbesar sel
       itu (dengan garis tren dan r) ditaruh di ruang kosong segitiga atas.
- [v6.1] BUG TUMPUKAN: judul sumbu tiap baris/kolom (diputar) saling menimpa karena terlalu panjang. Sekarang judul
         sumbu dihilangkan dan NAMA VARIABEL ditaruh horizontal di sel DIAGONAL (yang memang kosong).
         Angka sumbu diperkecil dan dijarangkan.
- [v6.1] Keterangan + sumber dipindah ke kartu kiri agar kartu matriks lebih pendek dan halaman muat satu layar.
"""
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from konten import JUDUL, P4_INTRO, SUMBER
from utils import VERMILION, T, fmt_id, gaya_plot, judul_halaman, kartu, muat, nav_bawah, sumber_link, terapkan_gaya

terapkan_gaya()
judul_halaman(JUDUL["p4"])

df = muat("provinsi_indikator.csv")
df["gender_wage_gap"] = (df.upah_l - df.upah_p) / df.upah_l * 100
df["gap_tpak"] = df.tpak_l - df.tpak_p
df["upah_juta"] = df.upah_total / 1e6

VAR = ["tpak", "tpt", "upah_juta", "jam_49plus", "jam_kurang35", "informal", "gender_wage_gap", "gap_tpak", "ipm"]
LABEL = {"tpak": "TPAK", "tpt": "TPT", "upah_juta": "Upah", "jam_49plus": "Jam ≥49",
         "jam_kurang35": "Jam <35", "informal": "Informal", "gender_wage_gap": "Gap Upah",
         "gap_tpak": "Gap TPAK", "ipm": "IPM"}


def nama_sumbu(huruf, i):
    """Variabel ke-i pada Splom memakai sumbu x/y (i=0) atau x2/y2, x3/y3, dst."""
    return huruf if i == 0 else f"{huruf}{i + 1}"


# judul sumbu diganti spasi tak-terputus: nama variabel ditulis di diagonal
fig = px.scatter_matrix(df, dimensions=VAR, hover_name="provinsi", labels={v: "\u00a0" for v in VAR})
fig.update_traces(diagonal_visible=False, showupperhalf=False,
                  marker=dict(size=5, opacity=0.38, color="#9FB1C3"),
                  hovertemplate="<b>%{hovertext}</b><extra></extra>", selector=dict(type="splom"))

for i, v in enumerate(VAR):                       # nama variabel horizontal di sel diagonal
    fig.add_annotation(xref=f"{nama_sumbu('x', i)} domain", yref=f"{nama_sumbu('y', i)} domain", x=0.5, y=0.5,
                       text="<b>" + "<br>".join(LABEL[v].split(" ")) + "</b>", showarrow=False,
                       font=dict(size=11, color="#14213D"))

kol, bar = VAR.index("jam_kurang35"), VAR.index("informal")
xs, ys = nama_sumbu("x", kol), nama_sumbu("y", bar)
r = df["jam_kurang35"].corr(df["informal"])

fig.add_shape(type="rect", xref=f"{xs} domain", yref=f"{ys} domain", x0=0, x1=1, y0=0, y1=1,
              fillcolor="rgba(213,94,0,0.14)", line=dict(color=VERMILION, width=3), layer="below")
fig.add_trace(go.Scatter(x=df.jam_kurang35, y=df.informal, xaxis=xs, yaxis=ys, mode="markers",
                         marker=dict(size=8, color=VERMILION, opacity=1, line=dict(color="white", width=1)),
                         hovertext=df.provinsi, hovertemplate="<b>%{hovertext}</b><extra></extra>",
                         showlegend=False))

gaya_plot(fig, T(470), margin=dict(l=42, r=10, t=34, b=36))
fig.update_xaxes(tickfont=dict(size=8), nticks=3, tickangle=0, showgrid=True, gridcolor="#EDF1F5")
fig.update_yaxes(tickfont=dict(size=8), nticks=3, showgrid=True, gridcolor="#EDF1F5")

# --- Versi diperbesar di ruang kosong kanan-atas (sumbu ke-10, di luar 9 sumbu matriks) ---
koef = np.polyfit(df.jam_kurang35, df.informal, 1)
gx = np.linspace(df.jam_kurang35.min(), df.jam_kurang35.max(), 20)
fig.add_trace(go.Scatter(x=df.jam_kurang35, y=df.informal, xaxis="x10", yaxis="y10", mode="markers",
                         marker=dict(size=10, color=VERMILION, opacity=0.9, line=dict(color="white", width=1.2)),
                         hovertext=df.provinsi, hovertemplate="<b>%{hovertext}</b><extra></extra>",
                         showlegend=False))
fig.add_trace(go.Scatter(x=gx, y=koef[0] * gx + koef[1], xaxis="x10", yaxis="y10", mode="lines",
                         line=dict(color="#7A3300", width=2, dash="dot"), hoverinfo="skip", showlegend=False))
gaya_inset = dict(showline=True, linecolor=VERMILION, linewidth=2, mirror=True, zeroline=False,
                  gridcolor="#F6E4D8", tickfont=dict(size=11))
fig.update_layout(
    xaxis10=dict(domain=[0.52, 1.0], anchor="y10", title=dict(text="Jam <35 (%)", font=dict(size=12)), **gaya_inset),
    yaxis10=dict(domain=[0.60, 0.95], anchor="x10", title=dict(text="Informal (%)", font=dict(size=12)), **gaya_inset),
)
fig.add_annotation(xref="paper", yref="paper", x=0.52, y=0.99, xanchor="left", yanchor="bottom", showarrow=False,
                   text="<b>Diperbesar: Jam &lt;35 × Informal</b>", font=dict(size=13, color=VERMILION))
fig.add_annotation(xref="x10 domain", yref="y10 domain", x=0.04, y=0.96, xanchor="left", yanchor="top",
                   showarrow=False, text=f"<b>r = {fmt_id(r)}</b>", font=dict(size=16, color="#7A3300"),
                   bgcolor="rgba(255,255,255,0.88)", borderpad=3)

kiri, kanan = st.columns([1, 2.15])
with kiri:
    with kartu("teks"):
        st.markdown(f"<div class='teks-rata' style='font-size:0.88rem;line-height:1.5;color:#2D3748;'>{P4_INTRO}</div>",
                    unsafe_allow_html=True)
        st.markdown(
            f"<div class='sorot merah' style='margin-top:0.7rem;font-size:0.88rem;'>"
            f"<b>Sel yang disorot: Jam &lt;35 &times; Informal.</b> Keduanya berkorelasi tinggi "
            f"(r = {fmt_id(r)}): provinsi dengan banyak pekerja informal hampir selalu juga punya banyak "
            f"pekerja dengan jam kerja kurang dari 35 jam seminggu. Hubungan ini dibahas lanjut di halaman "
            f"Profil Provinsi.</div>", unsafe_allow_html=True)
        st.caption("Segitiga atas disembunyikan karena matriks simetris. Tiap titik adalah satu provinsi "
                   "(arahkan kursor untuk melihat namanya). Upah dalam juta rupiah.")
        sumber_link(*SUMBER["p4"])
with kanan:
    with kartu("matriks"):
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

nav_bawah("pages/4_Pekerjaan_Layak.py")
