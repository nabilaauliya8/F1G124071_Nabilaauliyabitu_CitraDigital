import cv2
import os
import numpy as np
import matplotlib.pyplot as plt

# ==========================================
# NAMA FILE GAMBAR
# ==========================================

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

# ==========================================
# MEMBUAT FOLDER HASIL
# ==========================================

os.makedirs("hasil/grayscale", exist_ok=True)
os.makedirs("hasil/mean", exist_ok=True)
os.makedirs("hasil/median", exist_ok=True)
os.makedirs("hasil/gaussian", exist_ok=True)
os.makedirs("hasil/sharpening", exist_ok=True)
os.makedirs("hasil/perbandingan", exist_ok=True)


# ==========================================
# PROSES SEMUA GAMBAR
# ==========================================

for nama_file in daftar_gambar:

    # Lokasi gambar
    path = os.path.join("gambarijazah", nama_file)

    # Membaca gambar
    citra = cv2.imread(path)

    # Mengecek gambar
    if citra is None:
        print(f"Gambar tidak ditemukan: {nama_file}")
        continue

    # ==========================================
    # 1. GRAYSCALE
    # ==========================================

    grayscale = cv2.cvtColor(
        citra,
        cv2.COLOR_BGR2GRAY
    )

    # ==========================================
    # 2. MEAN FILTER
    # ==========================================

    mean = cv2.blur(
        grayscale,
        (5, 5)
    )

    # ==========================================
    # 3. MEDIAN FILTER
    # ==========================================

    median = cv2.medianBlur(
        grayscale,
        5
    )

    # ==========================================
    # 4. GAUSSIAN FILTER
    # ==========================================

    gaussian = cv2.GaussianBlur(
        grayscale,
        (5, 5),
        0
    )

    # ==========================================
    # 5. SHARPENING
    # ==========================================

    kernel = np.array([
        [0, -1, 0],
        [-1, 5, -1],
        [0, -1, 0]
    ])

    sharpening = cv2.filter2D(
        grayscale,
        -1,
        kernel
    )

    # ==========================================
    # NAMA FILE
    # ==========================================

    nama = os.path.splitext(nama_file)[0]

    # ==========================================
    # MENYIMPAN HASIL
    # ==========================================

    cv2.imwrite(
        f"hasil/grayscale/grayscale_{nama}.jpg",
        grayscale
    )

    cv2.imwrite(
        f"hasil/mean/mean_{nama}.jpg",
        mean
    )

    cv2.imwrite(
        f"hasil/median/median_{nama}.jpg",
        median
    )

    cv2.imwrite(
        f"hasil/gaussian/gaussian_{nama}.jpg",
        gaussian
    )

    cv2.imwrite(
        f"hasil/sharpening/sharpening_{nama}.jpg",
        sharpening
    )

    # ==========================================
    # MENAMPILKAN PERBANDINGAN
    # ==========================================

    plt.figure(figsize=(12, 8))

    # Original
    plt.subplot(2, 3, 1)
    plt.imshow(
        cv2.cvtColor(citra, cv2.COLOR_BGR2RGB)
    )
    plt.title("Original")
    plt.axis("off")

    # Grayscale
    plt.subplot(2, 3, 2)
    plt.imshow(
        grayscale,
        cmap="gray"
    )
    plt.title("Grayscale")
    plt.axis("off")

    # Mean
    plt.subplot(2, 3, 3)
    plt.imshow(
        mean,
        cmap="gray"
    )
    plt.title("Mean Filter")
    plt.axis("off")

    # Median
    plt.subplot(2, 3, 4)
    plt.imshow(
        median,
        cmap="gray"
    )
    plt.title("Median Filter")
    plt.axis("off")

    # Gaussian
    plt.subplot(2, 3, 5)
    plt.imshow(
        gaussian,
        cmap="gray"
    )
    plt.title("Gaussian Filter")
    plt.axis("off")

    # Sharpening
    plt.subplot(2, 3, 6)
    plt.imshow(
        sharpening,
        cmap="gray"
    )
    plt.title("Sharpening")
    plt.axis("off")

    plt.suptitle(
        f"Perbandingan Filtering - {nama}"
    )

    plt.tight_layout()

    # Menyimpan perbandingan
    plt.savefig(
        f"hasil/perbandingan/perbandingan_{nama}.jpg"
    )

    # Menampilkan
    plt.show()

    plt.close()

    print(f"Berhasil: {nama_file}")


print("\nSemua gambar selesai diproses!")