# PENGATURAN TAMPILAN
# True  = tampilan baru (latar berlapis, kartu bergaris warna, dock navigasi melayang, hero halaman 1).
# False = tampilan polos tahap 1 (hanya rapi, tanpa hiasan). Berguna untuk membandingkan.
UI_BARU = True

# Judul dan subjudul tiap halaman
JUDUL = {
    "p2": "Apa yang Dimaksud “Bekerja”?",
    "p3": "Penduduk Menurut Jenis Kegiatan, Agustus 2021-2025",
    "p4": "Kelayakan Kerja: Hubungan Antar 9 Variabel",
    "p5": "38 Provinsi, Terbagi Menjadi 3 Kelompok",
    "p6": "Mari Melihat Papua Pegunungan dengan Lebih Detail",
    "p7": "Kesimpulan",
}

# URL repositori GitHub.
GITHUB_URL = "https://github.com/JosiIntan/dashboard_kerja_rentan.git "
PENULIS = "-Josi Intan Tri Rizki-"

SUMBER = {
    "p1": ("Tabel Dinamis BPS Tingkat Pengangguran Terbuka (TPT) di Indonesia Tahun 2021 - 2025",
           "https://www.bps.go.id", "28 September 2026"),
    "p3": ("Tabel Dinamis BPS Penduduk Menurut Jenis Kegiatan di Indonesia Tahun 2021 - 2025",
           "https://www.bps.go.id", "28 September 2026"),
    "p4": ("Publikasi BPS Indikator Pasar Tenaga Kerja Indonesia Agustus 2025 & Indeks Pembangunan Manusia 2025",
           "https://www.bps.go.id", "28 September 2026"),
    "p5": ("Publikasi BPS Keadaan Angkatan Kerja Indonesia Agustus 2025",
           "https://www.bps.go.id", "28 September 2026"),
    "p6_prov": ("Publikasi BPS Keadaan Angkatan Kerja Indonesia Agustus 2025",
                "https://www.bps.go.id", "28 September 2026"),
    "p6_kab": ("Publikasi BPS Profil Ketenagakerjaan Papua Pegunungan Tahun 2025",
               "https://papua-pegunungan.bps.go.id", "28 September 2026"),
}

P1_PENUTUP = ("Indonesia cenderung mengalami penurunan tingkat pengangguran terbuka, "
              "apakah ini sesuatu hal yang baik?")

P2_CAPTION = "Diagram Struktur Klasifikasi Ketenagakerjaan Berdasarkan BPS."

P3_INTRO = ("Halaman sebelumnya menunjukkan definisi &ldquo;bekerja&rdquo; secara konsep. "
            "Sekarang seberapa besar tiap cabang?")

P4_INTRO = (
    "Halaman sebelumnya meringkas semua provinsi jadi satu angka. Untuk membandingkan 38 provinsi "
    "secara adil, kita butuh lebih dari sekadar TPT. Kelayakan suatu pekerjaan tidak bisa dilihat "
    "dari satu indikator saja. ILO (2013) mendefinisikan pekerjaan layak lewat banyak dimensi seperti "
    "kesempatan kerja, upah yang memadai, jam kerja yang wajar, stabilitas kerja, dan kesetaraan. "
    "Sembilan variabel berikut (TPAK, IPM, Gap TPAK, Gap Upah, Persentase Pekerja Informal, "
    "Jam Kerja Kurang dari 35 Jam, Jam Kerja Lebih dari 49 Jam, Rata-rata Upah, dan TPT) "
    "mewakili lima dimensi tersebut, dipilih agar tidak saling tumpang tindih secara definisi."
)

P5_MENENGAH = ("yang beranggotakan {n} provinsi memiliki ciri utama berupa angka-angka ketenagakerjaan "
               "mendekati rata-rata nasional di hampir semua indikator dan tidak menonjol ke arah "
               "rentan maupun mapan.")
P5_URBAN = ("yang beranggotakan {n} provinsi (termasuk DKI Jakarta, Jawa Barat, Banten) memiliki ciri utama berupa "
            "rata-rata upah yang tinggi dan persentase informalitas yang rendah, tetapi memiliki angka TPT tertinggi" 
            "dibandingkan ketiga kelompok.")
P5_RENTAN = ("yang beranggotakan {n} provinsi (NTT, Papua Tengah, Papua Pegunungan) memiliki ciri utama berupa angka TPAK "
             "yang tinggi dan TPT yang rendah dibandingkan ketiga kelompok, tetapi memiliki persentase informalitas dan proporsi "
             "jam kerja singkat yang jauh di atas kelompok lainnya, serta IPM terendah.")
P5_PENCILAN = ("merupakan pencilan paling ekstrem dimana jarak dari pusat paling besar dan terlihat juga dari angka"
               "partisipasi kerja tertinggi nasional, namun searah dengan indikator informalitas dan jam kerja "
               "pendek, berlawanan arah dengan IPM.")

P6_INTRO = ("Papua Pegunungan adalah pencilan paling ekstrem di antara 38 provinsi. "
            "Sekarang kita perbesar ke tingkat kabupaten/kota.")

P7_KESIMPULAN = (
    "TPT yang rendah sering dipandang sebagai tanda keberhasilan pasar kerja. Padahal, indikator ini hanya "
    "menunjukkan proporsi penduduk angkatan kerja yang tidak bekerja dan sedang mencari pekerjaan. Seseorang "
    "yang bekerja, meskipun hanya satu jam dalam seminggu, tidak lagi dikategorikan sebagai pengangguran. "
    "Kondisi ini menjadi penting ketika pekerjaan yang dijalani bersifat informal, berjam kerja pendek "
    "(kurang dari 35 jam), atau diterima karena keterpaksaan demi bertahan hidup. "
    "<b>Papua Pegunungan</b> menjadi contoh yang menunjukkan mengapa TPT tidak dapat dibaca secara tunggal. "
    "Provinsi ini memiliki TPT terendah sekaligus TPAK tertinggi di Indonesia, tetapi justru menjadi pencilan "
    "paling ekstrem dalam profil kerentanan kerja. Kondisi tersebut ditandai oleh tingkat informalitas dan "
    "proporsi pekerja dengan jam kerja pendek yang jauh lebih tinggi dibandingkan provinsi lain, serta IPM "
    "terendah secara nasional. Dengan demikian, TPT yang rendah di Papua Pegunungan tidak serta-merta "
    "menunjukkan pasar kerja yang sehat. Rendahnya pengangguran dapat berjalan bersamaan dengan tingginya "
    "kerentanan pekerja, terutama ketika masyarakat tetap bekerja dalam kondisi informal dan jam kerja yang "
    "terbatas. Karena itu, TPT sebaiknya dibaca bersama indikator lain seperti informalitas, jam kerja, upah, "
    "dan kualitas pembangunan manusia, bukan berdiri sendiri sebagai penanda keberhasilan pasar kerja."
)

P7_KETERBATASAN = (
    "Pada tingkat kabupaten, data TPT tersedia untuk seluruh 8 kabupaten di Papua Pegunungan, tetapi tidak "
    "semua estimasinya dapat ditampilkan. Beberapa kabupaten memiliki RSE berkisar 25–50%, sehingga estimasinya "
    "perlu digunakan dengan hati-hati. Sementara itu, kabupaten dengan RSE di atas 50% tidak ditampilkan oleh "
    "BPS karena reliabilitas estimasinya rendah. Kondisi ini perlu diperhatikan ketika membandingkan TPT "
    "antarkabupaten di Papua Pegunungan."
)
