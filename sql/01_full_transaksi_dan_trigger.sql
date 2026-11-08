-- ============================================================================
-- TUGAS 3 MSIM4206 (BASIS DATA) - SESUAI MODUL PRAKTIKUM UT & 3 VIDEO CONTOH
-- Database: rumah_sakit (Melanjutkan Tugas 2 + Transaksi + Trigger + Replikasi)
-- ============================================================================

CREATE DATABASE IF NOT EXISTS rumah_sakit;
USE rumah_sakit;

DROP TABLE IF EXISTS transaksi_obat;
DROP TABLE IF EXISTS obat;
DROP TABLE IF EXISTS pasien;

-- 1. Tabel Pasien (melanjutkan struktur Tugas 2)
CREATE TABLE pasien (
  id_pasien INT(11) NOT NULL PRIMARY KEY,
  nama_pasien VARCHAR(50) NOT NULL,
  jenis_kelamin CHAR(1) NOT NULL,
  alamat_pasien VARCHAR(100) NOT NULL
) ENGINE=InnoDB;

INSERT INTO pasien (id_pasien, nama_pasien, jenis_kelamin, alamat_pasien) VALUES
(1, 'Andi Saputra', 'L', 'Jl. Merdeka No. 10'),
(2, 'Siti Aminah', 'P', 'Jl. Sudirman No. 25'),
(3, 'Budi Raharjo', 'L', 'Jl. Diponegoro No. 5'),
(4, 'Dewi Lestari', 'P', 'Jl. Ahmad Yani No. 12'),
(5, 'Eko Prasetyo', 'L', 'Jl. Gatot Subroto No. 8');

-- ============================================================================
-- BAGIAN A: 5 STORED PROCEDURE (ROUTINES) TRANSAKSI SESUAI MODUL UT
-- ============================================================================

-- 1. transaksi1: START TRANSACTION tanpa COMMIT (Data hanya tampil sementara di sesi, tidak permanen)
DROP PROCEDURE IF EXISTS transaksi1;
DELIMITER $$
CREATE PROCEDURE transaksi1()
BEGIN
  START TRANSACTION;
  INSERT INTO pasien VALUES (11, 'Said', 'L', 'Bandung');
  SELECT * FROM pasien;
END$$
DELIMITER ;

-- 2. transaksi2: START TRANSACTION dengan COMMIT (Data tersimpan permanen di tabel pasien)
DROP PROCEDURE IF EXISTS transaksi2;
DELIMITER $$
CREATE PROCEDURE transaksi2()
BEGIN
  START TRANSACTION;
  INSERT INTO pasien VALUES (11, 'Said', 'L', 'Bandung');
  COMMIT;
  SELECT * FROM pasien;
END$$
DELIMITER ;

-- 3. transaksi3: UPDATE dibatalkan dengan ROLLBACK (Nama Said tidak jadi berubah ke Arif)
DROP PROCEDURE IF EXISTS transaksi3;
DELIMITER $$
CREATE PROCEDURE transaksi3()
BEGIN
  START TRANSACTION;
  UPDATE pasien SET nama_pasien = 'Arif' WHERE id_pasien = 11;
  ROLLBACK;
  COMMIT;
  SELECT * FROM pasien;
END$$
DELIMITER ;

-- 4. transaksi4: UPDATE + INSERT dibatalkan oleh ROLLBACK
DROP PROCEDURE IF EXISTS transaksi4;
DELIMITER $$
CREATE PROCEDURE transaksi4()
BEGIN
  START TRANSACTION;
  UPDATE pasien SET nama_pasien = 'Asep' WHERE id_pasien = 11;
  INSERT INTO pasien VALUES (12, 'Dudung', 'L', 'Cimahi');
  ROLLBACK;
  SELECT * FROM pasien;
END$$
DELIMITER ;

-- 5. transaksi5: SAVEPOINT (point1) & ROLLBACK TO point1
-- ID 11 diupdate jadi Asep, ID 12 (Dudung) masuk sebelum point1, ID 13 (Maman) batal karena ROLLBACK TO point1, ID 14 (Ujang) masuk lalu COMMIT
DROP PROCEDURE IF EXISTS transaksi5;
DELIMITER $$
CREATE PROCEDURE transaksi5()
BEGIN
  START TRANSACTION;
  UPDATE pasien SET nama_pasien = 'Asep' WHERE id_pasien = 11;
  INSERT INTO pasien VALUES (12, 'Dudung', 'L', 'Cimahi');
  SAVEPOINT point1;
  INSERT INTO pasien VALUES (13, 'Maman', 'L', 'Garut');
  ROLLBACK TO point1;
  INSERT INTO pasien VALUES (14, 'Ujang', 'L', 'Tasikmalaya');
  COMMIT;
  SELECT * FROM pasien;
END$$
DELIMITER ;

-- ============================================================================
-- BAGIAN B: TABEL OBAT, TRANSAKSI_OBAT, FOREIGN KEY CASCADE, DAN TRIGGER
-- ============================================================================

CREATE TABLE obat (
  id_obat INT(6) NOT NULL PRIMARY KEY,
  kode_obat VARCHAR(5) NOT NULL,
  nama_obat VARCHAR(30) NOT NULL,
  harga INT(10) NOT NULL,
  stok INT(5) NOT NULL
) ENGINE=InnoDB;

CREATE TABLE transaksi_obat (
  id_transaksi INT(6) NOT NULL PRIMARY KEY,
  id_pasien INT(11) NOT NULL,
  id_obat INT(6) NOT NULL,
  jumlah INT(5) NOT NULL,
  total_harga INT(10) NOT NULL,
  INDEX idx_pasien (id_pasien),
  INDEX idx_obat (id_obat),
  CONSTRAINT fk_to_pasien FOREIGN KEY (id_pasien) REFERENCES pasien(id_pasien) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT fk_to_obat FOREIGN KEY (id_obat) REFERENCES obat(id_obat) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB;

INSERT INTO obat (id_obat, kode_obat, nama_obat, harga, stok) VALUES
(1, 'A001', 'Paracetamol', 5000, 100),
(2, 'A002', 'Amoxicillin', 10000, 50),
(3, 'A003', 'Betadine', 15000, 100);

-- Trigger: otomatis mengurangi stok obat setiap kali ada INSERT di transaksi_obat
DROP TRIGGER IF EXISTS tr_beli;
DELIMITER $$
CREATE TRIGGER tr_beli
AFTER INSERT ON transaksi_obat
FOR EACH ROW
BEGIN
  UPDATE obat
  SET stok = stok - NEW.jumlah
  WHERE id_obat = NEW.id_obat;
END$$
DELIMITER ;
