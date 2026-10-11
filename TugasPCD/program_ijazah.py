import cv2
import os
import numpy as np
import matplotlib.pyplot as plt

# Membuat folder hasil
os.makedirs("enhancement", exist_ok=True)
os.makedirs("grafik_histogram", exist_ok=True)
os.makedirs("ocr", exist_ok=True)

# Nama file gambar
files = [
    "01_HighQuality_Enhanced.jpg",
    "02_LowContrast.jpg",
    "03_Blurred (1).jpg",
    "04_HighNoise (1).jpg",
    "05_LowResolution_Upsampled (1).jpg",
    "06_Faded_Underexposed (1).jpg",
    "07_ColorShift_WarmTint (1).jpg",
    "08_JPEGCompression_Artifacts (1).jpg",
    "09_CombinedDegradation (1).jpg"
]

for i, file in enumerate(files, 1):

    # Membaca gambar
    path = os.path.join("gambar no ijazah", file)
    img = cv2.imread(path)

    if img is None:
        print(f"{file} tidak ditemukan!")
        continue

    # Grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # ==================================
    # 1. BRIGHTNESS ADJUSTMENT
    # ==================================
    brightness = cv2.convertScaleAbs(
        gray, alpha=1, beta=20
    )

    # ==================================
    # 2. CONTRAST STRETCHING
    # ==================================
    mn = np.min(gray)
    mx = np.max(gray)

    if mx != mn:
        contrast = (
            (gray - mn) /
            (mx - mn) * 255
        ).astype(np.uint8)
    else:
        contrast = gray.copy()

    # ==================================
    # 3. HISTOGRAM EQUALIZATION
    # ==================================
    equalization = cv2.equalizeHist(gray)

    # ==================================
    # SIMPAN HASIL ENHANCEMENT
    # ==================================
    cv2.imwrite(
        f"enhancement/sebelum_{i}.jpg",
        gray
    )

    cv2.imwrite(
        f"enhancement/brightness_{i}.jpg",
        brightness
    )

    cv2.imwrite(
        f"enhancement/contrast_{i}.jpg",
        contrast
    )

    cv2.imwrite(
        f"enhancement/equalization_{i}.jpg",
        equalization
    )

    # ==================================
    # PERBANDINGAN CITRA
    # ==================================
    hasil = [
        (gray, "Sebelum Enhancement"),
        (brightness, "Brightness Adjustment"),
        (contrast, "Contrast Stretching"),
        (equalization, "Histogram Equalization")
    ]

    plt.figure(figsize=(12, 8))

    for j, (gambar, judul) in enumerate(hasil, 1):
        plt.subplot(2, 2, j)
        plt.imshow(gambar, cmap="gray")
        plt.title(judul)
        plt.axis("off")

    plt.suptitle(
        f"Perbandingan Enhancement Nomor Ijazah {i}"
    )

    plt.tight_layout()

    plt.savefig(
        f"enhancement/perbandingan_{i}.jpg",
        dpi=300
    )

    plt.show()
    plt.close()

    # ==================================
    # HISTOGRAM SEBELUM & SESUDAH
    # ==================================
    plt.figure(figsize=(12, 8))

    for j, (gambar, judul) in enumerate(hasil, 1):
        plt.subplot(2, 2, j)

        plt.hist(
            gambar.ravel(),
            256,
            [0, 256]
        )

        plt.title(judul)
        plt.xlabel("Intensitas Piksel")
        plt.ylabel("Jumlah Piksel")

    plt.suptitle(
        f"Grafik Histogram Nomor Ijazah {i}"
    )

    plt.tight_layout()

    plt.savefig(
        f"grafik_histogram/histogram_{i}.jpg",
        dpi=300
    )

    plt.show()
    plt.close()

    print(f"Ijazah {i} selesai.")

print("\n===================================")
print("SEMUA GAMBAR SELESAI DIPROSES")
print("===================================")
print("Hasil enhancement  : folder enhancement")
print("Grafik histogram   : folder grafik_histogram")
print("Folder OCR         : folder ocr")