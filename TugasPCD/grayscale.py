import cv2
import os
import matplotlib.pyplot as plt

# Membuat folder hasil jika belum ada
os.makedirs("hasil", exist_ok=True)

for i in range(1, 10):

    nama_file = f"ijazah{i}.jpeg"

    # Membaca ijazah
    ijazah = cv2.imread(nama_file)

    # Cek apakah ijazah berhasil dibaca
    if ijazah is None:
        print(f"Ijazah {nama_file} tidak ditemukan!")
        continue

    # Mengubah ijazah menjadi grayscale
    grayscale = cv2.cvtColor(ijazah, cv2.COLOR_BGR2GRAY)

    # Menyimpan hasil grayscale
    nama_hasil = f"hasil/grayscale_ijazah{i}.jpg"
    cv2.imwrite(nama_hasil, grayscale)

    # Menampilkan ijazah grayscale
    plt.figure(figsize=(6, 4))
    plt.imshow(grayscale, cmap="gray")
    plt.title(f"Grayscale - Ijazah {i}")
    plt.axis("off")
    plt.show()

    print(f"Berhasil: {nama_hasil}")
