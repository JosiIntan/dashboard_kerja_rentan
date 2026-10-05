import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

from konten import JUDUL, P5_MENENGAH, P5_PENCILAN, P5_RENTAN, P5_URBAN, SUMBER
from utils import (BIRU, HIJAU, ORANYE, VERMILION, T, gaya_plot, judul_halaman, kartu, muat, nav_bawah,
                   sumber_link, terapkan_gaya)

terapkan_gaya()
judul_halaman(JUDUL["p5"])

VAR_LABEL = {
    "tpak": "TPAK", "tpt": "TPT", "upah_total": "Upah", "jam_49plus": "Jam \u226549",
    "jam_kurang35": "Jam <35", "informal": "Informal", "gender_wage_gap": "Gap Upah",
    "gap_tpak": "Gap TPAK", "ipm": "IPM",
}
VAR = list(VAR_LABEL)

df = muat("provinsi_indikator.csv")
df["gender_wage_gap"] = (df.upah_l - df.upah_p) / df.upah_l * 100
df["gap_tpak"] = df.tpak_l - df.tpak_p

Z = StandardScaler().fit_transform(df[VAR])
pca = PCA().fit(Z)
skor = pca.transform(Z)
km = KMeans(n_clusters=3, n_init=10, random_state=0).fit(skor[:, :2])

rata_informal = df.groupby(km.labels_)["informal"].mean().sort_values()
NAMA_KELOMPOK = {rata_informal.index[0]: "Kelompok Urban-Formal",
                 rata_informal.index[1]: "Kelompok Menengah",
                 rata_informal.index[2]: "Kelompok Rentan Ekstrem"}
df["kelompok"] = [NAMA_KELOMPOK[i] for i in km.labels_]
df["PC1"], df["PC2"] = skor[:, 0], skor[:, 1]
jumlah = df.kelompok.value_counts()

WARNA = {"Kelompok Menengah": BIRU, "Kelompok Urban-Formal": ORANYE, "Kelompok Rentan Ekstrem": HIJAU}
fig = px.scatter(df, x="PC1", y="PC2", color="kelompok", hover_name="provinsi", custom_data=["provinsi"],
                 color_discrete_map=WARNA,
                 category_orders={"kelompok": ["Kelompok Menengah", "Kelompok Urban-Formal", "Kelompok Rentan Ekstrem"]})
fig.update_traces(hovertemplate="<b>%{customdata[0]}</b><extra></extra>",
                  marker=dict(size=10, line=dict(width=0.8, color="white")))

L = pca.components_[:2].T
skala = np.abs(skor[:, :2]).max() / np.abs(L).max() * 0.75
ujung_x, ujung_y = L[:, 0] * skala, L[:, 1] * skala

xmin = min(skor[:, 0].min(), ujung_x.min()) - 0.9
xmax = max(skor[:, 0].max(), ujung_x.max()) + 1.2
ymin = min(skor[:, 1].min(), ujung_y.min()) - 0.9
ymax = max(skor[:, 1].max(), ujung_y.max()) + 0.9

for i in range(len(VAR)):
    fig.add_annotation(x=ujung_x[i], y=ujung_y[i], ax=0, ay=0, xref="x", yref="y", axref="x", ayref="y",
                       showarrow=True, arrowhead=2, arrowsize=1, arrowwidth=1.5, arrowcolor="#555", text="")

TINGGI_FIG = T(440)
px_per_y = (TINGGI_FIG * 0.78) / (ymax - ymin)
JARAK_MIN = 22                                     

def susun_label(indeks):
    """Kembalikan {indeks: offset_y_piksel}. Label satu sisi (kiri/kanan) diurut dari atas lalu didorong
    ke bawah bila terlalu dekat; kelompok digeser balik agar rata-ratanya tetap di dekat posisi aslinya."""
    urut = sorted(indeks, key=lambda i: -ujung_y[i])
    ypx = {i: -ujung_y[i] * px_per_y for i in urut}
    final, atas = {}, None
    for i in urut:
        y = ypx[i]
        if atas is not None and y < atas + JARAK_MIN:
            y = atas + JARAK_MIN
        final[i] = y
        atas = y
    selisih = float(np.mean([final[i] - ypx[i] for i in urut])) if urut else 0.0
    return {i: final[i] - selisih - ypx[i] for i in urut}


kanan_idx = [i for i in range(len(VAR)) if ujung_x[i] >= 0]
kiri_idx = [i for i in range(len(VAR)) if ujung_x[i] < 0]
offset = {**susun_label(kanan_idx), **susun_label(kiri_idx)}

