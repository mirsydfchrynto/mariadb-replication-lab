# Naskah Bacaan Video Dokumenter Praktikum Tugas 3 Basis Data (MSIM4206)
- **Nama**: Subhan Yoga Maulana
- **NIM**: 044876223
- **Program Studi**: Sistem Informasi
- **Durasi Total Video**: `13:34` (13.6 menit, 25fps H.264 Tanpa Suara)
- **File Video**: `VIDEO_PRAKTIKUM_MURNI_TANPA_VO_SUBHAN_044876223.mp4` (`video/VIDEO_PRAKTIKUM_SIAP_PAKAI.mp4`)

---

### 1. [00:00] Perkenalan & Desain Skema ERD di Aplikasi yEd Graph Editor 3.25.1
> "Assalamualaikum warahmatullahi wabarakatuh. Perkenalkan nama saya Subhan Yoga Maulana, dengan NIM 044876223, dari Program Studi Sistem Informasi Universitas Terbuka. Pada video ini saya akan mempraktikkan Tugas 3 Mata Kuliah Basis Data secara bertahap dari dasar. Pertama kita melihat rancangan skema relasi 8 tabel pada database rumah_sakit yang dibuat di aplikasi yEd Graph Editor, yaitu tabel pasien, transaksi_obat, obat, daftar, pasien_dokter, dokter, administrator, dan dokter_admin."

### 2. [00:23] Menyalakan Service Apache & MySQL pada XAMPP Control Panel Windows
> "Selanjutnya kita membuka XAMPP Control Panel v3.3.0 di Windows, lalu kita klik tombol Start pada modul Apache dan klik tombol Start pada modul MySQL hingga keduanya berwarna hijau Running pada port 80 dan 3306, kemudian kita klik tombol Admin pada MySQL untuk masuk ke phpMyAdmin."

### 3. [00:47] Elemen 1: Perkenalan & Membuka phpMyAdmin
> "Assalamualaikum warahmatullahi wabarakatuh. Perkenalkan nama saya Subhan Yoga Maulana, dengan NIM 044876223, dari Program Studi Sistem Informasi Universitas Terbuka. Pada video ini saya akan mempraktikkan Tugas 3 Mata Kuliah Basis Data, yaitu Praktikum Transaksi dan Praktikum Basis Data Terdistribusi."

### 4. [00:52] Memeriksa Struktur Database rumah_sakit (Hasil Tugas 2)
> "Pertama kita membuka database rumah_sakit yang melanjutkan tabel dari Tugas 2. Terlihat enam tabel awal sudah menggunakan storage engine InnoDB."

### 5. [00:57] Memeriksa Data Awal Tabel pasien
> "Kita buka tabel pasien. Saat ini terdapat 5 data pasien awal dengan ID pasien 1 sampai 5."

### 6. [01:10] Membuat Routine transaksi1 (START TRANSACTION Tanpa COMMIT)
> "Selanjutnya kita masuk ke menu Routines lalu klik Create new routine. Kita buat routine bernama transaksi1, parameternya kita drop, lalu kita ketik START TRANSACTION dan INSERT pasien ID 6 bernama Hanif tanpa perintah COMMIT, lalu klik Go dan klik Execute."

### 7. [01:54] Verifikasi Tabel pasien Setelah transaksi1
> "Saat kita cek tabel pasien di menu Browse, terlihat data ID 6 atas nama Hanif belum tersimpan permanen di tabel karena belum dilakukan perintah COMMIT."

### 8. [02:12] Membuat Routine transaksi2 (START TRANSACTION Dengan COMMIT)
> "Berikutnya kita buat routine kedua bernama transaksi2. Kita drop parameternya, lalu kita ketik perintah yang sama namun kita tambahkan perintah COMMIT setelah INSERT, kemudian klik Go dan klik Execute."

### 9. [02:58] Verifikasi Tabel pasien Setelah transaksi2
> "Ketika kita cek kembali tabel pasien, kini data pasien ID 6 atas nama Hanif sudah tersimpan secara permanen di dalam database."

### 10. [03:16] Membuat Routine transaksi3 (Perintah ROLLBACK)
> "Selanjutnya kita buat routine transaksi3 untuk menguji perintah ROLLBACK. Kita ketik UPDATE pasien SET nama_pasien = 'Septin' WHERE id_pasien = 3, namun diikuti perintah ROLLBACK, lalu klik Go dan Execute."

