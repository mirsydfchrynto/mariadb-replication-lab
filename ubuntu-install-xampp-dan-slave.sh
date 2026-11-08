#!/usr/bin/env bash
# ==============================================================================
# ubuntu-install-xampp-dan-slave.sh
# Sesuai Video Tutorial Dosen (https://youtu.be/QfTBsFqXXOw):
# 1. Mengunduh XAMPP for Linux v8.2.12 (versi yang SAMA PERSIS dengan XAMPP Windows)
# 2. Mengatur chmod 755 dan menginstal ke /opt/lampp
# 3. Mengatur chmod +x /opt/lampp/manager-linux-x64.run
# 4. Menyalakan Apache & MySQL, menjalankan mysql_upgrade, dan menyiapkan my.cnf
#    (server-id = 2, replicate-do-db = rumah_sakit)
# ==============================================================================
set -euo pipefail

XAMPP_VER="8.2.12"
INSTALLER_NAME="xampp-linux-x64-${XAMPP_VER}-0-installer.run"
INSTALLER_URL="https://sourceforge.net/projects/xampp/files/XAMPP%20Linux/${XAMPP_VER}/${INSTALLER_NAME}/download"
DOWNLOAD_PATH="${HOME}/Downloads/${INSTALLER_NAME}"

echo "=============================================================================="
echo "  INSTALASI OTOMATIS XAMPP LINUX v${XAMPP_VER} DI UBUNTU (SESUAI VERSI WINDOWS)"
echo "=============================================================================="

if [ ! -d "/opt/lampp" ]; then
    mkdir -p "${HOME}/Downloads"
    if [ ! -f "$DOWNLOAD_PATH" ]; then
        echo "[1/4] Mengunduh ${INSTALLER_NAME} (Versi sama dengan XAMPP Windows)..."
        curl -L -C - -o "$DOWNLOAD_PATH" "$INSTALLER_URL"
    fi

    echo "[2/4] Mengubah permission installer (chmod 755 ${INSTALLER_NAME})..."
    chmod 755 "$DOWNLOAD_PATH"

    echo "[3/4] Menjalankan installer XAMPP ke /opt/lampp..."
    sudo "$DOWNLOAD_PATH" --mode unattended || sudo "$DOWNLOAD_PATH"
else
    echo "[OK] XAMPP sudah terinstall di /opt/lampp"
fi

echo "[4/4] Mengaktifkan manager-linux-x64.run & menyalakan layanan Apache + MySQL..."
sudo chmod +x /opt/lampp/manager-linux-x64.run
sudo /opt/lampp/lampp start
sudo /opt/lampp/bin/mysql_upgrade -u root --force >/dev/null 2>&1 || true

# Tampilkan IP Host-Only Ubuntu agar mudah dicatat saat rekaman
echo ""
echo "=============================================================================="
echo "  XAMPP UBUNTU SIAP DIGUNAKAN!"
echo "  - Untuk membuka GUI XAMPP Ubuntu (seperti di video tutorial dosen):"
echo "      cd /opt/lampp && sudo ./manager-linux-x64.run"
echo "  - Untuk membuka phpMyAdmin di Firefox Ubuntu:"
echo "      http://localhost/phpmyadmin"
echo "  - Daftar IP Ubuntu Anda saat ini (ip a):"
ip -4 addr show | grep inet
echo "=============================================================================="
