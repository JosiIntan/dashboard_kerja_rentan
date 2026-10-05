import numpy as np
from plotly.subplots import make_subplots
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
LABEL = {"tpak": "TPAK", "tpt": "TPT", "upah_juta": "Upah (juta)", "jam_49plus": "Jam ≥49",
         "jam_kurang35": "Jam <35", "informal": "Informal", "gender_wage_gap": "Gap Upah",
         "gap_tpak": "Gap TPAK", "ipm": "IPM"}


N = len(VAR)


def sumbu(huruf, n):
    """Nama sumbu subplot ke-n pada make_subplots (dihitung dari 1, baris demi baris): x, x2, x3, ..."""
    return huruf if n == 1 else f"{huruf}{n}"


def no(r, c):
    """Nomor subplot untuk baris r, kolom c (keduanya 1..N)."""
    return (r - 1) * N + c


fig = make_subplots(rows=N, cols=N, horizontal_spacing=0.012, vertical_spacing=0.012)
fig.update_xaxes(showgrid=False, showticklabels=False, showline=False, zeroline=False)
fig.update_yaxes(showgrid=False, showticklabels=False, showline=False, zeroline=False)

for r_ in range(2, N + 1):
    for c_ in range(1, r_):
        vx, vy = VAR[c_ - 1], VAR[r_ - 1]
        fig.add_trace(go.Scatter(
            x=df[vx], y=df[vy], mode="markers", showlegend=False,
            marker=dict(size=5, color="#9FB1C3", opacity=0.45),          
            hovertext=df.provinsi,
            hovertemplate="<b>%{hovertext}</b><br>" + LABEL[vx] + ": %{x:,.2f}<br>" + LABEL[vy] + ": %{y:,.2f}<extra></extra>"),
            row=r_, col=c_)
        fig.update_xaxes(showgrid=True, gridcolor="#EDF1F5", nticks=3, tickfont=dict(size=8), tickangle=0,
                         showticklabels=(r_ == N), row=r_, col=c_)
        fig.update_yaxes(showgrid=True, gridcolor="#EDF1F5", nticks=3, tickfont=dict(size=8),
                         showticklabels=(c_ == 1), row=r_, col=c_)


def pusat_sel(n):
    """Titik tengah sel subplot ke-n dalam koordinat paper, dibaca dari domain yang sudah dihitung make_subplots.
    (Tidak memakai 'xN domain' karena sumbu sel kosong tidak selalu dikenali Plotly -> label menumpuk.)"""
    xa = fig.layout["xaxis" if n == 1 else f"xaxis{n}"].domain
    ya = fig.layout["yaxis" if n == 1 else f"yaxis{n}"].domain
    return (xa[0] + xa[1]) / 2, (ya[0] + ya[1]) / 2


for i, v in enumerate(VAR, start=1):                 # nama variabel horizontal di sel diagonal (i,i)
    cx, cy = pusat_sel(no(i, i))
    fig.add_annotation(xref="paper", yref="paper", x=cx, y=cy, showarrow=False,
                       text="<b>" + "<br>".join(LABEL[v].split(" ")) + "</b>",
                       font=dict(size=11, color="#14213D"))

# --- Sel yang disorot: Jam<35 (kolom) x Informal (baris) ---
c_h, r_h = VAR.index("jam_kurang35") + 1, VAR.index("informal") + 1
xs, ys = sumbu("x", no(r_h, c_h)), sumbu("y", no(r_h, c_h))
r = df["jam_kurang35"].corr(df["informal"])

fig.add_shape(type="rect", xref=f"{xs} domain", yref=f"{ys} domain", x0=0, x1=1, y0=0, y1=1,
              fillcolor="rgba(213,94,0,0.14)", line=dict(color=VERMILION, width=3), layer="below")
fig.add_trace(go.Scatter(x=df.jam_kurang35, y=df.informal, xaxis=xs, yaxis=ys, mode="markers",
                         marker=dict(size=8, color=VERMILION, opacity=1, line=dict(color="white", width=1)),
                         hovertext=df.provinsi, hovertemplate="<b>%{hovertext}</b><extra></extra>",
                         showlegend=False))

gaya_plot(fig, T(470), margin=dict(l=44, r=10, t=34, b=40))

K = N * N + 1
xi, yi = sumbu("x", K), sumbu("y", K)
koef = np.polyfit(df.jam_kurang35, df.informal, 1)
gx = np.linspace(df.jam_kurang35.min(), df.jam_kurang35.max(), 20)
fig.add_trace(go.Scatter(x=df.jam_kurang35, y=df.informal, xaxis=xi, yaxis=yi, mode="markers",
                         marker=dict(size=10, color=VERMILION, opacity=0.9, line=dict(color="white", width=1.2)),
                         hovertext=df.provinsi, hovertemplate="<b>%{hovertext}</b><extra></extra>",
                         showlegend=False))
fig.add_trace(go.Scatter(x=gx, y=koef[0] * gx + koef[1], xaxis=xi, yaxis=yi, mode="lines",
                         line=dict(color="#7A3300", width=2, dash="dot"), hoverinfo="skip", showlegend=False))
gaya_inset = dict(showline=True, linecolor=VERMILION, linewidth=2, mirror=True, zeroline=False,
                  gridcolor="#F6E4D8", tickfont=dict(size=11), showticklabels=True)
fig.update_layout(**{
    f"xaxis{K}": dict(domain=[0.52, 1.0], anchor=yi, title=dict(text="Jam <35 (%)", font=dict(size=12)), **gaya_inset),
    f"yaxis{K}": dict(domain=[0.64, 0.97], anchor=xi, title=dict(text="Informal (%)", font=dict(size=12)), **gaya_inset),
})
fig.add_annotation(xref="paper", yref="paper", x=0.52, y=0.985, xanchor="left", yanchor="bottom", showarrow=False,
                   text="<b>Diperbesar: Jam &lt;35 × Informal</b>", font=dict(size=13, color=VERMILION))
fig.add_annotation(xref=f"{xi} domain", yref=f"{yi} domain", x=0.04, y=0.96, xanchor="left", yanchor="top",
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
        sumber_link(*SUMBER["p4"])
with kanan:
    with kartu("matriks"):
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

nav_bawah("pages/4_Pekerjaan_Layak.py")
