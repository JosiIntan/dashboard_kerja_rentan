# Bekerja Saja Belum Cukup — UAS Visualisasi Data dan Informasi 2026

## Menjalankan
```
pip install -r requirements.txt
streamlit run app.py
```

## Di mana mengedit apa
- **Semua teks** (pengantar, kesimpulan, sumber, judul, nama penulis, URL GitHub): `konten.py`
- **Tampilan polos vs tampilan baru**: `UI_BARU = True/False` di `konten.py`
- **Ukuran grafik** (Kompak / Normal / Besar): sidebar, buka lewat panah kecil di kiri atas
- Desain bersama (warna, kartu, navigasi): `utils.py`

## Catatan perubahan (v4 -> v6)
Tiap berkas punya blok "CATATAN PERUBAHAN" di bagian atas dan penanda `[v5]` / `[v6]` di komentar.
- v5 = perapian: biplot, peta, circle packing, matriks, breadcrumb, hapus legenda, hapus ikon tautan judul
- v6 = UI/UX: latar berlapis, kartu bergaris tiga warna, judul + subjudul baru, dock navigasi, hero halaman 1,
  tata letak satu layar, responsif untuk layar kecil

## Berkas baru v6.1
- `komponen.py`: icicle interaktif (klik = zoom-in, breadcrumb besar, angka di kiri) untuk halaman 3

## Struktur
app.py (router + sidebar), konten.py, utils.py, pages/1-7, data/processed/, .streamlit/config.toml
