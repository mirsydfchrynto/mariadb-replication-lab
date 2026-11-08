@echo off
setlocal EnableDelayedExpansion
title WORKSPACE PRAKTIKUM BASIS DATA (WINDOWS + VIRTUALBOX UBUNTU)
color 0A

set "SCRIPT_DIR=%~dp0"
set "XAMPP_DIR=C:\xampp"
if not exist "%XAMPP_DIR%\mysql\bin\mysql.exe" (
    if exist "D:\xampp\mysql\bin\mysql.exe" set "XAMPP_DIR=D:\xampp"
)
set "MYSQL_BIN=%XAMPP_DIR%\mysql\bin"
set "MY_INI=%MYSQL_BIN%\my.ini"

:MENU
cls
echo ================================================================================
echo   CONTROL PANEL PRAKTIKUM BASIS DATA (TRANSAKSI ^& REPLIKASI MASTER-SLAVE)
echo   PILIH MODE PENGERJAAN DI LAPTOP WINDOWS INI:
echo.
echo   [0] DOWNLOAD ^& INSTALL 4 SOFTWARE WAJIB DOSEN + AUTO-CREATE VM UBUNTU
echo       - Otomatis download ^& install: (1) yEd Graph Editor, (2) XAMPP v8.2.12,
echo         (3) Oracle VirtualBox, dan (4) File ISO Linux Ubuntu (20.04 / 24.04)
echo       - Otomatis membuat VM Ubuntu di VirtualBox (RAM 4GB, Disk 25GB, NAT + Host-Only)
echo.
echo   PILIH MODE PENGERJAAN DI LAPTOP WINDOWS INI:
echo.
echo   [1] PERSIAPAN REKAM DARI DASAR (BEST PRACTICE - PALING DISARANKAN)
echo       - Membuka Firewall Windows (Port 3306 ^& Ping ICMP) agar Ubuntu pasti konek
echo       - Menyalakan XAMPP Control Panel (Apache ^& MySQL)
echo       - Mengisi database `rumah_sakit` dengan 6 tabel awal Tugas 2 (bersih, belum
echo         ada transaksi1-5 dan belum ada tabel obat, siap direkam dari nol!)
echo       - Membuka Notepad Contekan Copas, Panduan Step-by-Step Awam, dan phpMyAdmin
echo.
echo   [2] JALANKAN AUTO-HUMAN TEMPO PELAN (25-35 MENIT OTOMATIS KETIK ^& KLIK)
echo       - Membuka Chrome/Edge asli di Windows dan mengerjakan dari nol satu per satu
echo         dengan ketikan per huruf dan jeda pelan (atau tekan ENTER per langkah)
echo.
echo   [3] MODE TERIMA BERES INSTAN (5 DETIK LANGSUNG JADI SEMUA)
echo       - Otomatis memasang seluruh transaksi1-5, tabel obat, trigger, my.ini,
echo         user replikasi, dan menghasilkan file rumah_sakit.sql + COPAS-KE-UBUNTU.txt
echo.
echo   [4] BUKA PANDUAN AWAM ^& FOLDER LAPORAN WORD (.DOCX / .PDF)
echo   [9] KELUAR
echo ================================================================================
set /p PILIH="Masukkan pilihan Anda (0/1/2/3/4/9): "

if "%PILIH%"=="0" goto MODE_INSTALL_SOFTWARE
if "%PILIH%"=="1" goto MODE_DASAR
if "%PILIH%"=="2" goto MODE_AUTO_PELAN
if "%PILIH%"=="3" goto MODE_INSTAN
if "%PILIH%"=="4" goto MODE_DOKUMEN
if "%PILIH%"=="9" exit /b 0
goto MENU

:MODE_INSTALL_SOFTWARE
powershell -NoProfile -ExecutionPolicy Bypass -File "%SCRIPT_DIR%0-INSTALL-SOFTWARE-WAJIB-WINDOWS.ps1"
pause
goto MENU
if "%PILIH%"=="0" exit /b 0
goto MENU