for i, v in enumerate(VAR):
    ke_kanan = ujung_x[i] >= 0
    fig.add_annotation(
        x=ujung_x[i], y=ujung_y[i], xref="x", yref="y",
        ax=18 if ke_kanan else -18, ay=offset[i], axref="pixel", ayref="pixel",
        showarrow=True, arrowhead=0, arrowwidth=0.8, arrowcolor="#B8C2CC",
        text=f"<b>{VAR_LABEL[v]}</b>", font=dict(size=12, color="#2D3748"),
        xanchor="left" if ke_kanan else "right", yanchor="middle",
        bgcolor="rgba(255,255,255,0.88)", bordercolor="#D5DDE5", borderwidth=0.5, borderpad=3)

# ---------- Highlight Papua Pegunungan ----------
pp = df[df.provinsi == "Papua Pegunungan"].iloc[0]
fig.add_trace(go.Scatter(
    x=[pp.PC1], y=[pp.PC2], mode="markers", hoverinfo="skip", showlegend=False,
    marker=dict(symbol="circle-open", size=30, color=VERMILION, line=dict(color=VERMILION, width=3))))  
fig.add_annotation(x=pp.PC1, y=pp.PC2, ax=-70, ay=48, axref="pixel", ayref="pixel", showarrow=True,
                   arrowhead=0, arrowwidth=1.5, arrowcolor=VERMILION, text="<b>Papua Pegunungan</b>",
                   font=dict(size=13, color=VERMILION), xanchor="right", yanchor="top",
                   bgcolor="rgba(255,255,255,0.95)", bordercolor=VERMILION, borderwidth=1, borderpad=6)

fig.add_hline(y=0, line_width=0.5, line_color="#DDD")
fig.add_vline(x=0, line_width=0.5, line_color="#DDD")

gaya_plot(fig, TINGGI_FIG, margin=dict(l=52, r=12, t=44, b=56))   
fig.update_layout(
    dragmode="select",
    legend=dict(orientation="h", y=1.1, x=0, title=None, font=dict(size=12),
                entrywidthmode="pixels", entrywidth=200),
   
    xaxis=dict(title=dict(text="← Mapan & IPM Tinggi    |    Rentan & Informal →", font=dict(size=11), standoff=8),
               showticklabels=False,
               range=[xmin, xmax], showgrid=False, zeroline=False),
    yaxis=dict(title=dict(text="← Upah Tinggi & Setara   |   Upah Rendah & Timpang →", font=dict(size=11), standoff=8),
               showticklabels=False,
               range=[ymin, ymax], showgrid=False, zeroline=False),
)

kiri, kanan = st.columns([1.9, 1])
with kiri:
    with kartu("biplot"):
        event = st.plotly_chart(fig, use_container_width=True, on_select="rerun",
                                selection_mode=("points", "box", "lasso"), key="pca_biplot",
                                config={"displayModeBar": False})
        terpilih = ([p["customdata"][0] for p in event.selection.get("points", []) if "customdata" in p]
                    if event.selection else [])
        if terpilih:
            st.markdown(f"**Provinsi terpilih ({len(terpilih)}):** " + ", ".join(terpilih))
        sumber_link(*SUMBER["p5"])

n_m, n_u, n_r = (int(jumlah.get(k, 0)) for k in ["Kelompok Menengah", "Kelompok Urban-Formal", "Kelompok Rentan Ekstrem"])
with kanan:
    with kartu("teks"):
        st.markdown(
            f"<div class='teks-rata' style='font-size:0.88rem;line-height:1.5;'>"
            f"<p style='margin:0 0 0.55rem'><b style='color:{BIRU}'>Kelompok Menengah</b> {P5_MENENGAH.format(n=n_m)}</p>"
            f"<p style='margin:0 0 0.55rem'><b style='color:#B87900'>Kelompok Urban-Formal</b> {P5_URBAN.format(n=n_u)}</p>"
            f"<p style='margin:0 0 0.7rem'><b style='color:{HIJAU}'>Kelompok Rentan Ekstrem</b> {P5_RENTAN.format(n=n_r)}</p>"
            f"</div>"
            f"<div class='sorot merah teks-rata' style='font-size:0.86rem;'><b>Papua Pegunungan</b> {P5_PENCILAN}</div>",
            unsafe_allow_html=True)

nav_bawah("pages/5_Profil_Provinsi.py")