### 11. [03:58] Verifikasi Tabel pasien Setelah transaksi3
> "Pada tabel pasien terlihat bahwa perubahan nama pada ID 3 dibatalkan oleh ROLLBACK sehingga nama pasien tetap Budi Raharjo."

### 12. [04:16] Membuat Routine transaksi4 (Modifikasi ROLLBACK & COMMIT)
> "Berikutnya sesuai modul praktikum kita buat routine transaksi4. Kita ketik INSERT pasien baru ID 7 bernama Rudi yang dibatalkan dengan ROLLBACK, lalu dilanjutkan UPDATE nama pasien ID 3 menjadi Septin yang disahkan dengan COMMIT."

### 13. [05:07] Verifikasi Tabel pasien Setelah transaksi4
> "Pada tabel pasien terlihat penambahan pasien ID 7 batal masuk karena ROLLBACK, sedangkan perubahan nama pasien ID 3 menjadi Septin berhasil disimpan permanen oleh COMMIT."

### 14. [05:26] Membuat Routine transaksi5 (SAVEPOINT point1 & ROLLBACK TO point1)
> "Selanjutnya kita buat routine transaksi5 untuk mempraktikkan SAVEPOINT. Kita menyisipkan pasien ID 8 bernama Dudung, lalu membuat SAVEPOINT point1. Setelah itu kita menyisipkan ID 9 bernama Maman namun kita batalkan ke titik point1 dengan ROLLBACK TO point1, dilanjutkan menyisipkan ID 10 bernama Ujang dan diakhiri COMMIT."

### 15. [06:36] Verifikasi Tabel pasien Setelah transaksi5
> "Pada tabel pasien terlihat ID 8 atas nama Dudung dan ID 10 atas nama Ujang berhasil tersimpan permanen, sedangkan ID 9 atas nama Maman batal masuk karena terkena ROLLBACK TO point1."

### 16. [06:50] Membuat Tabel obat, Tabel transaksi_obat, Relasi Foreign Key, dan Stok Awal
> "Tahap berikutnya adalah pembuatan tabel obat dan tabel transaksi_obat beserta relasi Foreign Key CASCADE dan pengisian tiga data obat awal melalui tab SQL."

### 17. [08:11] Memeriksa Stok Awal pada Tabel obat
> "Kita buka tabel obat. Terlihat stok awal Paracetamol adalah 100, Amoxicillin 50, dan Betadine 100."

### 18. [08:19] Memeriksa Relasi Foreign Key CASCADE pada Tabel transaksi_obat
> "Pada tampilan Relation view tabel transaksi_obat, terlihat relasi Foreign Key telah terhubung ke id_pasien pada tabel pasien dan id_obat pada tabel obat dengan aturan ON DELETE CASCADE dan ON UPDATE CASCADE."

### 19. [08:28] Membuat Trigger tg_stok_obat (AFTER INSERT)
> "Selanjutnya kita buka menu Triggers lalu klik Create new trigger. Kita beri nama tg_stok_obat dengan waktu AFTER dan event INSERT, lalu kita ketik UPDATE obat SET stok = stok - NEW.jumlah WHERE id_obat = NEW.id_obat."

### 20. [09:03] Menguji Trigger tg_stok_obat dengan Input Pembelian 15 Paracetamol
> "Sekarang kita uji trigger tersebut dengan membuka menu Insert pada tabel transaksi_obat. Kita masukkan id_transaksi 1, id_pasien 6 yaitu Hanif, id_obat 1 yaitu Paracetamol, jumlah 15, dan total_harga 75000, lalu klik Go."

### 21. [09:35] Verifikasi Stok Paracetamol Berkurang Otomatis Menjadi 85
> "Ketika kita periksa kembali tabel obat, terlihat stok Paracetamol yang semula 100 kini otomatis berkurang menjadi 85."

### 22. [09:45] Konfigurasi File my.ini pada XAMPP Windows (Master)
> "Selanjutnya untuk menyiapkan Replikasi Master-Slave, kita buka file my.ini pada XAMPP Windows melalui Notepad, lalu di bawah bagian [mysqld] kita ketikkan log-bin=mysql-bin, server-id=1, dan binlog-do-db=rumah_sakit, serta memberi tanda pagar pada server-id=1 bawaan, lalu kita simpan dan merestart MySQL."

