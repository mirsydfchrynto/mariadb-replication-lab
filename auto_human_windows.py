#!/usr/bin/env python3
"""
auto_human_windows.py
Menjalankan browser Chrome/Edge secara asli (non-headless) di atas Desktop Windows
dengan gerakan mouse alami dan ketikan karakter demi karakter (seperti diketik
manusia) dari langkah paling dasar (membuka database rumah_sakit hasil Tugas 2,
membuat routine transaksi1 s/d transaksi5 satu per satu, membuat tabel obat &
transaksi_obat, mengatur relasi, membuat trigger tg_stok_obat, menguji insert,
membuat user replikasi, hingga mengecek status replikasi).

Dapat dijalankan dalam:
1. Mode Tempo Pelan Otomatis (default jeda 18-20 detik per tahapan agar video ~25-30 menit)
2. Mode Interaktif (`python auto_human_windows.py --interactive` -> menunggu tekan ENTER di tiap tahapan)
"""
import os
import re
import sys
import time
from playwright.sync_api import sync_playwright

MASTER_URL = os.environ.get("MASTER_PMA_URL", "http://localhost/phpmyadmin")
DB_NAME = "rumah_sakit"
STEP_DELAY = float(os.environ.get("STEP_DELAY", "18.0"))
TYPE_DELAY_MS = int(os.environ.get("TYPE_DELAY_MS", "75"))
INTERACTIVE = "--interactive" in sys.argv


def find_browser_exe() -> str | None:
    for p in [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
        "/usr/bin/chromium",
    ]:
        if os.path.exists(p):
            return p
    return None


def wait_step(title: str, detail: str, sec: float = STEP_DELAY):
    print(f"\n======================================================================")
    print(f"[TAHAP] {title}")
    print(f"        {detail}")
    print(f"======================================================================")
    if INTERACTIVE:
        input(">>> Tekan [ENTER] untuk lanjut ke langkah berikutnya...")
    else:
        time.sleep(sec)


def fill_codemirror_human(page, selector: str, text: str):
    cm = page.locator(selector).first
    if cm.count() > 0 and cm.is_visible():
        cm.click()
        page.keyboard.press("Control+A")
        page.keyboard.press("Backspace")
        # Ketik per baris dengan kecepatan manusia agar terlihat natural di layar
        for line in text.splitlines():
            page.keyboard.type(line, delay=TYPE_DELAY_MS)
            page.keyboard.press("Enter")
    else:
        page.evaluate(
            """([sel, txt]) => {
                const el = document.querySelector(sel);
                if (el && el.CodeMirror) {
                    el.CodeMirror.setValue(txt);
                    el.CodeMirror.save();
                }
            }""",
            [selector, text],
        )


def create_and_exec_routine_human(page, name: str, sql_body: str, explain: str):
    page.goto(f"{MASTER_URL}/index.php?route=/database/routines&db={DB_NAME}")
    page.wait_for_load_state("networkidle")
    time.sleep(1.5)

    add_btn = page.locator("a", has_text=re.compile(r"Create new routine|Add routine", re.I)).first
    add_btn.click()
    page.locator("input[name='item_name']").wait_for(timeout=10000)
    time.sleep(1.0)

    # Ketik nama routine perlahan
    name_inp = page.locator("input[name='item_name']")
    name_inp.click()
    name_inp.type(name, delay=110)
    time.sleep(0.8)

    # Hapus parameter default
    drop_btn = page.locator("input.routine_param_remove, button.routine_param_remove, a.routine_param_remove")
    if drop_btn.count() > 0 and drop_btn.first.is_visible():
        drop_btn.first.click()
    else:
        page.evaluate("() => { document.querySelectorAll('.routine_params_table tbody tr').forEach(r => r.remove()); }")
    time.sleep(0.8)

    # Isi Definition SQL
    fill_codemirror_human(page, ".ui-dialog .CodeMirror", sql_body)
    wait_step(f"Membuat Routine {name}", explain, STEP_DELAY * 0.7)

    # Klik tombol Go pada modal dialog
    go_btn = page.locator(".ui-dialog-buttonset button", has_text="Go").first
    if go_btn.count() > 0:
        go_btn.click()
        time.sleep(2.0)

    # Klik Execute pada routine yang baru dibuat
    page.goto(f"{MASTER_URL}/index.php?route=/database/routines&db={DB_NAME}")
    page.wait_for_load_state("networkidle")
    time.sleep(1.0)
    row = page.locator("tr", has_text=name).first
    exec_btn = row.locator("a", has_text="Execute").first
    if exec_btn.count() > 0:
        exec_btn.click()
        page.wait_for_load_state("networkidle")
    wait_step(f"Hasil Eksekusi {name}", f"Menampilkan hasil SELECT setelah {name} dijalankan", STEP_DELAY * 0.8)

    # Buka tabel pasien untuk membuktikan perubahan data
    page.goto(f"{MASTER_URL}/index.php?route=/sql&db={DB_NAME}&table=pasien&pos=0")
    page.wait_for_load_state("networkidle")
    wait_step(f"Cek Tabel pasien Setelah {name}", explain, STEP_DELAY * 0.8)


