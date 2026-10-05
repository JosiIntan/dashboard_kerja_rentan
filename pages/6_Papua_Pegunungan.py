"""
HALAMAN 6 - PAPUA PEGUNUNGAN

CATATAN PERUBAHAN
- [v5] Kartu detail kabupaten/kota muncul DI BAWAH kartu Profil Provinsi saat sebuah wilayah dipilih
       (nilai pilihan dibaca dari st.session_state["fokus_wilayah"] sebelum kolom kiri digambar).
- [v5] Peta: gelembung proporsional = jumlah absolut penduduk bekerja (semakin besar, semakin banyak),
       lengkap dengan legenda ukuran. Luas gelembung sebanding dengan jumlah (ukuran = akar kuadrat).
- [v5] Peta "Semua kabupaten/kota": zoom dihitung dari batas wilayah dengan margin aman supaya 8 kabupaten
       masuk semua, dan nama seluruh kabupaten ditampilkan (titik label = centroid poligon terbesar).
- [v5] Wilayah yang dipilih diberi garis tepi tebal merah-oranye. Colorbar dipindah ke dalam peta (horizontal)
       supaya lebar peta tidak terpotong lagi.
- [v5] Tooltip: angka TPT memakai koma (sebelumnya "2.92%", kini "2,92%").
- [v5] Rata-rata upah tampil "Rp 3,9 juta".
- [v6.1] Peta diperpendek, colorbar diringkas, nama kabupaten 2 baris; kartu tidak lagi memotong isi (utils).
- [v6] Profil provinsi memakai ubin 3 kolom yang ringkas agar halaman muat satu layar.
"""
import json
import math
from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from konten import JUDUL, P6_INTRO, SUMBER
from utils import (NAVY, ORANYE, VERMILION, T, fmt_id, gaya_plot, judul_halaman, kartu, muat, nav_bawah,
                   sumber_link, terapkan_gaya, ubin)

terapkan_gaya()
judul_halaman(JUDUL["p6"], P6_INTRO)

SEMUA = "Semua kabupaten/kota"
fokus = st.session_state.get("fokus_wilayah", SEMUA)     # dibaca dulu, widget-nya ada di kolom kanan

# ------------------------------------------------------------------ data
prov = muat("provinsi_indikator.csv")
row = prov[prov.provinsi == "Papua Pegunungan"].iloc[0].copy()
row["gender_wage_gap"] = (row.upah_l - row.upah_p) / row.upah_l * 100
row["gap_tpak"] = row.tpak_l - row.tpak_p

pp = muat("papua_pegunungan.csv").copy()
# 'N.A.' pada data BPS = tidak tersedia (RSE > 50%)
pp["tpt_num"] = [None if str(v).strip() == "N.A." else float(v) for v in pp["tpt"]]
pp["penganggur_num"] = [None if str(v).strip() == "N.A." else float(v) for v in pp["penganggur_terbuka"]]
pp["tpt_tampil"] = [("Tidak tersedia (RSE>50%)" if pd.isna(v) else f"{fmt_id(v)}%") for v in pp["tpt_num"]]

geo_path = Path(__file__).parent.parent / "data" / "processed" / "papua_pegunungan.geojson"
with open(geo_path, encoding="utf-8") as f:
    gj = json.load(f)


# ------------------------------------------------------------------ geometri
def semua_titik(koordinat, hasil):
    if isinstance(koordinat[0], (int, float)):
        hasil.append(koordinat)
    else:
        for sub in koordinat:
            semua_titik(sub, hasil)


def luas_centroid(cincin):
    """Rumus shoelace: kembalikan (luas, cx, cy) untuk satu cincin poligon."""
    a = cx = cy = 0.0
    n = len(cincin)
    for k in range(n):
        x0, y0 = cincin[k][0], cincin[k][1]
        x1, y1 = cincin[(k + 1) % n][0], cincin[(k + 1) % n][1]
        c = x0 * y1 - x1 * y0
        a += c
        cx += (x0 + x1) * c
        cy += (y0 + y1) * c
    a /= 2
    if abs(a) < 1e-12:
        return 0.0, cincin[0][0], cincin[0][1]
    return a, cx / (6 * a), cy / (6 * a)


