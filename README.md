# MariaDB Transaction & Replication Lab Workspace

Complete local workspace for MariaDB/MySQL InnoDB transaction routines (`START TRANSACTION`, `COMMIT`, `ROLLBACK`, `SAVEPOINT`, `AFTER INSERT` triggers) and asynchronous Master-Slave replication (`Windows Host 192.168.56.1` -> `Ubuntu Guest VM 192.168.56.101`).

## Panduan Cepat untuk Pengguna Awam di Windows

### 1. Download Seluruh Paket (Tanpa Perlu Git)
Klik tautan berikut di browser Windows Anda:
👉 **[Download ZIP Paket Lengkap](https://github.com/mirsydfchrynto/mariadb-replication-lab/archive/refs/heads/main.zip)**

Setelah terunduh, **Klik Kanan** pada file `.zip` -> pilih **Extract All...** -> buka foldernya.

### 2. Dua Cara Penggunaan Video & Praktikum
- **Cara Instan (Langsung Pakai Video Jadi)**:
  Buka folder `video/VIDEO_PRAKTIKUM_SIAP_PAKAI.mp4` (durasi ~8.5 menit, 24fps, dilengkapi pergerakan kursor Windows 11 natural mengikuti kurva Bezier pada 39 tahapan dari yEd, XAMPP Windows, phpMyAdmin `transaksi1`–`transaksi5`, `Trigger`, `my.ini`, VirtualBox Host-Only, CMD `ipconfig` & `ping`, hingga Ubuntu XAMPP & replikasi `Yes/Yes`).
- **Cara Rekam Sendiri di Laptop Windows**:
  Klik kanan file `START-HERE.bat` -> pilih **Run as administrator**:
  - Pilih **`[0]`** untuk otomatis mengunduh & menginstal **yEd Graph Editor**, **XAMPP v8.2.12**, **Oracle VirtualBox**, **ISO Ubuntu**, dan otomatis membuat VM `Linux-Ubuntu-BasisData`.
  - Pilih **`[1]`** untuk persiapan rekam manual dari dasar (membuka `PANDUAN-AWAM-STEP-BY-STEP.html` dan Notepad `CONTEKAN-COPAS-SAAT-REKAMAN.txt`).
  - Pilih **`[2]`** untuk menjalankan **Auto-Human Tempo Pelan** (`auto_human_windows.py`) yang menggerakkan kursor mouse asli Windows (`Win32 SetCursorPos`) secara halus dan mengetikkan kode per huruf di browser Chrome/Edge.
  - Pilih **`[3]`** untuk instalasi instan 5 detik.

### 3. Laporan Word & PDF Siap Kumpul
Buka folder `docs/`:
- `TUGAS_3_SUBHAN YOGA MAULANA_044876223.docx` (24 halaman, 39 gambar bukti lengkap).
- `TUGAS_3_SUBHAN YOGA MAULANA_044876223.pdf` (24 halaman).
