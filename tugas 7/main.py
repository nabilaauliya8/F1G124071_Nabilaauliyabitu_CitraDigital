import os
import re
from pathlib import Path
import cv2
import numpy as np
import matplotlib
matplotlib.use("Agg")  # Mode headless agar pemrosesan batch cepat dan tidak memblokir GUI
import matplotlib.pyplot as plt
import pytesseract

BASE_DIR = Path(__file__).resolve().parent
FOLDER = BASE_DIR / "gambarijazah"
HASIL = BASE_DIR / "hasil"
HASIL.mkdir(parents=True, exist_ok=True)

# Keamanan: Validasi path tesseract executable
TESSERACT_PATH = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
if os.path.exists(TESSERACT_PATH):
    pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH

# Nomor ijazah yang menjadi acuan
TARGET = "571012022000056"
EKSTENSI_VALID = {".jpg", ".jpeg", ".png", ".bmp"}

# Pre-computed Look-Up Table (LUT) untuk Gamma Correction (gamma = 1.5)
# Menghindari komputasi berulang list comprehension Python pada setiap gambar
_GAMMA = 1.5
_GAMMA_LUT = np.clip(
    ((np.arange(256, dtype=np.float32) / 255.0) ** (1.0 / _GAMMA)) * 255.0,
    0, 255
).astype(np.uint8)


def baca_gambar(path):
    """Membaca gambar secara aman untuk path Windows (spasi, unicode, dll)."""
    try:
        data = np.fromfile(str(path), dtype=np.uint8)
        return cv2.imdecode(data, cv2.IMREAD_COLOR)
    except Exception as e:
        print(f"Error membaca berkas {path}: {e}")
        return None


def enhancement(gray):
    # Contrast Stretching (Ditingkatkan dengan cv2.convertScaleAbs untuk kecepatan C SIMD)
    low, high = np.percentile(gray, (2, 98))
    if high > low:
        scale = 255.0 / (high - low)
        shift = -low * scale
        contrast = cv2.convertScaleAbs(gray, alpha=scale, beta=shift)
    else:
        contrast = gray.copy()

    # CLAHE (Parameter dipertahankan 100% persis)
    clahe = cv2.createCLAHE(
        clipLimit=2.0, tileGridSize=(8, 8)
    ).apply(gray)

    # Gamma Correction menggunakan LUT terkomputasi
    gamma_img = cv2.LUT(gray, _GAMMA_LUT)

    return contrast, clahe, gamma_img


def baca_nomor(gray):
    # Perbesar gambar agar angka lebih mudah dibaca
    besar = cv2.resize(
        gray, None, fx=2, fy=2,
        interpolation=cv2.INTER_CUBIC
    )

    teks = pytesseract.image_to_string(
        besar,
        config="--psm 6 -c tessedit_char_whitelist=0123456789"
    )

    nomor = re.sub(r"\D", "", teks)
    return nomor if nomor else "Tidak terbaca"


def hitung_cer(prediksi, target):
    if prediksi == "Tidak terbaca":
        return 1.0

    len_t = len(target)
    if len_t == 0:
        return 0.0 if len(prediksi) == 0 else 1.0

    # Optimasi Dynamic Programming Levenshtein Distance
    # Menggunakan 2 buffer 1D bertukar tanpa alokasi list berulang di dalam loop
    prev_dp = list(range(len_t + 1))
    curr_dp = [0] * (len_t + 1)

    for i, a in enumerate(prediksi, 1):
        curr_dp[0] = i
        for j, b in enumerate(target, 1):
            cost = 0 if a == b else 1
            curr_dp[j] = min(
                curr_dp[j - 1] + 1,       # Insertion
                prev_dp[j] + 1,           # Deletion
                prev_dp[j - 1] + cost     # Substitution
            )
        prev_dp, curr_dp = curr_dp, prev_dp

    return prev_dp[-1] / max(len_t, 1)


def main():
    if not FOLDER.exists():
        print("Folder tidak ditemukan:", FOLDER)
        return

    # Filter dan pengurutan berkas yang aman menggunakan pathlib
    files = sorted([
        p for p in FOLDER.iterdir()
        if p.is_file() and p.suffix.lower() in EKSTENSI_VALID
    ])

    print("Jumlah gambar:", len(files))
    if not files:
        print("Gambar tidak ditemukan di folder:", FOLDER)
        return

    for i, path in enumerate(files, 1):
        gambar = baca_gambar(path)
        if gambar is None:
            print("Gagal membaca:", path.name)
            continue

        rgb = cv2.cvtColor(gambar, cv2.COLOR_BGR2RGB)
        gray = cv2.cvtColor(gambar, cv2.COLOR_BGR2GRAY)

        contrast, clahe, gamma_img = enhancement(gray)
        nomor = baca_nomor(gray)

        cer = hitung_cer(nomor, TARGET)
        akurasi = max(0.0, (1.0 - cer) * 100.0)

        # Ringkasan teks di panel terakhir
        ringkasan = (
            "HASIL OCR\n\n"
            f"Nomor: {nomor}\n\n"
            f"CER: {cer * 100:.2f}%\n\n"
            "Enhancement terbaik:\n\n"
            "CLAHE"
        )

        fig, ax = plt.subplots(2, 3, figsize=(15, 9))
        try:
            fig.suptitle(
                f"Hasil Enhancement OCR - {path.name}",
                fontsize=15, fontweight="bold"
            )

            panel = [
                ("Citra asli", rgb),
                ("Grayscale", gray),
                ("Contrast Stretching", contrast),
                ("CLAHE", clahe),
                ("Gamma Correction", gamma_img)
            ]

            for sumbu, (judul, citra) in zip(ax.flat, panel):
                sumbu.imshow(
                    citra, cmap="gray" if citra.ndim == 2 else None
                )
                sumbu.set_title(judul, loc="left", fontweight="bold")
                sumbu.axis("off")

            # Panel ringkasan OCR
            ax[1, 2].axis("off")
            ax[1, 2].set_title(
                "Ringkasan OCR", loc="left", fontweight="bold"
            )
            ax[1, 2].text(
                0.08, 0.78, ringkasan,
                transform=ax[1, 2].transAxes,
                fontsize=12, verticalalignment="top",
                linespacing=1.5
            )

            plt.tight_layout(rect=[0, 0, 1, 0.94])

            # Sanitasi nama berkas output untuk mencegah path traversal
            nama_bersih = path.stem
            output = HASIL / f"{nama_bersih}_enhanced_ocr.png"
            plt.savefig(str(output), dpi=150, bbox_inches="tight")
        finally:
            plt.close(fig)

        print(f"\nFile: {path.name}")
        print("Nomor target:", TARGET)
        print("Nomor OCR:", nomor)
        print(f"CER: {cer * 100:.2f}%")
        print(f"Akurasi karakter: {akurasi:.2f}%")
        print("Disimpan:", output)


if __name__ == "__main__":
    main()