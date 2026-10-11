import cv2
import numpy as np
import matplotlib.pyplot as plt
import os

os.makedirs("gambar ijazah/enhancement", exist_ok=True)
os.makedirs("gambar ijazah/grafik_histogram", exist_ok=True)

# Membaca gambar nomor ijazah 1
img = cv2.imread(
    "gambar ijazah/01_HighQuality_Enhanced.jpg"
)

# Cek gambar
if img is None:
    print("Gambar tidak ditemukan!")
    exit()

# Grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# 1. Brightness Adjustment
brightness = cv2.convertScaleAbs(
    gray, alpha=1, beta=20
)

# 2. Contrast Stretching
minimum = gray.min()
maksimum = gray.max()

if maksimum != minimum:
    contrast = (
        (gray - minimum) * 255 /
        (maksimum - minimum)
    ).astype(np.uint8)
else:
    contrast = gray.copy()

# 3. Histogram Equalization
equalization = cv2.equalizeHist(gray)


# =========================
# TAMPILKAN CITRA
# =========================

plt.figure(figsize=(12, 8))

plt.subplot(2, 2, 1)
plt.imshow(gray, cmap="gray")
plt.title("Sebelum Enhancement")
plt.axis("off")

plt.subplot(2, 2, 2)
plt.imshow(brightness, cmap="gray")
plt.title("Brightness Adjustment")
plt.axis("off")

plt.subplot(2, 2, 3)
plt.imshow(contrast, cmap="gray")
plt.title("Contrast Stretching")
plt.axis("off")

plt.subplot(2, 2, 4)
plt.imshow(equalization, cmap="gray")
plt.title("Histogram Equalization")
plt.axis("off")

plt.suptitle("Perbandingan Enhancement - Ijazah 1")
plt.tight_layout()

plt.savefig(
    "gambar ijazah/enhancement/perbandingan_ijazah1.jpg",
    dpi=300
)

plt.show()
plt.close()


# =========================
# TAMPILKAN HISTOGRAM
# =========================

plt.figure(figsize=(12, 8))

plt.subplot(2, 2, 1)
plt.hist(gray.ravel(), 256, [0, 256])
plt.title("Histogram Sebelum")

plt.subplot(2, 2, 2)
plt.hist(brightness.ravel(), 256, [0, 256])
plt.title("Histogram Brightness")

plt.subplot(2, 2, 3)
plt.hist(contrast.ravel(), 256, [0, 256])
plt.title("Histogram Contrast Stretching")

plt.subplot(2, 2, 4)
plt.hist(equalization.ravel(), 256, [0, 256])
plt.title("Histogram Equalization")

plt.suptitle("Perbandingan Histogram - Ijazah 1")
plt.tight_layout()

plt.savefig(
    "gambar ijazah/grafik_histogram/histogram_ijazah1.jpg",
    dpi=300
)

plt.show()
plt.close()


# =========================
# SIMPAN HASIL ENHANCEMENT
# =========================

cv2.imwrite(
    "gambar ijazah/enhancement/brightness_ijazah1.jpg",
    brightness
)

cv2.imwrite(
    "gambar ijazah/enhancement/contrast_ijazah1.jpg",
    contrast
)

cv2.imwrite(
    "gambar ijazah/enhancement/equalization_ijazah1.jpg",
    equalization
)

print("Ijazah 1 selesai diproses.")