from Pembagian import bagi
from Penambahan import tambah
from Pengurangan import kurang
from Perkalian import kali

print("======= HASIL MODUL =======")

pertama = int(input("Masukkan angka pertama : "))
kedua = int(input("Masukkan angka kedua : "))

print("======= HASIL PERHITUNGAN =======")
print("Hasil pembagian   : ", bagi(pertama,kedua))
print("Hasil penambahan  : ", tambah(pertama,kedua))
print("Hasil pengurangan : ", kurang(pertama,kedua))
print("Hasil perkalian   : ", kali(pertama,kedua))

