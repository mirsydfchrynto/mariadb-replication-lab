# Naskah Bacaan Video Dokumenter Praktikum Tugas 3 Basis Data (MSIM4206)

- **Nama**: Subhan Yoga Maulana
- **NIM**: 044876223
- **Program Studi**: Sistem Informasi
- **Durasi Total Video**: `13:34` (13.5 menit, 25fps H.264 Tanpa Suara)
- **File Video**: `VIDEO_DOKUMENTER_PRAKTIKUM_TUGAS3_SUBHAN_YOGA_MAULANA_044876223.mp4`

---

### 1. [00:00] Perkenalan dan Desain Skema ERD di Aplikasi yEd Graph Editor 3.25.1
> "Assalamualaikum warahmatullahi wabarakatuh. Perkenalkan nama saya Subhan Yoga Maulana, NIM 044876223, dari Program Studi Sistem Informasi Universitas Terbuka. Di video ini saya mempraktikkan Tugas 3 Mata Kuliah Basis Data secara bertahap dari awal. Pertama, ini adalah rancangan skema relasi delapan tabel pada database rumah_sakit yang dibuat di aplikasi yEd Graph Editor, yaitu tabel pasien, transaksi_obat, obat, daftar, pasien_dokter, dokter, administrator, dan dokter_admin."

### 2. [00:23] Menyalakan Service Apache dan MySQL di XAMPP Control Panel Windows
> "Sekarang kita buka XAMPP Control Panel v3.3.0 di Windows. Kita klik tombol Start pada modul Apache dan klik Start pada modul MySQL sampai keduanya berwarna hijau aktif pada port 80 dan 3306. Setelah aktif, kita klik tombol Admin pada baris MySQL untuk membuka phpMyAdmin di browser."

### 3. [00:47] Membuka Database rumah_sakit di phpMyAdmin
> "Setelah browser terbuka di localhost/phpmyadmin, kita pilih database rumah_sakit di panel sebelah kiri."

### 4. [00:52] Memeriksa Struktur Database rumah_sakit (Hasil Tugas 2)
> "Di halaman struktur database rumah_sakit, terlihat enam tabel awal hasil Tugas 2 sudah menggunakan storage engine InnoDB."

### 5. [00:57] Memeriksa Data Awal Tabel pasien
> "Kita buka tabel pasien. Di sini sudah ada 5 baris data pasien awal dengan ID 1 sampai 5."

### 6. [01:10] Membuat Routine transaksi1 (START TRANSACTION Tanpa COMMIT)
> "Untuk memulai Praktikum Transaksi, kita buka menu Routines lalu klik Create new routine. Kita beri nama transaksi1, parameternya kita hapus dengan klik Drop, lalu pada Definition kita masukkan perintah START TRANSACTION dan INSERT data pasien ID 6 bernama Hanif tanpa perintah COMMIT, lalu kita klik Go dan klik Execute."

### 7. [01:54] Verifikasi Tabel pasien Setelah transaksi1
> "Ketika kita kembali ke menu Browse tabel pasien, jumlah baris tetap 5. Data Hanif belum tersimpan permanen karena transaksinya belum di-COMMIT."

### 8. [02:12] Membuat Routine transaksi2 (START TRANSACTION Dengan COMMIT)
> "Sekarang kita buat routine kedua bernama transaksi2. Parameternya kita drop, lalu kita masukkan perintah yang sama seperti tadi tapi ditambahkan perintah COMMIT setelah INSERT, lalu klik Go dan klik Execute."

### 9. [02:58] Verifikasi Tabel pasien Setelah transaksi2
> "Saat kita cek lagi tabel pasien, data pasien ID 6 atas nama Hanif sekarang sudah tersimpan secara permanen di database."

### 10. [03:16] Membuat Routine transaksi3 (Perintah ROLLBACK)
> "Lanjut ke routine transaksi3 untuk menguji perintah ROLLBACK. Pada Definition kita tulis UPDATE pasien SET nama_pasien = 'Septin' WHERE id_pasien = 3, lalu diikuti perintah ROLLBACK dan COMMIT, kemudian klik Go dan Execute."

