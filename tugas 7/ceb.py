import os
from pathlib import Path
import cv2
import numpy as np
import matplotlib
matplotlib.use("Agg")  # Mode headless agar eksekusi cepat dan aman tanpa memblokir GUI
import matplotlib.pyplot as plt

BASE_DIR = Path(__file__).resolve().parent
FOLDER = BASE_DIR / "gambarijazah"
HASIL = BASE_DIR / "hasil"
HASIL.mkdir(parents=True, exist_ok=True)

EKSTENSI_VALID = {".jpg", ".jpeg", ".png", ".bmp"}
KERNEL_3X3 = np.ones((3, 3), np.uint8)  # Pre-allocated kernel constant untuk morfologi


def baca_gambar(path):
    """Membaca gambar secara aman untuk path Windows (spasi, unicode, dll)."""
    try:
        data = np.fromfile(str(path), dtype=np.uint8)
        return cv2.imdecode(data, cv2.IMREAD_COLOR)
    except Exception as e:
        print(f"Error membaca berkas {path}: {e}")
        return None


def deteksi_tanda_tangan(gray):
    h, w = gray.shape
    area = gray[
        int(h * 0.25):int(h * 0.75),
        int(w * 0.10):int(w * 0.90)
    ]

    _, otsu = cv2.threshold(
        area, 0, 255,
        cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU
    )

    opening = cv2.morphologyEx(
        otsu, cv2.MORPH_OPEN, KERNEL_3X3
    )
    closing = cv2.morphologyEx(
        opening, cv2.MORPH_CLOSE, KERNEL_3X3
    )

    rasio = cv2.countNonZero(closing) / closing.size
    status = "PRESENT" if rasio > 0.01 else "ABSENT"

    return area, otsu, opening, closing, status


def main():
    if not FOLDER.exists():
        print("Gambar tidak ditemukan:", FOLDER)
        return

    files = sorted([
        p for p in FOLDER.iterdir()
        if p.is_file() and p.suffix.lower() in EKSTENSI_VALID
    ])

    if not files:
        print("Gambar tidak ditemukan:", FOLDER)
        return

    for path in files:
        gambar = baca_gambar(path)
        if gambar is None:
            continue

        gray = cv2.cvtColor(gambar, cv2.COLOR_BGR2GRAY)
        area, otsu, opening, closing, status = deteksi_tanda_tangan(gray)

        print(path.name, ":", status)
        print("Piksel foreground:", cv2.countNonZero(closing))

        panel = [
            ("Citra asli", cv2.cvtColor(gambar, cv2.COLOR_BGR2RGB)),
            ("Grayscale", gray),
            ("Area tanda tangan", area),
            ("Otsu Thresholding", otsu),
            ("Morphological Opening", opening),
            ("Morphological Closing", closing)
        ]

        fig, ax = plt.subplots(2, 3, figsize=(14, 8))
        try:
            fig.suptitle(
                f"Deteksi Tanda Tangan: {status}\n"
                f"{path.name}"
            )

            for sumbu, (judul, citra) in zip(ax.flat, panel):
                sumbu.imshow(
                    citra, cmap="gray" if citra.ndim == 2 else None
                )
                sumbu.set_title(judul)
                sumbu.axis("off")

            plt.tight_layout()
            nama_bersih = path.stem
            output = HASIL / f"{nama_bersih}_tanda_tangan.png"
            plt.savefig(str(output), dpi=150, bbox_inches="tight")
        finally:
            plt.close(fig)


if __name__ == "__main__":
    main()