### 23. [10:06] Pengaturan Network Host-Only Adapter & Menyalakan VM Ubuntu di VirtualBox
> "Berikutnya kita buka Oracle VM VirtualBox Manager, klik Settings pada mesin virtual Ubuntu-BasisData, pilih menu Network, lalu ubah Attached to menjadi Host-only Adapter dengan nama VirtualBox Host-Only Ethernet Adapter, klik OK, lalu kita klik Start VM."

### 24. [10:23] Pemeriksaan IP (ipconfig & ip a) dan Uji Ping Dua Arah Windows <-> Ubuntu
> "Setelah itu kita buka Command Prompt di Windows dan ketik ipconfig untuk melihat IP Host yaitu 192.168.56.1, lalu kita uji ping ke IP Ubuntu 192.168.56.101 dan hasilnya Reply 0% loss. Sebaliknya di Terminal Ubuntu kita ketik ip -4 addr show enp0s3 yang menampilkan IP 192.168.56.101, lalu kita ping ke 192.168.56.1 dan berhasil terhubung."

### 25. [10:48] Menyalakan XAMPP Linux 8.2.12 & Mengedit /opt/lampp/etc/my.cnf di Ubuntu
> "Di dalam Desktop Ubuntu VirtualBox, kita nyalakan MySQL Database dan Apache Web Server pada XAMPP 8.2.12, lalu pada Terminal Ubuntu kita edit file /opt/lampp/etc/my.cnf menggunakan nano dengan memberi tanda pagar pada #server-id = 1 serta menambahkan server-id = 2 dan replicate-do-db = rumah_sakit, kemudian kita klik Restart MySQL."

### 26. [11:11] Praktikum Replikasi: Membuat User Replikasi pada Server Master
> "Pada phpMyAdmin Master kita buka menu User accounts lalu klik Add user account untuk membuat akun replikasi bernama subhan dengan host persen dan hak akses Replication client serta Replication slave."

### 27. [11:36] Memeriksa Status Primary Replication & Posisi Binary Log Master
> "Kita buka menu Replication di Master lalu klik Show primary status untuk mencatat nama File mysql-bin.000001 dan angka Position 328."

### 28. [11:50] Menghubungkan Server Slave Ubuntu ke Server Master Windows (CHANGE MASTER TO)
> "Selanjutnya pada phpMyAdmin Server Slave di Ubuntu kita buka tab SQL lalu mengetikkan perintah STOP SLAVE, CHANGE MASTER TO MASTER_HOST='192.168.56.1', MASTER_USER='subhan', MASTER_PASSWORD='1234', MASTER_LOG_FILE='mysql-bin.000001', MASTER_LOG_POS=328, dan START SLAVE, lalu klik Go."

### 29. [12:21] Verifikasi Status Slave_IO_Running: Yes & Slave_SQL_Running: Yes di Ubuntu
> "Kita klik See replica status table pada menu Replication di Slave Ubuntu. Terlihat Master_Host terhubung ke 192.168.56.1, serta Slave_IO_Running bernilai Yes dan Slave_SQL_Running bernilai Yes."

### 30. [12:38] Uji Sinkronisasi Replikasi: Input Pembelian 25 Betadine di Server Master
> "Untuk membuktikan replikasi berjalan secara real-time, kita kembali ke Server Master lalu menginput transaksi kedua pada tabel transaksi_obat, yaitu pembelian Betadine sebanyak 25 buah oleh pasien ID 8 atas nama Dudung, kemudian klik Go."

### 31. [13:18] Pembuktian di Server Slave Ubuntu: Transaksi ke-2 & Stok Betadine Otomatis Tereplikasi
> "Sekarang kita beralih ke phpMyAdmin pada Server Slave di Ubuntu. Pada tabel transaksi_obat terlihat transaksi kedua pembelian 25 Betadine otomatis muncul. Dan ketika kita klik tabel obat di Slave Ubuntu, stok Betadine otomatis berkurang dari 100 menjadi 75. Sekian praktikum Tugas 3 Basis Data dari saya, terima kasih, wassalamualaikum warahmatullahi wabarakatuh."
