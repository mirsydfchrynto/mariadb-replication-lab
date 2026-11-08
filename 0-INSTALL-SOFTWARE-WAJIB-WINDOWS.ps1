# ==============================================================================
# 0-INSTALL-SOFTWARE-WAJIB-WINDOWS.ps1
# Otomatis mengunduh & menginstal ke-4 Software Wajib Mata Kuliah Basis Data UT
# sesuai pengumuman resmi Tutor/Dosen:
#   1) Aplikasi yEd Graph Editor (https://www.yworks.com/products/yed)
#   2) Aplikasi XAMPP v8.2.12 (https://www.apachefriends.org/download.html)
#   3) Aplikasi VirtualBox (https://www.virtualbox.org/wiki/Downloads)
#   4) File ISO Linux Ubuntu (Versi 20.04 Focal / Versi 24.04 Noble LTS)
#   5) Otomatis membuat Virtual Machine Ubuntu di VirtualBox (RAM 4GB, Disk 25GB,
#      Adapter 1 = NAT untuk internet, Adapter 2 = Host-Only untuk replikasi)
# ==============================================================================

$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$DownloadDir = Join-Path $ScriptDir "installers"
if (-not (Test-Path $DownloadDir)) { New-Item -ItemType Directory -Path $DownloadDir | Out-Null }

Write-Host "==============================================================================" -ForegroundColor Cyan
Write-Host "  AUTO-INSTALLER 4 SOFTWARE WAJIB BASIS DATA UT + AUTO-BUILDER VM UBUNTU" -ForegroundColor Cyan
Write-Host "==============================================================================" -ForegroundColor Cyan
Write-Host ""

# ------------------------------------------------------------------------------
# 1. Cek & Install Aplikasi yEd Graph Editor
# ------------------------------------------------------------------------------
Write-Host "[1/5] Memeriksa Aplikasi yEd Graph Editor..." -ForegroundColor Yellow
$yedPaths = @(
    "${env:ProgramFiles}\yWorks\yEd\yEd.exe",
    "${env:ProgramFiles(x86)}\yWorks\yEd\yEd.exe",
    "${env:LOCALAPPDATA}\Programs\yWorks\yEd\yEd.exe"
)
$yedFound = $yedPaths | Where-Object { Test-Path $_ } | Select-Object -First 1

if ($yedFound) {
    Write-Host "      [OK] yEd Graph Editor sudah terinstall di: $yedFound" -ForegroundColor Green
} else {
    Write-Host "      [INFO] Menginstall yEd Graph Editor via Winget / Installer resmi..." -ForegroundColor Cyan
    try {
        winget install --id yWorks.yEd --accept-package-agreements --accept-source-agreements
    } catch {
        Write-Host "      [INFO] Membuka halaman unduhan resmi yEd (https://www.yworks.com/products/yed)..." -ForegroundColor Yellow
        Start-Process "https://www.yworks.com/products/yed/download#download"
    }
}

# ------------------------------------------------------------------------------
# 2. Cek & Install XAMPP for Windows (Versi 8.2.12 - Sama dengan Ubuntu nanti)
# ------------------------------------------------------------------------------
Write-Host "[2/5] Memeriksa Aplikasi XAMPP Windows (Versi 8.2.12)..." -ForegroundColor Yellow
if ((Test-Path "C:\xampp\mysql\bin\mysql.exe") -or (Test-Path "D:\xampp\mysql\bin\mysql.exe")) {
    Write-Host "      [OK] XAMPP Windows sudah terinstall." -ForegroundColor Green
} else {
    $xamppExe = Join-Path $DownloadDir "xampp-windows-x64-8.2.12-0-VS16-installer.exe"
    $xamppUrl = "https://sourceforge.net/projects/xampp/files/XAMPP%20Windows/8.2.12/xampp-windows-x64-8.2.12-0-VS16-installer.exe/download"
    Write-Host "      [INFO] Mengunduh XAMPP Windows v8.2.12 (agar sama persis dengan versi Ubuntu)..." -ForegroundColor Cyan
    & curl.exe -L -C - -o "$xamppExe" "$xamppUrl"
    Write-Host "      [INFO] Menjalankan installer XAMPP Windows (Silakan klik Next sampai selesai di C:\xampp)..." -ForegroundColor Yellow
    Start-Process -FilePath "$xamppExe" -Wait
}

