import os
from pathlib import Path

import cv2
import numpy as np
import matplotlib
matplotlib.use("Agg")  # simpan ke file saja, tanpa membuka jendela per gambar
import matplotlib.pyplot as plt
import pytesseract

# ------------------------------------------------------------------
# PENGATURAN & KONSTANTA MODUL
# ------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent
FOLDER_INPUT = BASE_DIR / "gambarijazah"
FOLDER_HASIL = BASE_DIR / "hasil"
EKSTENSI = {".jpg", ".jpeg", ".png", ".bmp"}

TESSERACT_PATH = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
if os.path.exists(TESSERACT_PATH):
    pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH

BAHASA = "eng"      # "ind+eng" jika data bahasa Indonesia sudah dipasang
MIN_CONF = 30       # confidence minimum teks OCR

# Kernel morfologi ter-alokasi awal untuk efisiensi eksekusi
KERNEL_ELLIPSE_3X3 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
KERNEL_DILATE_5X5 = np.ones((5, 5), np.uint8)


def baca_gambar(path):
    """Baca gambar dengan aman untuk path Windows (spasi, kurung, dll)."""
    try:
        data = np.fromfile(str(path), dtype=np.uint8)
        return cv2.imdecode(data, cv2.IMREAD_COLOR)
    except Exception as e:
        print(f"Error membaca berkas {path}: {e}")
        return None


def proses_gambar(path_gambar):
    img_bgr = baca_gambar(path_gambar)
    if img_bgr is None:
        print(f"  [LEWATI] Gagal membaca: {path_gambar.name}")
        return None

    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)

    # --- Grayscale ---
    gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)

    # --- Deteksi teks OCR + mask ---
    data = pytesseract.image_to_data(
        gray, lang=BAHASA, output_type=pytesseract.Output.DICT
    )
    ocr_vis = cv2.cvtColor(gray, cv2.COLOR_GRAY2RGB)
    text_mask = np.zeros(gray.shape, dtype=np.uint8)

    # Optimasi: Ekstrak list dari dictionary sekali untuk menghindari lookup berulang
    texts = data["text"]
    confs = data["conf"]
    lefts = data["left"]
    tops = data["top"]
    widths = data["width"]
    heights = data["height"]

    n_items = len(texts)
    for i in range(n_items):
        teks = texts[i].strip()
        try:
            conf = float(confs[i])
        except (ValueError, TypeError):
            conf = -1.0

        if teks == "" or conf < MIN_CONF:
            continue

        x, y = lefts[i], tops[i]
        w, h = widths[i], heights[i]
        cv2.rectangle(ocr_vis, (x, y), (x + w, y + h), (255, 0, 0), 2)
        cv2.rectangle(text_mask, (x, y), (x + w, y + h), 255, -1)

    text_mask = cv2.dilate(text_mask, KERNEL_DILATE_5X5, iterations=2)
    gray_clean = cv2.inpaint(gray, text_mask, 3, cv2.INPAINT_TELEA)

    # --- Thresholding (tanda tangan putih, latar gelap) ---
    blur = cv2.GaussianBlur(gray_clean, (5, 5), 0)

    _, th_global = cv2.threshold(blur, 127, 255, cv2.THRESH_BINARY_INV)
    _, th_otsu = cv2.threshold(
        blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU
    )
    th_adaptive = cv2.adaptiveThreshold(
        blur, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY_INV,
        blockSize=31, C=10,
    )

    # --- Morfologi pada hasil Otsu ---
    opening = cv2.morphologyEx(th_otsu, cv2.MORPH_OPEN, KERNEL_ELLIPSE_3X3)
    closing = cv2.morphologyEx(th_otsu, cv2.MORPH_CLOSE, KERNEL_ELLIPSE_3X3)

    return [
        ("Citra asli", img_rgb, None),
        ("Grayscale", gray, "gray"),
        ("Deteksi teks OCR", ocr_vis, None),
        ("Global Thresholding", th_global, "gray"),
        ("Otsu Thresholding", th_otsu, "gray"),
        ("Adaptive Thresholding", th_adaptive, "gray"),
        ("Morphological Opening", opening, "gray"),
        ("Morphological Closing", closing, "gray"),
    ]


def simpan_grid(tampilan, path_output):
    fig, axes = plt.subplots(4, 2, figsize=(10, 16))
    try:
        for ax, (judul, gambar, cmap) in zip(axes.ravel(), tampilan):
            ax.imshow(gambar, cmap=cmap)
            ax.set_title(judul, fontsize=11, fontweight="bold", loc="left")
            ax.axis("off")
        plt.tight_layout()
        fig.savefig(str(path_output), dpi=200, bbox_inches="tight")
    finally:
        plt.close(fig)


def main():
    if not FOLDER_INPUT.exists():
        raise FileNotFoundError(f"Folder tidak ditemukan: {FOLDER_INPUT}")

    FOLDER_HASIL.mkdir(exist_ok=True)

    daftar = sorted(
        p for p in FOLDER_INPUT.iterdir()
        if p.is_file() and p.suffix.lower() in EKSTENSI
    )
    print(f"Ditemukan {len(daftar)} gambar di '{FOLDER_INPUT.name}'.\n")

    for n, path in enumerate(daftar, start=1):
        print(f"[{n}/{len(daftar)}] {path.name}")
        tampilan = proses_gambar(path)
        if tampilan is None:
            continue

        # "01_HighQuality_Enhanced (1).jpg" -> "01_HighQuality_Enhanced_deteksi.jpg"
        nama_bersih = path.stem.replace(" (1)", "")
        path_output = FOLDER_HASIL / f"{nama_bersih}_deteksi.jpg"
        simpan_grid(tampilan, path_output)
        print(f"  -> {path_output.name}")

    print(f"\nSelesai. Semua hasil ada di folder: {FOLDER_HASIL}")


if __name__ == "__main__":
    main()