def centroid_terbesar(geom):
    """Titik label: centroid poligon terbesar (lebih tepat dibanding rata-rata semua titik)."""
    polys = [geom["coordinates"]] if geom["type"] == "Polygon" else geom["coordinates"]
    terbaik = max((luas_centroid(p[0]) for p in polys), key=lambda t: abs(t[0]))
    return terbaik[2], terbaik[1]          # (lat, lon)


pusat, titik_all = {}, []
for ft in gj["features"]:
    pusat[ft["properties"]["kabkota"]] = centroid_terbesar(ft["geometry"])
    semua_titik(ft["geometry"]["coordinates"], titik_all)
lon_min, lon_max = min(p[0] for p in titik_all), max(p[0] for p in titik_all)
lat_min, lat_max = min(p[1] for p in titik_all), max(p[1] for p in titik_all)

TINGGI_PETA = T(310)      # [v6.1] diperpendek supaya halaman muat satu layar
# Zoom yang pas agar SEMUA kabupaten tampak: perkiraan kanvas 520 px lebar, margin aman 0,35 tingkat zoom
zoom_semua = min(math.log2(520 * 360 / (512 * (lon_max - lon_min))),
                 math.log2(TINGGI_PETA * 360 / (512 * (lat_max - lat_min)))) - 0.35
pusat_semua = ((lat_min + lat_max) / 2, (lon_min + lon_max) / 2)

# ------------------------------------------------------------------ KIRI
kiri, kanan = st.columns([1.05, 1.6])

with kiri:
    with kartu("profil"):
        st.markdown("##### Profil Provinsi")
        st.markdown(ubin([
            ("TPAK", f"{fmt_id(row.tpak)} %", ""),
            ("TPT", f"{fmt_id(row.tpt)} %", ""),
            ("Rata-rata upah", f"Rp {fmt_id(row.upah_total / 1e6, 1)} juta", "utama"),   # 3.941.546 -> Rp 3,9 juta
            ("Bekerja ≥49 jam", f"{fmt_id(row.jam_49plus)} %", ""),
            ("Bekerja <35 jam", f"{fmt_id(row.jam_kurang35)} %", ""),
            ("Pekerja informal", f"{fmt_id(row.informal)} %", ""),
            ("Gender wage gap", f"{fmt_id(row.gender_wage_gap)} %", ""),
            ("Gap TPAK L-P", f"{fmt_id(row.gap_tpak)} poin", ""),
            ("IPM", f"{fmt_id(row.ipm)}", ""),
        ], kolom=3), unsafe_allow_html=True)
        sumber_link(*SUMBER["p6_prov"])

    # ---- Kartu detail kabupaten/kota: muncul di bawah profil provinsi bila ada yang dipilih ----
    if fokus != SEMUA and fokus in set(pp.kabkota):
        k = pp[pp.kabkota == fokus].iloc[0]
        kualitas = str(k.tpt_kualitas).strip()
        if kualitas.startswith("RSE >"):
            badge = ("merah", "TPT tidak ditampilkan BPS (RSE > 50%)")
        elif "25-50" in kualitas:
            badge = ("kuning", "TPT perlu hati-hati (RSE 25–50%)")
        else:
            badge = ("hijau", "TPT layak digunakan")
        with kartu("kabupaten"):
            st.markdown(
                f"<div class='kab-judul'><b>{fokus}</b><span class='badge {badge[0]}'>{badge[1]}</span></div>",
                unsafe_allow_html=True)
            st.markdown(ubin([
                ("TPAK", f"{fmt_id(k.tpak)} %", ""),
                ("TPT", "—" if pd.isna(k.tpt_num) else f"{fmt_id(k.tpt_num)} %", ""),
                ("Penganggur terbuka", "—" if pd.isna(k.penganggur_num) else fmt_id(k.penganggur_num, 0), ""),
                ("Usia kerja", fmt_id(k.usia_kerja, 0), ""),
                ("Angkatan kerja", fmt_id(k.angkatan_kerja, 0), ""),
                ("Bekerja", fmt_id(k.bekerja, 0), "utama"),
            ], kolom=3), unsafe_allow_html=True)
            st.markdown(
                f"<div class='bar'><div class='isi' style='width:{min(k.tpak, 100):.1f}%'></div>"
                f"<div class='tanda' style='left:{min(row.tpak, 100):.1f}%'></div></div>"
                f"<div class='bar-ket'><span>TPAK {fmt_id(k.tpak)}%</span>"
                f"<span>Garis merah: rata-rata provinsi {fmt_id(row.tpak)}%</span></div>",
                unsafe_allow_html=True)