# ------------------------------------------------------------------------------
# 3. Cek & Install Oracle VM VirtualBox
# ------------------------------------------------------------------------------
Write-Host "[3/5] Memeriksa Aplikasi Oracle VM VirtualBox..." -ForegroundColor Yellow
$vboxManage = "C:\Program Files\Oracle\VirtualBox\VBoxManage.exe"
if (Test-Path $vboxManage) {
    Write-Host "      [OK] VirtualBox sudah terinstall di: $vboxManage" -ForegroundColor Green
} else {
    $vboxExe = Join-Path $DownloadDir "VirtualBox-7.0.20-163906-Win.exe"
    $vboxUrl = "https://download.virtualbox.org/virtualbox/7.0.20/VirtualBox-7.0.20-163906-Win.exe"
    Write-Host "      [INFO] Mengunduh Oracle VirtualBox v7.0.20..." -ForegroundColor Cyan
    & curl.exe -L -C - -o "$vboxExe" "$vboxUrl"
    Write-Host "      [INFO] Menginstall VirtualBox..." -ForegroundColor Yellow
    Start-Process -FilePath "$vboxExe" -Wait
}

# ------------------------------------------------------------------------------
# 4. Cek / Unduh File ISO Linux Ubuntu (Versi 20.04 LTS atau 24.04.3 LTS)
# ------------------------------------------------------------------------------
Write-Host "[4/5] Memeriksa File ISO Linux Ubuntu..." -ForegroundColor Yellow
$existingIso = Get-ChildItem -Path $DownloadDir, "$env:USERPROFILE\Downloads" -Filter "*ubuntu*desktop*amd64*.iso" -ErrorAction SilentlyContinue | Select-Object -First 1

if ($existingIso) {
    $isoPath = $existingIso.FullName
    Write-Host "      [OK] File ISO Ubuntu sudah ditemukan di: $isoPath" -ForegroundColor Green
} else {
    Write-Host ""
    Write-Host "Pilih versi ISO Ubuntu sesuai tautan Dosen/Modul:" -ForegroundColor Cyan
    Write-Host "  [1] Ubuntu 20.04.6 LTS (Focal Fossa - Lebih ringan ~4.1 GB, sangat stabil untuk XAMPP)"
    Write-Host "  [2] Ubuntu 24.04.2 LTS (Noble Numbat - Versi 24 terbaru ~5.8 GB)"
    Write-Host "  [3] Saya sudah punya file ISO Ubuntu di folder lain (Pilih file manual)"
    $pilIso = Read-Host "Masukkan pilihan (1/2/3)"

    if ($pilIso -eq "3") {
        Add-Type -AssemblyName System.Windows.Forms
        $dlg = New-Object System.Windows.Forms.OpenFileDialog
        $dlg.Filter = "ISO Files (*.iso)|*.iso"
        $dlg.Title = "Pilih File ISO Ubuntu Desktop"
        if ($dlg.ShowDialog() -eq "OK") {
            $isoPath = $dlg.FileName
        } else {
            throw "File ISO tidak dipilih."
        }
    } elseif ($pilIso -eq "2") {
        $isoPath = Join-Path $DownloadDir "ubuntu-24.04.2-desktop-amd64.iso"
        $isoUrl = "https://releases.ubuntu.com/24.04/ubuntu-24.04.2-desktop-amd64.iso"
        Write-Host "      [INFO] Mengunduh Ubuntu 24.04 LTS (Mendukung auto-resume jika terputus)..." -ForegroundColor Cyan
        & curl.exe -L -C - -o "$isoPath" "$isoUrl"
    } else {
        $isoPath = Join-Path $DownloadDir "ubuntu-20.04.6-desktop-amd64.iso"
        $isoUrl = "https://releases.ubuntu.com/focal/ubuntu-20.04.6-desktop-amd64.iso"
        Write-Host "      [INFO] Mengunduh Ubuntu 20.04.6 LTS Focal (Mendukung auto-resume jika terputus)..." -ForegroundColor Cyan
        & curl.exe -L -C - -o "$isoPath" "$isoUrl"
    }
}

