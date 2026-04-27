# Otomata A - Tugas Praktikum

Repositori ini berisi pengerjaan tugas praktikum mata kuliah Otomata A. Implementasi program dibuat menggunakan Python dengan antarmuka grafis Tkinter agar pengguna dapat memasukkan input secara langsung dan melihat hasil analisis dengan mudah.

## Anggota Kelompok

| Nama | NRP |
| --- | --- |
| Muhammad Adi Anugerah Arrahman | 5025241118 |
| Rifat Qurratu Aini Irwandi | 5025241233 |
| Mayandra Suhaira Frisiandi | 5025241240 |

## Isi Proyek

- `Praktikum 1.py`  
	Program lexical analyzer sederhana untuk mengelompokkan token dari program komputer ke dalam beberapa kategori, seperti:
	- reserve words
	- simbol dan tanda baca
	- variabel / identifier
	- kalimat matematika, fungsi, atau bentuk ekspresi lain

- `prak2.py`  
	Program simulasi FSM untuk memeriksa keanggotaan string biner berdasarkan aturan mesin hingga string diterima atau ditolak.

## Deskripsi Tugas

### Tugas Praktikum #1

Membuat program yang dapat membaca input berupa program komputer lain, lalu menghasilkan output berupa token-token yang terbaca dan mengelompokkannya sesuai sifat string tersebut. Antarmuka dibuat agar pengguna dapat dengan mudah memasukkan program yang ingin dicari token-nya.

### Tugas Praktikum #2

Membuat program untuk mengotomasi FSM yang diberikan, yaitu mesin yang menentukan apakah sebuah string merupakan anggota bahasa:

$$
L = \{ x \in (0+1)^* \mid \text{karakter terakhir pada } x \text{ adalah } 1 \text{ dan } x \text{ tidak memiliki substring } 00 \}
$$

Program juga dilengkapi antarmuka agar pengguna dapat memasukkan string biner dan langsung melihat hasil identifikasinya.

## Fitur

- Antarmuka grafis berbasis Tkinter.
- Input string atau program secara langsung dari pengguna.
- Klasifikasi token otomatis pada praktikum 1.
- Pemeriksaan string biner pada FSM praktikum 2.
- Output hasil ditampilkan secara ringkas dan mudah dibaca.

## Cara Menjalankan

1. Pastikan Python sudah terpasang di perangkat.
2. Buka terminal atau Command Prompt pada folder proyek ini.
3. Jalankan salah satu file berikut:

```bash
python "Praktikum 1.py"
```

atau

```bash
python prak2.py
```

## Catatan

- Proyek ini dibuat untuk kebutuhan praktikum Otomata A.
- Jika ingin menambahkan dokumentasi atau screenshot hasil program, bagian README ini bisa diperluas lagi.