:BUKA_FIREWALL_DAN_XAMPP
echo.
echo [1/4] Membuka akses Port 3306 dan Ping (ICMP) di Windows Firewall...
netsh advfirewall firewall delete rule name="MySQL_Repl_3306" >nul 2>&1
netsh advfirewall firewall add rule name="MySQL_Repl_3306" dir=in action=allow protocol=TCP localport=3306 >nul 2>&1
netsh advfirewall firewall delete rule name="ICMP_Ping_Allow" >nul 2>&1
netsh advfirewall firewall add rule name="ICMP_Ping_Allow" protocol=icmpv4:8,any dir=in action=allow >nul 2>&1
echo       [OK] Firewall Windows siap menerima ping ^& koneksi dari VirtualBox Ubuntu.

echo [2/4] Memastikan XAMPP Control Panel, Apache, dan MySQL aktif...
if exist "%XAMPP_DIR%\xampp-control.exe" (
    tasklist /FI "IMAGENAME eq xampp-control.exe" 2>NUL | find /I /N "xampp-control.exe" >NUL
    if errorlevel 1 start "" "%XAMPP_DIR%\xampp-control.exe"
)
tasklist /FI "IMAGENAME eq mysqld.exe" 2>NUL | find /I /N "mysqld.exe" >NUL
if errorlevel 1 (
    start "" /B "%MYSQL_BIN%\mysqld.exe" --defaults-file="%MY_INI%"
    timeout /t 4 /nobreak >nul
)
tasklist /FI "IMAGENAME eq httpd.exe" 2>NUL | find /I /N "httpd.exe" >NUL
if errorlevel 1 (
    start "" /B "%XAMPP_DIR%\apache\bin\httpd.exe"
    timeout /t 2 /nobreak >nul
)
exit /b 0

:MODE_DASAR
call :BUKA_FIREWALL_DAN_XAMPP
echo [3/4] Menyiapkan database `rumah_sakit` kondisi akhir Tugas 2 (6 tabel dasar)...
"%MYSQL_BIN%\mysql.exe" -u root < "%SCRIPT_DIR%sql\00_persiapan_tugas2.sql"
echo       [OK] Database `rumah_sakit` kini berisi 6 tabel Tugas 2 (siap direkam dari nol).

echo [4/4] Membuka Panduan Step-by-Step, Notepad Contekan Copas, dan phpMyAdmin...
start "" "%SCRIPT_DIR%PANDUAN-AWAM-STEP-BY-STEP.html"
start notepad.exe "%SCRIPT_DIR%CONTEKAN-COPAS-SAAT-REKAMAN.txt"
start "" "http://localhost/phpmyadmin"
echo.
echo ================================================================================
echo   SIAP DIREKAM! Silakan buka OBS Studio, mulai rekam layar Windows Anda,
echo   dan ikuti langkah di PANDUAN-AWAM-STEP-BY-STEP.html sambil copy-paste
echo   potongan kode dari jendela Notepad yang baru saja terbuka!
echo ================================================================================
pause
goto MENU

:MODE_AUTO_PELAN
call :BUKA_FIREWALL_DAN_XAMPP
"%MYSQL_BIN%\mysql.exe" -u root < "%SCRIPT_DIR%sql\00_persiapan_tugas2.sql"
echo.
echo Pilih kecepatan Auto-Human:
echo   [A] Otomatis Tempo Pelan (~25-30 Menit, jeda 20 detik per tahapan)
echo   [B] Mode Interaktif (Ketik ^& Klik otomatis, pindah langkah saat tekan ENTER)
set /p SUBMODE="Pilihan (A/B): "
pip show playwright >nul 2>&1
if errorlevel 1 (
    echo Menginstall pustaka otomatisasi browser...
    pip install playwright
)
if /I "%SUBMODE%"=="B" (
    python "%SCRIPT_DIR%auto_human_windows.py" --interactive
) else (
    set "STEP_DELAY=20"
    python "%SCRIPT_DIR%auto_human_windows.py"
)
pause
goto MENU

