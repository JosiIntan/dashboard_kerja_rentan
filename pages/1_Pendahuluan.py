import plotly.graph_objects as go
import streamlit as st

from konten import P1_PENUTUP, SUMBER
from utils import BIRU, NAVY, T, fmt_id, gaya_plot, kartu, muat, nav_bawah, sumber_link, tengah_vertikal, terapkan_gaya

terapkan_gaya()
tengah_vertikal()

with st.container(key="hero"):
    st.markdown(
        "<h1 style='text-align:center;font-size:clamp(1.5rem,4.2vw,2.3rem);line-height:1.15;margin:0 0 0.4rem;'>"
        "<span class='mark'>284,4 Juta Penduduk</span> di Indonesia Tahun 2025,<br>Berapa Orang yang Bekerja?</h1>",
        unsafe_allow_html=True)
    st.markdown(
        "<div class='alur'><span class='langkah'>Penduduk</span><span class='panah'>→</span>"
        "<span class='langkah'>Usia Kerja</span><span class='panah'>→</span>"
        "<span class='langkah'>Angkatan Kerja</span><span class='panah'>→</span>"
        "<span class='langkah'>Bekerja</span></div>",
        unsafe_allow_html=True)

tpt = muat("tpt_indonesia.csv")
tpt["angka_tahun"] = tpt.tahun.str.split(" ").str[1].astype(int)
tpt["urutan_bulan"] = tpt.tahun.str.split(" ").str[0].map({"Feb": 0, "Agus": 1})
tpt = tpt.sort_values(["angka_tahun", "urutan_bulan"]).reset_index(drop=True)

fig = go.Figure(go.Scatter(
    x=tpt.tahun, y=tpt.tpt_indonesia, mode="lines+markers",
    line=dict(color=BIRU, width=3.5), marker=dict(size=9, color=BIRU, line=dict(color="white", width=1.5)),
    fill="tozeroy", fillcolor="rgba(0,114,178,0.09)",
    hovertemplate="TPT %{x}: <b>%{y:.2f}%</b><extra></extra>",
))
for i, geser in [(0, 20), (len(tpt) - 1, -20)]:        # angka hanya di titik awal dan akhir
    fig.add_annotation(x=tpt.tahun[i], y=tpt.tpt_indonesia[i], text=f"<b>{fmt_id(tpt.tpt_indonesia[i])}%</b>",
                       showarrow=False, yshift=geser, font=dict(size=14, color=NAVY))
gaya_plot(fig, T(290))
fig.update_xaxes(title=None, tickangle=-45, tickfont=dict(size=11), showgrid=False)
fig.update_yaxes(title="TPT (%)", range=[0, max(tpt.tpt_indonesia) * 1.2], gridcolor="#EDF1F5")

with kartu("tpt"):
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    sumber_link(*SUMBER["p1"])

st.markdown(f"<div class='sorot' style='text-align:center;font-weight:600;font-size:1.08rem;'>{P1_PENUTUP}</div>",
            unsafe_allow_html=True)

nav_bawah("pages/1_Pendahuluan.py")
