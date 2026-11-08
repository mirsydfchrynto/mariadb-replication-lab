#!/usr/bin/env bash
# ============================================================================
# 2-SETUP-SLAVE-UBUNTU.sh
# Skrip Universal Setup Slave Replikasi (Mendukung XAMPP Ubuntu /opt/lampp,
# MariaDB/MySQL Native Linux, maupun Docker di Arch Linux)
# Penggunaan di Ubuntu VirtualBox:
#   sudo bash 2-SETUP-SLAVE-UBUNTU.sh 192.168.56.1
# ============================================================================
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MASTER_HOST="${1:-192.168.56.1}"
REPL_USER="${2:-repl_user}"
REPL_PASS="${3:-password123}"

echo "============================================================================"
echo "  SETUP OTOMATIS SLAVE MYSQL (UBUNTU / LINUX) - TUGAS 3 BASIS DATA UT"
echo "============================================================================"

# Mode 1: Jika dijalankan di Arch Linux dengan Docker (tanpa /opt/lampp)
if [ ! -d "/opt/lampp" ] && command -v docker >/dev/null 2>&1 && [ -f "$SCRIPT_DIR/docker-compose.yml" ]; then
    echo "[INFO] Mendeteksi lingkungan Docker Linux. Menjalankan reset-praktikum.sh..."
    bash "$SCRIPT_DIR/reset-praktikum.sh"
    exit 0
fi

# Mode 2: XAMPP di Ubuntu VirtualBox (/opt/lampp)
if [ -d "/opt/lampp" ]; then
    MYSQL_BIN="/opt/lampp/bin/mysql"
    MYSQL_UPGRADE="/opt/lampp/bin/mysql_upgrade"
    MY_CNF="/opt/lampp/etc/my.cnf"

    echo "[OK] XAMPP Linux ditemukan di /opt/lampp"
    cp -n "$MY_CNF" "${MY_CNF}.backup_ut" 2>/dev/null || true

    # Komentari server-id = 1 bawaan agar tidak bentrok dengan Master
    sed -i 's/^[[:space:]]*server-id[[:space:]]*=[[:space:]]*1/#server-id = 1/g' "$MY_CNF"

    if ! grep -q "replicate-do-db = rumah_sakit" "$MY_CNF"; then
        echo "[INFO] Menambahkan server-id = 2 & replicate-do-db = rumah_sakit ke $MY_CNF..."
        awk '/^\[mysqld\]/{print; print "server-id = 2\nreplicate-do-db = rumah_sakit"; next}1' "$MY_CNF" > "${MY_CNF}.tmp" && mv "${MY_CNF}.tmp" "$MY_CNF"
    fi
    chmod 644 "$MY_CNF"

    echo "[INFO] Merestart layanan XAMPP Ubuntu..."
    /opt/lampp/lampp restart

    echo "[INFO] Menjalankan mysql_upgrade untuk mencegah error import Stored Procedures..."
    "$MYSQL_UPGRADE" -u root --force >/dev/null 2>&1 || true
else
    echo "[ERROR] /opt/lampp tidak ditemukan. Pastikan XAMPP Ubuntu sudah terinstall."
    exit 1
fi

echo "[INFO] Menguji koneksi ping ke Master Windows ($MASTER_HOST)..."
if ping -c 2 -W 2 "$MASTER_HOST" >/dev/null 2>&1; then
    echo "[OK] Koneksi jaringan ke Master ($MASTER_HOST) berhasil!"
else
    echo "[PERINGATAN] Ping ke $MASTER_HOST belum merespons. Pastikan Adapter VirtualBox = Host-Only / Bridged dan 1-SETUP-MASTER-WINDOWS.bat sudah dijalankan."
fi

echo "[INFO] Membuat database rumah_sakit dan mengimpor rumah_sakit_dump.sql..."
"$MYSQL_BIN" -u root -e "DROP DATABASE IF EXISTS rumah_sakit; CREATE DATABASE rumah_sakit;"
if [ -f "$SCRIPT_DIR/rumah_sakit_dump.sql" ]; then
    "$MYSQL_BIN" -u root rumah_sakit < "$SCRIPT_DIR/rumah_sakit_dump.sql"
else
    "$MYSQL_BIN" -u root < "$SCRIPT_DIR/01_praktikum_transaksi_rumah_sakit.sql"
fi

echo "[INFO] Mengambil posisi binlog (File & Position) langsung dari Master ($MASTER_HOST)..."
MASTER_STATUS=$("$MYSQL_BIN" -h "$MASTER_HOST" -u "$REPL_USER" -p"$REPL_PASS" -N -e "SHOW MASTER STATUS;" 2>/dev/null || true)

if [ -n "$MASTER_STATUS" ]; then
    LOG_FILE=$(echo "$MASTER_STATUS" | awk '{print $1}')
    LOG_POS=$(echo "$MASTER_STATUS" | awk '{print $2}')
    echo "[OK] Berhasil membaca Master Status: File=$LOG_FILE, Position=$LOG_POS"
else
    LOG_FILE="mysql-bin.000001"
    LOG_POS="328"
    echo "[INFO] Menggunakan default File=$LOG_FILE, Position=$LOG_POS"
fi

echo "[INFO] Mengaktifkan koneksi Replikasi Slave ke Master..."
"$MYSQL_BIN" -u root -e "
STOP SLAVE;
RESET SLAVE ALL;
CHANGE MASTER TO
  MASTER_HOST='$MASTER_HOST',
  MASTER_USER='$REPL_USER',
  MASTER_PASSWORD='$REPL_PASS',
  MASTER_LOG_FILE='$LOG_FILE',
  MASTER_LOG_POS=$LOG_POS;
START SLAVE;
"

sleep 2
echo "============================================================================"
echo "  STATUS REPLIKASI SLAVE SAAT INI:"
echo "============================================================================"
"$MYSQL_BIN" -u root -e "SHOW SLAVE STATUS\G" | grep -E "Slave_IO_State|Master_Host|Master_Log_File|Read_Master_Log_Pos|Slave_IO_Running|Slave_SQL_Running|Last_Error"
echo "============================================================================"
echo "  SELESAI! Buka http://localhost/phpmyadmin di browser Ubuntu."
echo "============================================================================"