:MODE_INSTAN
call :BUKA_FIREWALL_DAN_XAMPP
echo [3/4] Mengatur Replikasi Master di %MY_INI% dan merestart MySQL...
if not exist "%MY_INI%.backup_ori" copy /Y "%MY_INI%" "%MY_INI%.backup_ori" >nul
findstr /C:"binlog-do-db = rumah_sakit" "%MY_INI%" >nul 2>&1
if errorlevel 1 (
    powershell -NoProfile -Command ^
      "$c = Get-Content '%MY_INI%' -Raw; " ^
      "$c = $c -replace '(?m)^server-id\s*=\s*1', '#server-id = 1'; " ^
      "$rep = \"`r`n[mysqld]`r`nlog-bin = mysql-bin`r`nserver-id = 1`r`nbinlog-do-db = rumah_sakit`r`nbind-address = 0.0.0.0`r`n\"; " ^
      "Set-Content -Path '%MY_INI%' -Value ($c + $rep) -Encoding ASCII"
    taskkill /F /IM mysqld.exe >nul 2>&1
    timeout /t 2 /nobreak >nul
    start "" /B "%MYSQL_BIN%\mysqld.exe" --defaults-file="%MY_INI%"
    timeout /t 4 /nobreak >nul
)

echo [4/4] Memasang seluruh tabel, transaksi1-5, trigger tg_stok_obat, dan user replikasi...
"%MYSQL_BIN%\mysql.exe" -u root < "%SCRIPT_DIR%sql\00_persiapan_tugas2.sql"
"%MYSQL_BIN%\mysql.exe" -u root < "%SCRIPT_DIR%sql\01_full_transaksi_dan_trigger.sql"
"%MYSQL_BIN%\mysql.exe" -u root -e "CREATE USER IF NOT EXISTS 'subhan'@'%%' IDENTIFIED BY '1234'; GRANT REPLICATION SLAVE, REPLICATION CLIENT ON *.* TO 'subhan'@'%%'; FLUSH PRIVILEGES; RESET MASTER;"
"%MYSQL_BIN%\mysqldump.exe" -u root --routines --triggers rumah_sakit > "%SCRIPT_DIR%rumah_sakit.sql"

for /f "tokens=1,2" %%a in ('"%MYSQL_BIN%\mysql.exe" -u root -N -e "SHOW MASTER STATUS;"') do (
    set "LOG_FILE=%%a"
    set "LOG_POS=%%b"
)
set "WIN_IP=192.168.56.1"
for /f "tokens=2 delims=:" %%i in ('ipconfig ^| findstr /C:"192.168.56."') do (
    for /f "tokens=* delims= " %%j in ("%%i") do set "WIN_IP=%%j"
)

(
echo STOP SLAVE;
echo CHANGE MASTER TO
echo   MASTER_HOST='%WIN_IP%',
echo   MASTER_USER='subhan',
echo   MASTER_PASSWORD='1234',
echo   MASTER_LOG_FILE='%LOG_FILE%',
echo   MASTER_LOG_POS=%LOG_POS%;
echo START SLAVE;
) > "%SCRIPT_DIR%COPAS-KE-UBUNTU.txt"

echo.
echo [SELESAI] File `rumah_sakit.sql` dan `COPAS-KE-UBUNTU.txt` telah siap!
start notepad.exe "%SCRIPT_DIR%COPAS-KE-UBUNTU.txt"
start "" "http://localhost/phpmyadmin"
pause
goto MENU

:MODE_DOKUMEN
start "" "%SCRIPT_DIR%PANDUAN-AWAM-STEP-BY-STEP.html"
explorer.exe "%SCRIPT_DIR%docs"
goto MENU