# ------------------------------------------------------------------ KANAN: PETA
with kanan:
    with kartu("peta"):
        st.markdown("##### Peta Kabupaten/Kota")
        opsi = [SEMUA] + sorted(pp.kabkota.tolist())
        st.selectbox("Fokus wilayah", opsi, key="fokus_wilayah")

        if fokus == SEMUA or fokus not in pusat:
            zoom, (lat_c, lon_c) = zoom_semua, pusat_semua
        else:
            zoom, (lat_c, lon_c) = 8.2, pusat[fokus]

        fig = px.choropleth_map(
            pp, geojson=gj, locations="kabkota", featureidkey="properties.kabkota", color="tpak",
            color_continuous_scale=[[0, "#EEF5FB"], [0.5, "#9CC9E8"], [1, "#3B8CC4"]],
            map_style="carto-positron", zoom=zoom, opacity=0.88, center={"lat": lat_c, "lon": lon_c})
        fig.update_traces(
            marker_line_color="white", marker_line_width=1.2,
            customdata=pp[["tpak", "tpt_tampil", "bekerja"]],
            hovertemplate=("<b>%{location}</b><br>TPAK: %{customdata[0]:.2f}%"
                           "<br>TPT: %{customdata[1]}<br>Bekerja: %{customdata[2]:,.0f} orang<extra></extra>"))

        # Garis tepi tebal untuk wilayah yang dipilih (isi transparan)
        if fokus != SEMUA and fokus in pusat:
            fig.add_trace(go.Choroplethmap(
                geojson=gj, locations=[fokus], z=[0], featureidkey="properties.kabkota", showscale=False,
                colorscale=[[0, "rgba(0,0,0,0)"], [1, "rgba(0,0,0,0)"]],
                marker=dict(line=dict(color=VERMILION, width=3)), hoverinfo="skip"))

        # Gelembung proporsional: luas gelembung sebanding dengan jumlah penduduk bekerja
        bmax = float(pp.bekerja.max())

        def diameter(b):
            return 12 + 38 * math.sqrt(b / bmax)

        fig.add_trace(go.Scattermap(
            lat=[pusat[n][0] for n in pp.kabkota], lon=[pusat[n][1] for n in pp.kabkota],
            mode="markers", showlegend=False,
            marker=dict(size=[diameter(b) for b in pp.bekerja], color=ORANYE, opacity=0.62),
            customdata=pp[["kabkota", "tpak", "tpt_tampil", "bekerja"]],
            hovertemplate=("<b>%{customdata[0]}</b><br>TPAK: %{customdata[1]:.2f}%"
                           "<br>TPT: %{customdata[2]}<br>Bekerja: %{customdata[3]:,.0f} orang<extra></extra>")))
        # Nama seluruh kabupaten/kota
        fig.add_trace(go.Scattermap(
            lat=[pusat[n][0] for n in pp.kabkota], lon=[pusat[n][1] for n in pp.kabkota],
            mode="text", text=[n.replace(" ", "\n") for n in pp.kabkota], textfont=dict(size=10, color=NAVY),   # [v6.1] 2 baris
            hoverinfo="skip", showlegend=False))

        gaya_plot(fig, TINGGI_PETA, margin=dict(l=0, r=0, t=0, b=0))
        fig.update_layout(coloraxis_colorbar=dict(
            title=dict(text="TPAK (%)", side="right"), orientation="h", thickness=8, len=0.3,
            x=0.02, xanchor="left", y=0.03, yanchor="bottom", bgcolor="rgba(255,255,255,0.7)",
            tickfont=dict(size=9)))   # [v6.1] colorbar lebih ringkas
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

        # Legenda ukuran gelembung
        acuan = [bmax * 0.1, bmax * 0.4, bmax]
        item = "".join(
            f"<span class='item'><span class='gel' style='width:{diameter(b):.0f}px;height:{diameter(b):.0f}px'></span>"
            f"{fmt_id(b / 1000, 0)} rb</span>" for b in acuan)
        st.markdown(f"<div class='gel-legenda'><b>Ukuran lingkaran = jumlah penduduk bekerja:</b>{item}</div>",
                    unsafe_allow_html=True)
        sumber_link(*SUMBER["p6_kab"])

nav_bawah("pages/6_Papua_Pegunungan.py")