### 11. [03:58] Verifikasi Tabel pasien Setelah transaksi3
> "Pada tabel pasien terlihat nama pasien ID 3 tetap Budi Raharjo dan batal berubah menjadi Septin karena dibatalkan oleh perintah ROLLBACK."

### 12. [04:16] Membuat Routine transaksi4 (Modifikasi ROLLBACK dan COMMIT)
> "Sesuai skenario di modul praktikum, kita buat routine transaksi4. Kita masukkan INSERT pasien baru ID 7 bernama Rudi yang dibatalkan dengan ROLLBACK, lalu dilanjutkan UPDATE nama pasien ID 3 menjadi Septin yang disahkan dengan COMMIT."

### 13. [05:07] Verifikasi Tabel pasien Setelah transaksi4
> "Di tabel pasien terlihat penambahan pasien ID 7 batal masuk karena terkena ROLLBACK, sedangkan perubahan nama ID 3 menjadi Septin berhasil disimpan permanen oleh COMMIT."

### 14. [05:26] Membuat Routine transaksi5 (SAVEPOINT point1 dan ROLLBACK TO point1)
> "Berikutnya kita buat routine transaksi5 untuk mempraktikkan SAVEPOINT. Kita masukkan pasien ID 8 bernama Dudung, lalu membuat SAVEPOINT point1. Setelah itu kita masukkan ID 9 bernama Maman, tapi kita batalkan ke titik point1 dengan perintah ROLLBACK TO point1, lalu menambahkan ID 10 bernama Ujang dan diakhiri COMMIT."

### 15. [06:36] Verifikasi Tabel pasien Setelah transaksi5
> "Hasilnya pada tabel pasien: ID 8 Dudung dan ID 10 Ujang tersimpan permanen, sedangkan ID 9 Maman batal masuk karena kembali ke titik point1."

### 16. [06:50] Membuat Tabel obat, transaksi_obat, Relasi Foreign Key, dan Stok Awal
> "Tahap berikutnya adalah pembuatan Trigger. Kita buka tab SQL pada database rumah_sakit untuk membuat tabel obat dan tabel transaksi_obat dengan relasi Foreign Key CASCADE serta mengisi data stok awal obat, lalu klik Go."

### 17. [08:11] Memeriksa Stok Awal pada Tabel obat
> "Kita periksa tabel obat. Stok awal Paracetamol adalah 100, Amoxicillin 50, dan Betadine 100."

### 18. [08:19] Memeriksa Relasi Foreign Key CASCADE pada Tabel transaksi_obat
> "Di menu Relation view tabel transaksi_obat, terlihat Foreign Key sudah terhubung ke id_pasien dan id_obat dengan opsi ON DELETE CASCADE dan ON UPDATE CASCADE."

### 19. [08:28] Membuat Trigger tg_stok_obat (AFTER INSERT)
> "Pada tabel transaksi_obat kita buka menu Triggers lalu klik Create new trigger. Kita beri nama tg_stok_obat dengan waktu AFTER dan event INSERT, lalu kita ketik UPDATE obat SET stok = stok - NEW.jumlah WHERE id_obat = NEW.id_obat, lalu klik Go."

### 20. [09:03] Menguji Trigger tg_stok_obat dengan Input Pembelian 15 Paracetamol
> "Kita uji trigger ini lewat menu Insert pada tabel transaksi_obat. Kita masukkan id_transaksi 1, id_pasien 6 yaitu Hanif, id_obat 1 yaitu Paracetamol, jumlah 15, dan total harga 75000, lalu klik Go."

### 21. [09:35] Verifikasi Stok Paracetamol Berkurang Otomatis Menjadi 85
> "Saat kita buka lagi tabel obat, stok Paracetamol yang awalnya 100 otomatis berkurang menjadi 85 karena pemotongan stok oleh Trigger."

### 22. [09:45] Konfigurasi File my.ini pada XAMPP Windows (Master)
> "Sekarang kita masuk ke Praktikum Basis Data Terdistribusi Replikasi Master-Slave. Di Windows sebagai Master, kita buka file my.ini lewat tombol Config MySQL di XAMPP, lalu di bawah bagian [mysqld] kita tambahkan log-bin=mysql-bin, server-id=1, dan binlog-do-db=rumah_sakit, lalu simpan file dan restart MySQL di XAMPP."