def main():
    exe = find_browser_exe()
    with sync_playwright() as p:
        launch_args = {"headless": False, "args": ["--start-maximized"]}
        if exe:
            launch_args["executable_path"] = exe
        browser = p.chromium.launch(**launch_args)
        context = browser.new_context(no_viewport=True)
        page = context.new_page()

        # 1. Buka halaman utama phpMyAdmin & pilih database rumah_sakit
        page.goto(MASTER_URL)
        page.wait_for_load_state("networkidle")
        wait_step("Elemen 1: Perkenalan & Buka phpMyAdmin", "Perkenalkan Nama, NIM, Prodi Sistem Informasi UT, dan topik Tugas 3 Basis Data.")

        page.goto(f"{MASTER_URL}/index.php?route=/database/structure&db={DB_NAME}")
        page.wait_for_load_state("networkidle")
        wait_step("Struktur Database rumah_sakit (Hasil Tugas 2)", "Tunjukkan 6 tabel awal dengan Storage Engine InnoDB.")

        page.goto(f"{MASTER_URL}/index.php?route=/sql&db={DB_NAME}&table=pasien&pos=0")
        page.wait_for_load_state("networkidle")
        wait_step("Data Awal Tabel pasien", "Tunjukkan 5 baris data pasien awal (ID 1 s/d 5).")

        # 2. Buat & Jalankan transaksi1 s/d transaksi5
        create_and_exec_routine_human(
            page,
            "transaksi1",
            "BEGIN\nSTART TRANSACTION;\nINSERT INTO `pasien` (`id_pasien`, `nama_pasien`, `alamat_pasien`, `jenis_kelamin`)\nVALUES (6, 'Hanif', 'Jl. Babakan Loa No. 22', 'L');\nSELECT * FROM pasien;\nEND",
            "START TRANSACTION tanpa COMMIT: data Hanif (ID 6) hanya tampil sementara dan belum masuk permanen ke tabel pasien.",
        )

        create_and_exec_routine_human(
            page,
            "transaksi2",
            "BEGIN\nSTART TRANSACTION;\nINSERT INTO `pasien` (`id_pasien`, `nama_pasien`, `alamat_pasien`, `jenis_kelamin`)\nVALUES (6, 'Hanif', 'Jl. Babakan Loa No. 22', 'L');\nCOMMIT;\nSELECT * FROM pasien;\nEND",
            "START TRANSACTION dengan COMMIT: data Hanif (ID 6) kini tersimpan permanen di tabel pasien.",
        )

        create_and_exec_routine_human(
            page,
            "transaksi3",
            "BEGIN\nSTART TRANSACTION;\nUPDATE pasien SET nama_pasien = 'Septin' WHERE id_pasien = 3;\nROLLBACK;\nCOMMIT;\nSELECT * FROM pasien;\nEND",
            "Perintah ROLLBACK membatalkan UPDATE nama pasien ID 3 menjadi Septin (tetap Budi Raharjo).",
        )

        create_and_exec_routine_human(
            page,
            "transaksi4",
            "BEGIN\nSTART TRANSACTION;\nINSERT INTO `pasien` (`id_pasien`, `nama_pasien`, `alamat_pasien`, `jenis_kelamin`)\nVALUES (7, 'Rudi', 'Jl. Kebon Jeruk No. 14', 'L');\nROLLBACK;\nUPDATE pasien SET nama_pasien = 'Septin' WHERE id_pasien = 3;\nCOMMIT;\nSELECT * FROM pasien;\nEND",
            "Modifikasi ROLLBACK & COMMIT: INSERT ID 7 (Rudi) dibatalkan oleh ROLLBACK, sedangkan UPDATE ID 3 menjadi Septin disahkan oleh COMMIT.",
        )

        create_and_exec_routine_human(
            page,
            "transaksi5",
            "BEGIN\nSTART TRANSACTION;\nINSERT INTO `pasien` (`id_pasien`, `nama_pasien`, `alamat_pasien`, `jenis_kelamin`)\nVALUES (8, 'Dudung', 'Jl. Cimahi No. 11', 'L');\nSAVEPOINT point1;\nINSERT INTO `pasien` (`id_pasien`, `nama_pasien`, `alamat_pasien`, `jenis_kelamin`)\nVALUES (9, 'Maman', 'Jl. Garut No. 5', 'L');\nROLLBACK TO point1;\nINSERT INTO `pasien` (`id_pasien`, `nama_pasien`, `alamat_pasien`, `jenis_kelamin`)\nVALUES (10, 'Ujang', 'Jl. Tasikmalaya No. 9', 'L');\nCOMMIT;\nSELECT * FROM pasien;\nEND",
            "SAVEPOINT point1 & ROLLBACK TO point1: ID 8 (Dudung) dan ID 10 (Ujang) tersimpan, sedangkan ID 9 (Maman) batal masuk.",
        )

        # 3. Buat tabel obat & transaksi_obat beserta Foreign Key dan data awal obat
        page.goto(f"{MASTER_URL}/index.php?route=/database/sql&db={DB_NAME}")
        page.wait_for_load_state("networkidle")
        ddl = (
            "CREATE TABLE obat (\n"
            "  id_obat INT(6) NOT NULL AUTO_INCREMENT PRIMARY KEY,\n"
            "  kode_obat VARCHAR(5) NOT NULL,\n"
            "  nama_obat VARCHAR(30) NOT NULL,\n"
            "  harga INT(10) NOT NULL,\n"
            "  stok INT(5) NOT NULL\n"
            ") ENGINE=InnoDB;\n\n"
            "CREATE TABLE transaksi_obat (\n"
            "  id_transaksi INT(6) NOT NULL AUTO_INCREMENT PRIMARY KEY,\n"
            "  id_pasien INT(3) NOT NULL,\n"
            "  id_obat INT(6) NOT NULL,\n"
            "  jumlah INT(5) NOT NULL,\n"
            "  total_harga INT(10) NOT NULL,\n"
            "  INDEX (id_pasien),\n"
            "  INDEX (id_obat),\n"
            "  CONSTRAINT fk_to_pasien FOREIGN KEY (id_pasien) REFERENCES pasien(id_pasien) ON DELETE CASCADE ON UPDATE CASCADE,\n"
            "  CONSTRAINT fk_to_obat FOREIGN KEY (id_obat) REFERENCES obat(id_obat) ON DELETE CASCADE ON UPDATE CASCADE\n"
            ") ENGINE=InnoDB;\n\n"
            "INSERT INTO obat VALUES\n"
            "(1, 'A001', 'Paracetamol', 5000, 100),\n"
            "(2, 'A002', 'Amoxicillin', 10000, 50),\n"
            "(3, 'A003', 'Betadine', 15000, 100);"
        )
        fill_codemirror_human(page, "#sqlqueryform .CodeMirror", ddl)
        wait_step("Membuat Tabel obat & transaksi_obat + Relasi FK", "Menampilkan query pembuatan tabel obat, transaksi_obat, dan pengisian stok awal.")
        page.locator("#button_submit_query").click()
        time.sleep(2.0)

        page.goto(f"{MASTER_URL}/index.php?route=/table/relation&db={DB_NAME}&table=transaksi_obat")
        page.wait_for_load_state("networkidle")
        wait_step("Relasi Foreign Key CASCADE", "Menampilkan relasi id_pasien dan id_obat pada tabel transaksi_obat.")

        page.goto(f"{MASTER_URL}/index.php?route=/sql&db={DB_NAME}&table=obat&pos=0")
        page.wait_for_load_state("networkidle")
        wait_step("Data Stok Awal Tabel obat", "Paracetamol = 100, Amoxicillin = 50, Betadine = 100.")

        # 4. Buat Trigger tg_stok_obat
        page.goto(f"{MASTER_URL}/index.php?route=/database/triggers&db={DB_NAME}&table=transaksi_obat")
        page.wait_for_load_state("networkidle")
        time.sleep(1.0)
        page.locator("a", has_text=re.compile(r"Create new trigger|Add trigger", re.I)).first.click()
        page.locator("input[name='item_name']").wait_for(timeout=10000)
        page.locator("input[name='item_name']").type("tg_stok_obat", delay=100)
        page.locator("select[name='item_timing']").select_option("AFTER")
        page.locator("select[name='item_event']").select_option("INSERT")
        fill_codemirror_human(
            page,
            ".ui-dialog .CodeMirror",
            "UPDATE obat SET stok = stok - NEW.jumlah WHERE id_obat = NEW.id_obat",
        )
        wait_step("Membuat Trigger tg_stok_obat", "AFTER INSERT pada transaksi_obat untuk mengurangi stok obat otomatis.")
        page.locator(".ui-dialog-buttonset button", has_text="Go").first.click()
        time.sleep(2.0)

        # 5. Uji Insert transaksi_obat
        page.goto(f"{MASTER_URL}/index.php?route=/table/change&db={DB_NAME}&table=transaksi_obat")
        page.wait_for_load_state("networkidle")
        time.sleep(1.0)
        for col_name, val in [("id_transaksi", "1"), ("id_pasien", "6"), ("id_obat", "1"), ("jumlah", "15"), ("total_harga", "75000")]:
            row = page.locator("tr", has_text=col_name).first
            inp = row.locator("input[type='text'], input[type='number'], select").last
            if inp.count() > 0:
                tag = inp.evaluate("el => el.tagName.toLowerCase()")
                if tag == "select":
                    inp.select_option(val)
                else:
                    inp.fill(val)
        wait_step("Uji Trigger: Input Pembelian 15 Paracetamol", "Pasien ID 6 (Hanif) membeli 15 Paracetamol (id_obat = 1).")
        page.locator("input[value='Go']").last.click()
        time.sleep(2.0)

        page.goto(f"{MASTER_URL}/index.php?route=/sql&db={DB_NAME}&table=obat&pos=0")
        page.wait_for_load_state("networkidle")
        wait_step("Hasil Trigger tg_stok_obat", "Stok Paracetamol otomatis berkurang dari 100 menjadi 85.")

        # 6. Tampilkan Menu User Accounts & Replication untuk Tahap 2
        page.goto(f"{MASTER_URL}/index.php?route=/server/privileges&adduser=1")
        page.wait_for_load_state("networkidle")
        page.locator("input[name='username']").type("subhan", delay=100)
        if page.locator("select[name='pred_hostname']").count() > 0:
            page.locator("select[name='pred_hostname']").select_option("any")
        page.locator("input[name='pma_pw']").fill("1234")
        page.locator("input[name='pma_pw2']").fill("1234")
        for priv in ["Repl_client_priv", "Repl_slave_priv"]:
            cb = page.locator(f"input[name='{priv}']")
            if cb.count() > 0:
                cb.check()
        wait_step("Praktikum 2 (Replikasi): Membuat User Replikasi", "User 'subhan' dengan Host '%' dan hak akses Replication Client & Slave.")

        page.goto(f"{MASTER_URL}/index.php?route=/server/replication")
        page.wait_for_load_state("networkidle")
        wait_step("Menu Replication Master", "Tunjukkan status Primary Replication dan lanjutkan ke Ubuntu VirtualBox sesuai panduan.")

        input("\n>>> Selesai di sisi Master! Tekan [ENTER] untuk menutup jendela otomatisasi...")
        context.close()
        browser.close()


if __name__ == "__main__":
    main()