# ------------------------------------------------------------------------------
# 5. Otomatis Membuat Virtual Machine Ubuntu di VirtualBox (Sesuai Video Dosen QfTBsFqXXOw)
# ------------------------------------------------------------------------------
if (Test-Path $vboxManage) {
    Write-Host "[5/5] Mengonfigurasi Virtual Machine 'Linux-Ubuntu-BasisData' di VirtualBox..." -ForegroundColor Yellow
    $vmName = "Linux-Ubuntu-BasisData"
    $vmList = & $vboxManage list vms
    if ($vmList -match $vmName) {
        Write-Host "      [OK] VM '$vmName' sudah terdaftar di VirtualBox." -ForegroundColor Green
    } else {
        $vmFolder = Join-Path $env:USERPROFILE "VirtualBox VMs\$vmName"
        $vdiPath = Join-Path $vmFolder "$vmName.vdi"

        # Pastikan Host-Only Network Adapter tersedia di VirtualBox
        $hostOnlyList = & $vboxManage list hostonlyifs
        if (-not ($hostOnlyList -match "VirtualBox Host-Only Ethernet Adapter")) {
            Write-Host "      [INFO] Membuat VirtualBox Host-Only Ethernet Adapter..." -ForegroundColor Cyan
            & $vboxManage hostonlyif create | Out-Null
        }

        Write-Host "      [INFO] Membuat VM '$vmName' (RAM 4096 MB, CPU 2 Core, Disk 25 GB)..." -ForegroundColor Cyan
        & $vboxManage createvm --name "$vmName" --ostype "Ubuntu_64" --register
        & $vboxManage modifyvm "$vmName" --memory 4096 --cpus 2 --vram 128 --graphicscontroller vmsvga --ioapic on --rtcuseutc on
        # Adapter 1 = NAT (Agar Ubuntu punya internet untuk download XAMPP Linux)
        # Adapter 2 = Host-Only Adapter (Agar Windows & Ubuntu langsung terhubung di 192.168.56.x tanpa perlu matikan VM!)
        & $vboxManage modifyvm "$vmName" --nic1 nat
        & $vboxManage modifyvm "$vmName" --nic2 hostonly --hostonlyadapter2 "VirtualBox Host-Only Ethernet Adapter"

        & $vboxManage createhd --filename "$vdiPath" --size 25600 --format VDI
        & $vboxManage storagectl "$vmName" --name "SATA Controller" --add sata --controller IntelAhci
        & $vboxManage storageattach "$vmName" --storagectl "SATA Controller" --port 0 --device 0 --type hdd --medium "$vdiPath"
        & $vboxManage storagectl "$vmName" --name "IDE Controller" --add ide
        & $vboxManage storageattach "$vmName" --storagectl "IDE Controller" --port 0 --device 0 --type dvddrive --medium "$isoPath"

        # Pasang Shared Folder otomatis ke folder repositori ini agar file rumah_sakit.sql tidak perlu pakai flashdisk!
        & $vboxManage sharedfolder add "$vmName" --name "praktikum_share" --hostpath "$ScriptDir" --automount

        Write-Host "      [OK] VM '$vmName' berhasil dibuat lengkap dengan ISO Ubuntu & jaringan NAT + Host-Only!" -ForegroundColor Green
    }

    Write-Host ""
    $startVm = Read-Host "Apakah ingin langsung menyalakan VM Ubuntu di VirtualBox sekarang? (Y/N)"
    if ($startVm -match "^[Yy]") {
        & $vboxManage startvm "$vmName" --type gui
    }
}

Write-Host ""
Write-Host "==============================================================================" -ForegroundColor Green
Write-Host "  SELURUH SOFTWARE WAJIB & VM VIRTUALBOX TELAH SIAP!" -ForegroundColor Green
Write-Host "  Setelah masuk ke Desktop Ubuntu di VirtualBox, buka Terminal Ubuntu dan" -ForegroundColor Green
Write-Host "  jalankan 1 baris ini untuk otomatis download & install XAMPP Linux v8.2.12:" -ForegroundColor Green
Write-Host "    curl -fsSL https://raw.githubusercontent.com/mirsydfchrynto/mariadb-replication-lab/main/ubuntu-install-xampp-dan-slave.sh | sudo bash" -ForegroundColor Yellow
Write-Host "==============================================================================" -ForegroundColor Green
