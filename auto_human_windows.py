#!/usr/bin/env python3
"""
auto_human_windows.py
Menjalankan browser Chrome/Edge secara asli (non-headless) di atas Desktop Windows
dan menggerakkan KURSOR MOUSE ASLI WINDOWS (via Win32 API ctypes SetCursorPos
dengan lintasan kurva Bezier manusiawi + Fitts's Law ease-in-out) serta mengetik
karakter demi karakter dari langkah paling dasar:
- Membuka database rumah_sakit (hasil Tugas 2)
- Membuat routine transaksi1 s/d transaksi5 satu per satu dari nol
- Membuat tabel obat & transaksi_obat beserta relasi Foreign Key CASCADE
- Membuat trigger tg_stok_obat & menguji form Insert pembelian obat
- Membuka form pembuatan User Replikasi & status Primary Replication

Dapat dijalankan dalam:
1. Mode Tempo Pelan Otomatis (default jeda 15 detik per tahapan)
2. Mode Interaktif (`python auto_human_windows.py --interactive` -> menunggu tekan ENTER di tiap tahapan)
"""
import ctypes
import math
import os
import re
import sys
import time
from playwright.sync_api import sync_playwright

MASTER_URL = os.environ.get("MASTER_PMA_URL", "http://localhost/phpmyadmin")
DB_NAME = "rumah_sakit"
STEP_DELAY = float(os.environ.get("STEP_DELAY", "15.0"))
TYPE_DELAY_MS = int(os.environ.get("TYPE_DELAY_MS", "70"))
INTERACTIVE = "--interactive" in sys.argv
IS_WINDOWS = os.name == "nt"


class POINT(ctypes.Structure):
    _fields_ = [("x", ctypes.c_long), ("y", ctypes.c_long)]


def get_os_cursor_pos() -> tuple[int, int]:
    if IS_WINDOWS:
        pt = POINT()
        ctypes.windll.user32.GetCursorPos(ctypes.byref(pt))
        return pt.x, pt.y
    return 640, 360


def set_os_cursor_pos(x: int, y: int):
    if IS_WINDOWS:
        ctypes.windll.user32.SetCursorPos(int(x), int(y))


def ease_in_out(t: float) -> float:
    return 4 * t * t * t if t < 0.5 else 1 - pow(-2 * t + 2, 3) / 2


def move_mouse_human(page, target_x: float, target_y: float, duration: float = 0.65):
    """Menggerakkan kursor OS Windows asli & mouse Playwright secara halus mengikuti kurva Bezier."""
    start_x, start_y = get_os_cursor_pos()
    # Offset tinggi header Chrome (~85px di atas viewport pada layar Windows)
    screen_tx = int(target_x)
    screen_ty = int(target_y + (85 if IS_WINDOWS else 0))

    dx = screen_tx - start_x
    dy = screen_ty - start_y
    dist = math.hypot(dx, dy)
    arc = min(60.0, max(10.0, dist * 0.15))
    nx = -dy / (dist + 1e-5)
    ny = dx / (dist + 1e-5)

    p1 = (start_x + dx * 0.3 + nx * arc, start_y + dy * 0.3 + ny * arc)
    p2 = (start_x + dx * 0.7 + nx * (arc * 0.5), start_y + dy * 0.7 + ny * (arc * 0.5))

    steps = max(15, int(duration * 60))
    for i in range(steps + 1):
        t = ease_in_out(i / steps)
        u = 1.0 - t
        bx = u**3 * start_x + 3 * u**2 * t * p1[0] + 3 * u * t**2 * p2[0] + t**3 * screen_tx
        by = u**3 * start_y + 3 * u**2 * t * p1[1] + 3 * u * t**2 * p2[1] + t**3 * screen_ty
        set_os_cursor_pos(int(bx), int(by))
        time.sleep(duration / steps)

    try:
        page.mouse.move(target_x, target_y, steps=8)
    except Exception:
        pass


