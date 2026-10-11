import cv2
import os
import matplotlib.pyplot as plt

# Membuat folder hasil jika belum ada
os.makedirs("hasil", exist_ok=True)

for i in range(1, 10):

    nama_file = f"ijazah{i}.jpeg"

    # Membaca citra asli
    ijazah = cv2.imread(nama_file)

    # Cek apakah citra berhasil dibaca
    if ijazah is None:
        print(f"Ijazah {nama_file} tidak ditemukan!")
        continue

    # Mengubah citra menjadi grayscale
    grayscale = cv2.cvtColor(ijazah, cv2.COLOR_BGR2GRAY)

    # ==========================================
    # HISTOGRAM CITRA ASLI BERWARNA
    # ==========================================

    hist_b = cv2.calcHist([ijazah], [0], None, [256], [0, 256])
    hist_g = cv2.calcHist([ijazah], [1], None, [256], [0, 256])
    hist_r = cv2.calcHist([ijazah], [2], None, [256], [0, 256])

    # ==========================================
    # HISTOGRAM GRAYSCALE
    # ==========================================

    hist_gray = cv2.calcHist(
        [grayscale],
        [0],
        None,
        [256],
        [0, 256]
    )

    # ==========================================
    # 2 HISTOGRAM DALAM 1 KOTAK
    # ==========================================

    plt.figure(figsize=(10, 8))

    # Histogram citra asli
    plt.subplot(2, 1, 1)

    plt.plot(hist_b, label="Blue (B)")
    plt.plot(hist_g, label="Green (G)")
    plt.plot(hist_r, label="Red (R)")

    plt.title(f"Histogram Citra Asli - Ijazah {i}")
    plt.xlabel("Intensitas Piksel")
    plt.ylabel("Jumlah Piksel")
    plt.xlim([0, 256])
    plt.legend()
    plt.grid()

    # Histogram grayscale
    plt.subplot(2, 1, 2)

    plt.plot(hist_gray)

    plt.title(f"Histogram Grayscale - Ijazah {i}")
    plt.xlabel("Intensitas Piksel")
    plt.ylabel("Jumlah Piksel")
    plt.xlim([0, 256])
    plt.grid()

    # Merapikan tampilan
    plt.tight_layout()

    # Menyimpan hasil
    nama_hasil = f"hasil/2_histogram_ijazah{i}.jpg"
    plt.savefig(nama_hasil)

    # Menampilkan
    plt.show()

    plt.close()

    print(f"Berhasil: {nama_hasil}")