-- ============================================================================
-- 00_PERSIAPAN_DATABASE_TUGAS2_RUMAH_SAKIT.sql
-- Jalankan file ini di phpMyAdmin Windows (Tab Import) SEBELUM mulai merekam!
-- File ini menyiapkan database `rumah_sakit` kondisi akhir Tugas 2 (6 tabel awal:
-- pasien, dokter, administrator, daftar, pasien_dokter, dokter_admin)
-- sehingga saat rekaman Tugas 3 dimulai, Anda benar-benar membuat transaksi1..5,
-- tabel obat, tabel transaksi_obat, dan Trigger dari nol seperti di video contoh!
-- ============================================================================

DROP DATABASE IF EXISTS rumah_sakit;
CREATE DATABASE rumah_sakit;
USE rumah_sakit;

CREATE TABLE administrator (
  id_admin INT(3) NOT NULL AUTO_INCREMENT PRIMARY KEY,
  nama_admin VARCHAR(30) NOT NULL,
  waktu_jaga VARCHAR(100) NOT NULL
) ENGINE=InnoDB;

CREATE TABLE dokter (
  id_dokter INT(3) NOT NULL AUTO_INCREMENT PRIMARY KEY,
  nama_dokter VARCHAR(30) NOT NULL,
  alamat_dokter VARCHAR(100) NOT NULL,
  tanggal_lahir DATE NOT NULL,
  no_hp VARCHAR(15) NOT NULL,
  spesialis VARCHAR(15) NOT NULL,
  waktu_kerja VARCHAR(100) NOT NULL
) ENGINE=InnoDB;

CREATE TABLE pasien (
  id_pasien INT(3) NOT NULL AUTO_INCREMENT PRIMARY KEY,
  nama_pasien VARCHAR(30) NOT NULL,
  alamat_pasien VARCHAR(100) NOT NULL,
  jenis_kelamin VARCHAR(1) NOT NULL
) ENGINE=InnoDB;

CREATE TABLE daftar (
  id_daftar INT(3) NOT NULL AUTO_INCREMENT PRIMARY KEY,
  id_pasien INT(3) NOT NULL,
  id_admin INT(3) NOT NULL,
  CONSTRAINT fk_daftar_pasien FOREIGN KEY (id_pasien) REFERENCES pasien(id_pasien) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT fk_daftar_admin FOREIGN KEY (id_admin) REFERENCES administrator(id_admin) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB;

CREATE TABLE pasien_dokter (
  id INT(3) NOT NULL AUTO_INCREMENT PRIMARY KEY,
  id_dokter INT(3) NOT NULL,
  id_pasien INT(3) NOT NULL,
  waktu_periksa DATETIME DEFAULT CURRENT_TIMESTAMP,
  resep VARCHAR(100) NOT NULL,
  CONSTRAINT fk_pd_dokter FOREIGN KEY (id_dokter) REFERENCES dokter(id_dokter) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT fk_pd_pasien FOREIGN KEY (id_pasien) REFERENCES pasien(id_pasien) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB;

CREATE TABLE dokter_admin (
  id_data INT(3) NOT NULL AUTO_INCREMENT PRIMARY KEY,
  id_dokter INT(3) NOT NULL,
  id_admin INT(3) NOT NULL,
  CONSTRAINT fk_da_dokter FOREIGN KEY (id_dokter) REFERENCES dokter(id_dokter) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT fk_da_admin FOREIGN KEY (id_admin) REFERENCES administrator(id_admin) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB;

INSERT INTO pasien (id_pasien, nama_pasien, alamat_pasien, jenis_kelamin) VALUES
(1, 'Andi Saputra', 'Jl. Merdeka No. 10', 'L'),
(2, 'Siti Aminah', 'Jl. Sudirman No. 25', 'P'),
(3, 'Budi Raharjo', 'Jl. Diponegoro No. 5', 'L'),
(4, 'Dewi Lestari', 'Jl. Ahmad Yani No. 12', 'P'),
(5, 'Eko Prasetyo', 'Jl. Gatot Subroto No. 8', 'L');

INSERT INTO dokter (id_dokter, nama_dokter, alamat_dokter, tanggal_lahir, no_hp, spesialis, waktu_kerja) VALUES
(1, 'dr. Hendra, Sp.PD', 'Jl. Melati No. 3', '1980-05-12', '081234567890', 'Penyakit Dalam', 'Senin-Jumat 08:00-14:00'),
(2, 'dr. Rina, Sp.A', 'Jl. Mawar No. 7', '1985-08-20', '081298765432', 'Anak', 'Senin-Sabtu 09:00-15:00');

INSERT INTO administrator (id_admin, nama_admin, waktu_jaga) VALUES
(1, 'Rizky Pratama', 'Pagi 07:00-15:00'),
(2, 'Nadia Putri', 'Siang 15:00-23:00');
