from pathlib import Path
import re
from difflib import SequenceMatcher


# ============================================================
# KONFIGURASI
# ============================================================

FOLDER_OCR = Path("hasil/ocr")
FILE_HASIL = Path("hasil/ocr/evaluasi_ocr.txt")


# ============================================================
# GROUND TRUTH
# ============================================================
# Masukkan nomor ijazah yang benar.
# Jika semua 9 gambar adalah nomor ijazah yang sama,
# cukup tulis satu kali di sini.

GROUND_TRUTH = "571012022000056"


# ============================================================
# DAFTAR GAMBAR
# ============================================================

daftar_gambar = [
    "01_HighQuality_Enhanced (1).jpg",
    "02_LowContrast (1).jpg",
    "03_Blurred (1).jpg",
    "04_HighNoise (1).jpg",
    "05_LowResolution_Upsampled (1).jpg",
    "06_Faded_Underexposed (1).jpg",
    "07_ColorShift_WarmTint (1).jpg",
    "08_JPEGCompression_Artifacts (1).jpg",
    "09_CombinedDegradation (1).jpg"
]


# ============================================================
# METODE OCR
# ============================================================

metode_list = [
    "Original",
    "Mean Filter",
    "Median Filter",
    "Gaussian Filter",
    "Sharpening"
]


# ============================================================
# NORMALISASI TEKS
# ============================================================

def normalisasi_teks(teks):

    if teks is None:
        return ""

    # Ubah menjadi huruf besar
    teks = teks.upper()

    # Hanya mengambil huruf dan angka
    teks = re.sub(r"[^A-Z0-9]", "", teks)

    return teks


# ============================================================
# HITUNG KARAKTER BENAR
# ============================================================

def hitung_karakter_benar(hasil_ocr, ground_truth):

    hasil_ocr = normalisasi_teks(hasil_ocr)
    ground_truth = normalisasi_teks(ground_truth)

    if hasil_ocr == "":
        return 0

    matcher = SequenceMatcher(
        None,
        ground_truth,
        hasil_ocr
    )

    matching_blocks = matcher.get_matching_blocks()

    karakter_benar = 0

    for block in matching_blocks:
        karakter_benar += block.size

    return karakter_benar


# ============================================================
# HITUNG AKURASI
# ============================================================

def hitung_akurasi(hasil_ocr, ground_truth):

    ground_truth = normalisasi_teks(
        ground_truth
    )

    if ground_truth == "":
        return 0.0

    karakter_benar = hitung_karakter_benar(
        hasil_ocr,
        ground_truth
    )

    akurasi = (
        karakter_benar /
        len(ground_truth)
    ) * 100

    if akurasi > 100:
        akurasi = 100.0

    return akurasi


# ============================================================
# MEMBACA HASIL OCR
# ============================================================

def baca_hasil_ocr(file_ocr):

    hasil = {}

    if not file_ocr.exists():
        return hasil

    teks = file_ocr.read_text(
        encoding="utf-8"
    )

    # Mencari bagian:
    # ORIGINAL:
    # MEAN FILTER:
    # MEDIAN FILTER:
    # GAUSSIAN FILTER:
    # SHARPENING:

    pola = {
        "Original":
            r"ORIGINAL:\s*(.*?)(?=\n\nMEAN FILTER:|\Z)",

        "Mean Filter":
            r"MEAN FILTER:\s*(.*?)(?=\n\nMEDIAN FILTER:|\Z)",

        "Median Filter":
            r"MEDIAN FILTER:\s*(.*?)(?=\n\nGAUSSIAN FILTER:|\Z)",

        "Gaussian Filter":
            r"GAUSSIAN FILTER:\s*(.*?)(?=\n\nSHARPENING:|\Z)",

        "Sharpening":
            r"SHARPENING:\s*(.*?)(?=\n\n|\Z)"
    }

    for metode, regex in pola.items():

        match = re.search(
            regex,
            teks,
            re.IGNORECASE |
            re.DOTALL
        )

        if match:

            hasil_ocr = match.group(1).strip()

            if hasil_ocr == "":
                hasil_ocr = "Tidak terbaca"

            hasil[metode] = hasil_ocr

        else:

            hasil[metode] = "Tidak terbaca"

    return hasil


# ============================================================
# FORMAT TABEL
# ============================================================

LEBAR_METODE = 20
LEBAR_OCR = 30
LEBAR_BENAR = 18
LEBAR_AKURASI = 12


def garis_tabel():

    return (
        "+"
        + "-" * LEBAR_METODE
        + "+"
        + "-" * LEBAR_OCR
        + "+"
        + "-" * LEBAR_BENAR
        + "+"
        + "-" * LEBAR_AKURASI
        + "+"
    )


def header_tabel():

    return (
        "| "
        + "Metode".ljust(
            LEBAR_METODE - 2
        )
        + "| "
        + "Hasil OCR".ljust(
            LEBAR_OCR - 2
        )
        + "| "
        + "Karakter Benar".ljust(
            LEBAR_BENAR - 2
        )
        + "| "
        + "Akurasi".ljust(
            LEBAR_AKURASI - 2
        )
        + "|"
    )


def baris_tabel(
    metode,
    hasil_ocr,
    karakter_benar,
    akurasi
):

    if len(hasil_ocr) > LEBAR_OCR - 3:

        hasil_ocr = (
            hasil_ocr[:LEBAR_OCR - 6]
            + "..."
        )

    return (
        "| "
        + metode.ljust(
            LEBAR_METODE - 2
        )
        + "| "
        + hasil_ocr.ljust(
            LEBAR_OCR - 2
        )
        + "| "
        + str(
            karakter_benar
        ).ljust(
            LEBAR_BENAR - 2
        )
        + "| "
        + f"{akurasi:.2f}%".ljust(
            LEBAR_AKURASI - 2
        )
        + "|"
    )


