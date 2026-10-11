def input_array(nama, jumlah_matriks, jumlah_baris, jumlah_kolom):

    print("\n===================================")
    print(f"        INPUT ARRAY {nama}")
    print("===================================")

    array = []

    total_elemen = jumlah_baris * jumlah_kolom

    for matriks_ke in range(jumlah_matriks):

        while True:
            print(f"\nMatriks {matriks_ke + 1}")
            print(f"Masukkan {total_elemen} angka:")

            data = input(">> ").split()

            if len(data) != total_elemen:
                print(f"⚠️ Harus memasukkan tepat {total_elemen} angka.")
                continue

            try:
                data = [int(x) for x in data]
                break
            except ValueError:
                print("⚠️ Semua input harus berupa angka.")

        matriks = []

        posisi = 0

        for i in range(jumlah_baris):
            baris = []

            for j in range(jumlah_kolom):
                baris.append(data[posisi])
                posisi += 1

            matriks.append(baris)

        array.append(matriks)

    return array


def perkalian_array_3d(A, B):

    hasil = []

    for k in range(len(A)):

        matriks = []

        for i in range(len(A[k])):

            baris = []

            for j in range(len(B[k][0])):

                total = 0

                for x in range(len(A[k][0])):
                    total += A[k][i][x] * B[k][x][j]

                baris.append(total)

            matriks.append(baris)

        hasil.append(matriks)

    return hasil


def tampilkan(nama, array):

    print("\n===================================")
    print(f"          {nama}")
    print("===================================")

    for k, matriks in enumerate(array):

        print(f"\nMatriks {k + 1}:")

        for baris in matriks:
            print("[", end=" ")

            for nilai in baris:
                print(nilai, end=" ")

            print("]")


# ===================================
# PROGRAM UTAMA
# ===================================

print("===================================")
print("     PERKALIAN ARRAY MATRIKS 3D")
print("===================================")

jumlah_matriks = 2
jumlah_baris = 2
jumlah_kolom = 2


# INPUT A
A = input_array(
    "A",
    jumlah_matriks,
    jumlah_baris,
    jumlah_kolom
)


# INPUT B
B = input_array(
    "B",
    jumlah_matriks,
    jumlah_baris,
    jumlah_kolom
)


# TAMPILKAN A DAN B
tampilkan("ARRAY A", A)
tampilkan("ARRAY B", B)


# PERKALIAN
C = perkalian_array_3d(A, B)


# TAMPILKAN HASIL
tampilkan("HASIL PERKALIAN A x B", C)


print("\n===================================")
print("          PROGRAM SELESAI")
print("===================================")