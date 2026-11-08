# Panduan Upload & Push ke Repositori GitHub Pribadi Mahasiswa

Petunjuk bagi **Subhan Yoga Maulana (NIM: 044876223)** untuk mengunggah berkas Tugas 3 Basis Data ke akun GitHub pribadi.

---

## Cara 1: Upload Langsung via Web Browser GitHub (Paling Mudah)

1. Buka browser dan login ke akun GitHub di: [https://github.com](https://github.com)
2. Buat repositori baru di: [https://github.com/new](https://github.com/new)
   - **Repository name**: `praktikum-basis-data-tugas3` (atau `tugas3-basis-data-msim4206`)
   - **Visibility**: `Public`
   - Centang **Add a README file**
   - Klik tombol **Create repository**
3. Masuk ke halaman repositori yang baru dibuat:
   - Klik menu **Add file** di bagian kanan atas, lalu pilih **Upload files**
   - Tarik (*drag and drop*) berkas-berkas tugas ini dari komputer ke browser:
     - Laporan praktikum Word (`.docx`) dan PDF (`.pdf`)
     - File diagram ERD yEd (`skema_rumah_sakit.graphml`)
     - Skrip SQL (`00_persiapan_tugas2.sql` dan `01_full_transaksi_dan_trigger.sql`)
     - Naskah bacaan narasi
   - Beri pesan commit singkat, contoh: `Upload berkas praktikum tugas 3 basis data`
   - Klik tombol hijau **Commit changes**
4. Selesai. Link repositori Anda adalah:
   `https://github.com/USERNAME_ANDA/praktikum-basis-data-tugas3`

---

## Cara 2: Push Menggunakan Git Command Line di Komputer

Jika di komputer Anda sudah terpasang Git:

1. Buat repositori kosong di [https://github.com/new](https://github.com/new) tanpa mencentang README.
2. Buka folder berkas tugas ini di File Explorer.
3. Klik kanan pada area kosong dan pilih **Open in Terminal** atau **Open Git Bash here**.
4. Jalankan perintah berikut:

```bash
git init -b main
git add .
git commit -m "feat: pengumpulan praktikum tugas 3 basis data msim4206"
git remote add origin https://github.com/USERNAME_ANDA/praktikum-basis-data-tugas3.git
git push -u origin main
```

*(Ganti `USERNAME_ANDA` dengan username GitHub Anda).*

---

## Pendaftaran Akun ke Organisasi GitHub Kelas

Sesuai tautan pengumuman tutor:
Formulir pendaftaran akun GitHub mahasiswa ke organisasi GitHub mata kuliah:
👉 [https://docs.google.com/forms/d/1NjkNOb2e0_ptEWXSWq10xs7nTeNvjDCBx4eSybNnor0](https://docs.google.com/forms/d/1NjkNOb2e0_ptEWXSWq10xs7nTeNvjDCBx4eSybNnor0)