# ============================================================
# PROSES EVALUASI
# ============================================================

semua_hasil = []

total_karakter = (
    len(normalisasi_teks(GROUND_TRUTH))
    * len(daftar_gambar)
)


# ============================================================
# EVALUASI SETIAP GAMBAR
# ============================================================

for nomor, nama_file in enumerate(
    daftar_gambar,
    start=1
):

    nama = Path(
        nama_file
    ).stem

    file_ocr = (
        FOLDER_OCR
        / f"ocr_{nama}.txt"
    )

    hasil_ocr = baca_hasil_ocr(
        file_ocr
    )

    semua_hasil.append(
        "=" * 100
    )

    semua_hasil.append(
        f"CITRA {nomor:02d}"
    )

    semua_hasil.append(
        f"Nama File : {nama_file}"
    )

    semua_hasil.append(
        f"Ground Truth : {GROUND_TRUTH}"
    )

    semua_hasil.append("")

    # Header tabel
    semua_hasil.append(
        garis_tabel()
    )

    semua_hasil.append(
        header_tabel()
    )

    semua_hasil.append(
        garis_tabel()
    )

    # --------------------------------------------------------
    # EVALUASI SETIAP METODE
    # --------------------------------------------------------

    for metode in metode_list:

        teks_ocr = hasil_ocr.get(
            metode,
            "Tidak terbaca"
        )

        karakter_benar = (
            hitung_karakter_benar(
                teks_ocr,
                GROUND_TRUTH
            )
        )

        akurasi = (
            hitung_akurasi(
                teks_ocr,
                GROUND_TRUTH
            )
        )

        semua_hasil.append(
            baris_tabel(
                metode,
                teks_ocr,
                karakter_benar,
                akurasi
            )
        )

    semua_hasil.append(
        garis_tabel()
    )

    semua_hasil.append("")
    semua_hasil.append("")


# ============================================================
# REKAP AKURASI SEMUA GAMBAR
# ============================================================

semua_hasil.append(
    "=" * 100
)

semua_hasil.append(
    "REKAP HASIL OCR SEMUA CITRA"
)

semua_hasil.append(
    "=" * 100
)

semua_hasil.append("")


# ============================================================
# TABEL REKAP
# ============================================================

R_LEBAR_METODE = 20
R_LEBAR_BENAR = 24
R_LEBAR_TOTAL = 18
R_LEBAR_AKURASI = 12


def garis_rekap():

    return (
        "+"
        + "-" * R_LEBAR_METODE
        + "+"
        + "-" * R_LEBAR_BENAR
        + "+"
        + "-" * R_LEBAR_TOTAL
        + "+"
        + "-" * R_LEBAR_AKURASI
        + "+"
    )


semua_hasil.append(
    garis_rekap()
)

semua_hasil.append(
    "| "
    + "Metode".ljust(
        R_LEBAR_METODE - 2
    )
    + "| "
    + "Karakter Benar".ljust(
        R_LEBAR_BENAR - 2
    )
    + "| "
    + "Total Karakter".ljust(
        R_LEBAR_TOTAL - 2
    )
    + "| "
    + "Akurasi".ljust(
        R_LEBAR_AKURASI - 2
    )
    + "|"
)

semua_hasil.append(
    garis_rekap()
)


# ============================================================
# HITUNG REKAP SETIAP METODE
# ============================================================

for metode in metode_list:

    total_benar = 0

    for nomor, nama_file in enumerate(
        daftar_gambar,
        start=1
    ):

        nama = Path(
            nama_file
        ).stem

        file_ocr = (
            FOLDER_OCR
            / f"ocr_{nama}.txt"
        )

        hasil_ocr = baca_hasil_ocr(
            file_ocr
        )

        teks_ocr = hasil_ocr.get(
            metode,
            "Tidak terbaca"
        )

        karakter_benar = (
            hitung_karakter_benar(
                teks_ocr,
                GROUND_TRUTH
            )
        )

        total_benar += karakter_benar

    if total_karakter > 0:

        akurasi_total = (
            total_benar /
            total_karakter
        ) * 100

    else:

        akurasi_total = 0.0

    semua_hasil.append(
        "| "
        + metode.ljust(
            R_LEBAR_METODE - 2
        )
        + "| "
        + str(
            total_benar
        ).ljust(
            R_LEBAR_BENAR - 2
        )
        + "| "
        + str(
            total_karakter
        ).ljust(
            R_LEBAR_TOTAL - 2
        )
        + "| "
        + f"{akurasi_total:.2f}%".ljust(
            R_LEBAR_AKURASI - 2
        )
        + "|"
    )


semua_hasil.append(
    garis_rekap()
)


# ============================================================
# SIMPAN HASIL
# ============================================================

FILE_HASIL.parent.mkdir(
    parents=True,
    exist_ok=True
)

FILE_HASIL.write_text(
    "\n".join(semua_hasil),
    encoding="utf-8"
)


# ============================================================
# TAMPILKAN HASIL
# ============================================================

print(
    "\n".join(semua_hasil)
)

print("")
print("=" * 100)
print("EVALUASI OCR SELESAI")
print("=" * 100)

print(
    f"Hasil disimpan di: {FILE_HASIL}"
)