### 23. [10:06] Pengaturan Network Host-Only Adapter dan Menyalakan VM Ubuntu
> "Pada Oracle VM VirtualBox Manager, kita klik Settings pada mesin virtual Ubuntu-BasisData, pilih menu Network, pastikan Adapter 1 diatur ke Host-only Adapter dengan nama VirtualBox Host-Only Ethernet Adapter, klik OK, lalu klik Start VM."

### 24. [10:23] Pemeriksaan IP (ipconfig dan ip a) serta Uji Ping Dua Arah
> "Kita cek koneksi jaringan antar-OS. Di Command Prompt Windows kita ketik ipconfig, terlihat IP Windows adalah 192.168.56.1 dan hasil ping ke Ubuntu 192.168.56.101 berhasil 0% loss. Di Terminal Ubuntu kita ketik ip a, terlihat IP Ubuntu adalah 192.168.56.101 dan ping ke Windows 192.168.56.1 juga berhasil terhubung."

### 25. [10:48] Menyalakan XAMPP Linux dan Mengedit my.cnf di Ubuntu
> "Di dalam Desktop Ubuntu VirtualBox, kita jalankan XAMPP Linux 8.2.12. Pada Terminal Ubuntu kita buka file /opt/lampp/etc/my.cnf dengan nano, kita beri tanda pagar pada #server-id = 1 lalu kita tambahkan server-id = 2 dan replicate-do-db = rumah_sakit, kemudian simpan dan restart MySQL di XAMPP Ubuntu."

### 26. [11:11] Membuat User Replikasi di Server Master Windows
> "Kembali ke phpMyAdmin Master di Windows, kita buka tab User accounts lalu klik Add user account. Kita buat user replikasi bernama subhan dengan host persen, password 1234, dan mencentang hak akses Replication client serta Replication slave, lalu klik Go."

### 27. [11:36] Memeriksa Status Primary Replication dan Posisi Log Master
> "Kita buka tab Replication di Master lalu klik Show primary status. Tercatat file log aktif adalah mysql-bin.000001 pada posisi 328."

### 28. [11:50] Menghubungkan Slave Ubuntu ke Master Windows (CHANGE MASTER TO)
> "Pada phpMyAdmin Slave di Ubuntu, setelah database rumah_sakit diimpor, kita buka tab SQL lalu jalankan perintah STOP SLAVE, CHANGE MASTER TO MASTER_HOST='192.168.56.1', MASTER_USER='subhan', MASTER_PASSWORD='1234', MASTER_LOG_FILE='mysql-bin.000001', MASTER_LOG_POS=328, dan START SLAVE, lalu klik Go."

### 29. [12:21] Verifikasi Status Slave_IO_Running: Yes dan Slave_SQL_Running: Yes
> "Kita buka tab Replication di Slave Ubuntu lalu klik See replica status table. Terlihat Master_Host terhubung ke 192.168.56.1, serta parameter Slave_IO_Running bernilai Yes dan Slave_SQL_Running bernilai Yes."

### 30. [12:38] Uji Sinkronisasi Replikasi: Input Pembelian 25 Betadine di Master
> "Untuk membuktikan sinkronisasi data berjalan secara langsung, kita input transaksi kedua di Master Windows pada tabel transaksi_obat, yaitu pembelian 25 Betadine oleh pasien ID 8 atas nama Dudung, lalu klik Go. Di Master, stok Betadine berkurang dari 100 menjadi 75."

### 31. [13:18] Pembuktian di Slave Ubuntu: Transaksi dan Stok Otomatis Tereplikasi
> "Sekarang kita beralih ke phpMyAdmin Slave di Ubuntu. Saat tabel transaksi_obat di-refresh, transaksi kedua otomatis masuk. Dan saat kita buka tabel obat di Slave Ubuntu, stok Betadine juga otomatis berkurang menjadi 75 tanpa kita menginput apa pun di Ubuntu. Praktikum Tugas 3 Basis Data telah selesai dilaksanakan dengan baik. Terima kasih, wassalamualaikum warahmatullahi wabarakatuh."