def move_and_click_human(page, locator, duration: float = 0.65):
    el = locator.first
    try:
        el.scroll_into_view_if_needed()
        box = el.bounding_box()
        if box:
            cx = box["x"] + box["width"] / 2
            cy = box["y"] + box["height"] / 2
            move_mouse_human(page, cx, cy, duration=duration)
            time.sleep(0.25)
    except Exception:
        pass
    el.click()


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
        move_and_click_human(page, cm)
        page.keyboard.press("Control+A")
        page.keyboard.press("Backspace")
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
    time.sleep(1.2)

    add_btn = page.locator("a", has_text=re.compile(r"Create new routine|Add routine", re.I)).first
    move_and_click_human(page, add_btn)
    page.locator("input[name='item_name']").wait_for(timeout=10000)
    time.sleep(0.8)

    name_inp = page.locator("input[name='item_name']")
    move_and_click_human(page, name_inp)
    name_inp.type(name, delay=95)
    time.sleep(0.6)

    drop_btn = page.locator("input.routine_param_remove, button.routine_param_remove, a.routine_param_remove")
    if drop_btn.count() > 0 and drop_btn.first.is_visible():
        move_and_click_human(page, drop_btn.first)
    else:
        page.evaluate("() => { document.querySelectorAll('.routine_params_table tbody tr').forEach(r => r.remove()); }")
    time.sleep(0.6)

    fill_codemirror_human(page, ".ui-dialog .CodeMirror", sql_body)
    wait_step(f"Membuat Routine {name}", explain, STEP_DELAY * 0.7)

    go_btn = page.locator(".ui-dialog-buttonset button", has_text="Go").first
    if go_btn.count() > 0:
        move_and_click_human(page, go_btn)
        time.sleep(1.8)

    page.goto(f"{MASTER_URL}/index.php?route=/database/routines&db={DB_NAME}")
    page.wait_for_load_state("networkidle")
    time.sleep(1.0)
    row = page.locator("tr", has_text=name).first
    exec_btn = row.locator("a", has_text="Execute").first
    if exec_btn.count() > 0:
        move_and_click_human(page, exec_btn)
        page.wait_for_load_state("networkidle")
    wait_step(f"Hasil Eksekusi {name}", f"Menampilkan hasil SELECT setelah {name} dijalankan", STEP_DELAY * 0.8)

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

        page.goto(MASTER_URL)
        page.wait_for_load_state("networkidle")
        wait_step("Elemen 1: Perkenalan & Buka phpMyAdmin", "Perkenalkan Nama, NIM, Prodi Sistem Informasi UT, dan topik Tugas 3 Basis Data.")

        page.goto(f"{MASTER_URL}/index.php?route=/database/structure&db={DB_NAME}")
        page.wait_for_load_state("networkidle")
        wait_step("Struktur Database rumah_sakit (Hasil Tugas 2)", "Tunjukkan 6 tabel awal dengan Storage Engine InnoDB.")

        page.goto(f"{MASTER_URL}/index.php?route=/sql&db={DB_NAME}&table=pasien&pos=0")
        page.wait_for_load_state("networkidle")
        wait_step("Data Awal Tabel pasien", "Tunjukkan 5 baris data pasien awal (ID 1 s/d 5).")

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
        move_and_click_human(page, page.locator("#button_submit_query"))
        time.sleep(2.0)

        page.goto(f"{MASTER_URL}/index.php?route=/table/relation&db={DB_NAME}&table=transaksi_obat")
        page.wait_for_load_state("networkidle")
        wait_step("Relasi Foreign Key CASCADE", "Menampilkan relasi id_pasien dan id_obat pada tabel transaksi_obat.")

        page.goto(f"{MASTER_URL}/index.php?route=/sql&db={DB_NAME}&table=obat&pos=0")
        page.wait_for_load_state("networkidle")
        wait_step("Data Stok Awal Tabel obat", "Paracetamol = 100, Amoxicillin = 50, Betadine = 100.")

        page.goto(f"{MASTER_URL}/index.php?route=/database/triggers&db={DB_NAME}&table=transaksi_obat")
        page.wait_for_load_state("networkidle")
        time.sleep(1.0)
        move_and_click_human(page, page.locator("a", has_text=re.compile(r"Create new trigger|Add trigger", re.I)))
        page.locator("input[name='item_name']").wait_for(timeout=10000)
        move_and_click_human(page, page.locator("input[name='item_name']"))
        page.locator("input[name='item_name']").type("tg_stok_obat", delay=95)
        page.locator("select[name='item_timing']").select_option("AFTER")
        page.locator("select[name='item_event']").select_option("INSERT")
        fill_codemirror_human(
            page,
            ".ui-dialog .CodeMirror",
            "UPDATE obat SET stok = stok - NEW.jumlah WHERE id_obat = NEW.id_obat",
        )
        wait_step("Membuat Trigger tg_stok_obat", "AFTER INSERT pada transaksi_obat untuk mengurangi stok obat otomatis.")
        move_and_click_human(page, page.locator(".ui-dialog-buttonset button", has_text="Go"))
        time.sleep(2.0)

        page.goto(f"{MASTER_URL}/index.php?route=/table/change&db={DB_NAME}&table=transaksi_obat")
        page.wait_for_load_state("networkidle")
        time.sleep(1.0)
        for col_name, val in [("id_transaksi", "1"), ("id_pasien", "6"), ("id_obat", "1"), ("jumlah", "15"), ("total_harga", "75000")]:
            row = page.locator("tr", has_text=col_name).first
            inp = row.locator("input[type='text'], input[type='number'], select").last
            if inp.count() > 0:
                move_and_click_human(page, inp, duration=0.45)
                tag = inp.evaluate("el => el.tagName.toLowerCase()")
                if tag == "select":
                    inp.select_option(val)
                else:
                    inp.fill(val)
        wait_step("Uji Trigger: Input Pembelian 15 Paracetamol", "Pasien ID 6 (Hanif) membeli 15 Paracetamol (id_obat = 1).")
        move_and_click_human(page, page.locator("input[value='Go']").last)
        time.sleep(2.0)

        page.goto(f"{MASTER_URL}/index.php?route=/sql&db={DB_NAME}&table=obat&pos=0")
        page.wait_for_load_state("networkidle")
        wait_step("Hasil Trigger tg_stok_obat", "Stok Paracetamol otomatis berkurang dari 100 menjadi 85.")

        page.goto(f"{MASTER_URL}/index.php?route=/server/privileges&adduser=1")
        page.wait_for_load_state("networkidle")
        move_and_click_human(page, page.locator("input[name='username']"))
        page.locator("input[name='username']").type("subhan", delay=95)
        if page.locator("select[name='pred_hostname']").count() > 0:
            page.locator("select[name='pred_hostname']").select_option("any")
        page.locator("input[name='pma_pw']").fill("1234")
        page.locator("input[name='pma_pw2']").fill("1234")
        for priv in ["Repl_client_priv", "Repl_slave_priv"]:
            cb = page.locator(f"input[name='{priv}']")
            if cb.count() > 0:
                move_and_click_human(page, cb, duration=0.4)
        wait_step("Praktikum 2 (Replikasi): Membuat User Replikasi", "User 'subhan' dengan Host '%' dan hak akses Replication Client & Slave.")

        page.goto(f"{MASTER_URL}/index.php?route=/server/replication")
        page.wait_for_load_state("networkidle")
        wait_step("Menu Replication Master", "Tunjukkan status Primary Replication dan lanjutkan ke Ubuntu VirtualBox sesuai panduan.")

        input("\n>>> Selesai di sisi Master! Tekan [ENTER] untuk menutup jendela otomatisasi...")
        context.close()
        browser.close()


if __name__ == "__main__":
    main()
