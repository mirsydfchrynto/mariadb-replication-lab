# MariaDB Transaction & Replication Lab Workspace

Local sandbox for MariaDB/MySQL InnoDB transaction routines (`START TRANSACTION`, `COMMIT`, `ROLLBACK`, `SAVEPOINT`, `AFTER INSERT` triggers) and asynchronous Master-Slave replication (`Windows Host` -> `Ubuntu Guest VM`).

## Quick Start on Windows

### Option A — Clone via Git
```powershell
git clone https://github.com/mirsydfchrynto/mariadb-replication-lab.git
cd mariadb-replication-lab
.\START-HERE.bat
```

### Option B — Download ZIP (Without Git installed)
Open in browser or run in PowerShell:
```powershell
Invoke-WebRequest -Uri "https://github.com/mirsydfchrynto/mariadb-replication-lab/archive/refs/heads/main.zip" -OutFile "lab.zip"
Expand-Archive -Path "lab.zip" -DestinationPath "." -Force
cd mariadb-replication-lab-main
.\START-HERE.bat
```

## Included Components
- `START-HERE.bat` — Interactive Windows control center (Firewall setup, XAMPP starter, Base schema initializer, Slow-tempo browser automation, or Instant 1-click setup).
- `PANDUAN-AWAM-STEP-BY-STEP.html` — Beginner-friendly visual guide with 1-click Copy buttons for every step from start to finish.
- `CONTEKAN-COPAS-SAAT-REKAMAN.txt` — Plain-text snippet sheet for Notepad during screen recording.
- `auto_human_windows.py` — Human-paced browser automation script (character-by-character typing and configurable step pauses).
- `ubuntu-slave-setup.sh` — Automated Slave configuration script for Ubuntu VirtualBox (`/opt/lampp`).
- `erd/skema_rumah_sakit.graphml` — Ready-to-open ERD file for yEd Graph Editor.
- `docs/` — Complete 21-page documentation report (`.docx` and `.pdf`) with 33 step-by-step verification screenshots.
- `audio/vo_panduan_bahasa_indonesia.mp3` — Full Indonesian voice-over reference track.
