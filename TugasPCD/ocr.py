import cv2
import pytesseract
import os
import pytesseract

# Tambahkan baris ini di bagian atas (sesuaikan path jika instalasi berada di folder lain)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
# Membuat folder hasil OCR
os.makedirs("ocr", exist_ok=True)

print("===================================")
print("        OCR NOMOR IJAZAH")
print("===================================")

# Memproses 9 gambar
for i in range(1, 10):

    # Membaca hasil enhancement
    sebelum = cv2.imread(f"enhancement/sebelum_{i}.jpg")
    brightness = cv2.imread(f"enhancement/brightness_{i}.jpg")
    contrast = cv2.imread(f"enhancement/contrast_{i}.jpg")
    equalization = cv2.imread(
        f"enhancement/equalization_{i}.jpg"
    )

    # Mengecek file
    if sebelum is None:
        print(f"\nIjazah {i}: file tidak ditemukan!")
        continue

    # OCR
    hasil_sebelum = pytesseract.image_to_string(
        sebelum,
        config="--psm 7"
    )

    hasil_brightness = pytesseract.image_to_string(
        brightness,
        config="--psm 7"
    )

    hasil_contrast = pytesseract.image_to_string(
        contrast,
        config="--psm 7"
    )

    hasil_equalization = pytesseract.image_to_string(
        equalization,
        config="--psm 7"
    )

    # Menampilkan hasil
    print(f"\n========== IJAZAH {i} ==========")

    print("Sebelum Enhancement :",
          hasil_sebelum.strip())

    print("Brightness          :",
          hasil_brightness.strip())

    print("Contrast Stretching :",
          hasil_contrast.strip())

    print("Histogram Equalization :",
          hasil_equalization.strip())

    # Menyimpan hasil OCR
    with open(
        f"ocr/hasil_ocr_{i}.txt",
        "w"
    ) as file:

        file.write(
            f"HASIL OCR NOMOR IJAZAH {i}\n"
        )

        file.write(
            "============================\n\n"
        )

        file.write(
            "Sebelum Enhancement : "
            + hasil_sebelum.strip()
            + "\n"
        )

        file.write(
            "Brightness          : "
            + hasil_brightness.strip()
            + "\n"
        )

        file.write(
            "Contrast Stretching : "
            + hasil_contrast.strip()
            + "\n"
        )

        file.write(
            "Histogram Equalization : "
            + hasil_equalization.strip()
            + "\n"
        )

print("\n===================================")
print("          OCR SELESAI")
print("===================================")
print("Hasil OCR tersimpan di folder: ocr")