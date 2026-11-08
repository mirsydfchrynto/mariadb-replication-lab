#!/usr/bin/env python3
"""
record_live_human_practicum.py
Menghasilkan video praktikum real-time 24fps (BUKAN slideshow statis) dengan:
1. Kursor panah standar Windows 11 asli (aero_arrow) yang bergerak secara kontinu
   di setiap detik mengikuti kurva Bezier manusiawi (Fitts's Law ease-in-out +
   micro-jitter halus + efek klik natural).
2. Efek pengetikan bertahap (progressive typing) pada jendela pembuatan Routine,
   SQL Editor, Trigger, dan Form Insert.
3. Sinkronisasi penuh 39 adegan (termasuk yEd Graph Editor, XAMPP Control Panel
   Windows, Notepad my.ini, VirtualBox Host-Only Adapter, CMD ipconfig & ping,
   XAMPP Ubuntu & nano my.cnf, serta seluruh tahapan phpMyAdmin Master & Slave)
   dengan Voice-Over Bahasa Indonesia tanpa subtitle burn-in.
"""
import asyncio
import math
import os
import random
import subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

BASE_DIR = "/home/mirsydfchrynto/Documents/Tugas3-MSIM4206"
IMG_DIR = os.path.join(BASE_DIR, "screenshots_step_by_step")
AUDIO_39_DIR = "/tmp/subhan_39_audio"
EDGE_TTS = "/home/mirsydfchrynto/.local/bin/edge-tts"
FPS = 24
WIDTH, HEIGHT = 1280, 720

random.seed(42)


def make_win11_cursor_sprite() -> Image.Image:
    """Membuat sprite kursor panah standar Windows 11 (aero_arrow) resolusi tinggi (supersampled 4x)."""
    scale = 4
    w, h = 24 * scale, 32 * scale
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))

    # Bayangan lembut (drop shadow khas Windows 11)
    shadow = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    sdraw = ImageDraw.Draw(shadow)
    pts_shadow = [
        (2 * scale, 3 * scale),
        (2 * scale, 22 * scale),
        (6.8 * scale, 17.4 * scale),
        (10.0 * scale, 25.0 * scale),
        (12.8 * scale, 23.7 * scale),
        (9.5 * scale, 16.2 * scale),
        (16.2 * scale, 16.2 * scale),
    ]
    sdraw.polygon(pts_shadow, fill=(0, 0, 0, 95))
    shadow = shadow.filter(ImageFilter.GaussianBlur(radius=1.6 * scale))
    img.alpha_composite(shadow)

    # Badan panah putih bersih dengan garis tepi hitam tegas
    draw = ImageDraw.Draw(img)
    pts = [
        (1 * scale, 1 * scale),
        (1 * scale, 20 * scale),
        (5.8 * scale, 15.4 * scale),
        (9.0 * scale, 23.0 * scale),
        (11.8 * scale, 21.7 * scale),
        (8.5 * scale, 14.2 * scale),
        (15.2 * scale, 14.2 * scale),
    ]
    draw.polygon(pts, fill=(255, 255, 255, 255), outline=(15, 15, 15, 255), width=int(1.25 * scale))
    return img.resize((24, 32), Image.Resampling.LANCZOS)


def ease_in_out_cubic(t: float) -> float:
    return 4 * t * t * t if t < 0.5 else 1 - pow(-2 * t + 2, 3) / 2


def bezier_point(t: float, p0, p1, p2, p3) -> tuple[int, int]:
    u = 1.0 - t
    tt = t * t
    uu = u * u
    uuu = uu * u
    ttt = tt * t
    x = uuu * p0[0] + 3 * uu * t * p1[0] + 3 * u * tt * p2[0] + ttt * p3[0]
    y = uuu * p0[1] + 3 * uu * t * p1[1] + 3 * u * tt * p2[1] + ttt * p3[1]
    return int(round(x)), int(round(y))


def generate_human_cursor_path(waypoints: list[tuple[int, int]], total_frames: int) -> list[tuple[int, int, bool]]:
    """
    Menghasilkan posisi (x, y, is_clicking) untuk setiap frame (24fps)
    mengikuti kurva Bezier manusiawi antar titik fokus di layar.
    """
    if total_frames <= 0:
        return []
    if len(waypoints) < 2:
        wp = waypoints[0] if waypoints else (640, 360)
        return [(wp[0], wp[1], False) for _ in range(total_frames)]

    segs = len(waypoints) - 1
    base_frames = max(1, total_frames // segs)
    path = []

    for s_idx in range(segs):
        p0 = waypoints[s_idx]
        p3 = waypoints[s_idx + 1]
        frames_this = base_frames if s_idx < segs - 1 else (total_frames - len(path))
        if frames_this <= 0:
            continue

        # 55% waktu untuk menggerakkan mouse dengan kurva Bezier, 45% waktu hover/menunjuk natural
        move_frames = max(4, int(frames_this * 0.58))
        dwell_frames = max(0, frames_this - move_frames)

        dx = p3[0] - p0[0]
        dy = p3[1] - p0[1]
        dist = math.hypot(dx, dy)
        arc = min(65.0, max(12.0, dist * 0.14)) * (1 if s_idx % 2 == 0 else -1)
        nx = -dy / (dist + 1e-5)
        ny = dx / (dist + 1e-5)

        p1 = (p0[0] + dx * 0.30 + nx * arc, p0[1] + dy * 0.30 + ny * arc)
        p2 = (p0[0] + dx * 0.72 + nx * (arc * 0.5), p0[1] + dy * 0.72 + ny * (arc * 0.5))

        for f in range(move_frames):
            raw_t = f / max(1, move_frames - 1)
            et = ease_in_out_cubic(raw_t)
            bx, by = bezier_point(et, p0, p1, p2, p3)
            # Tambahkan micro-tremor tangan manusia (±1 px saat bergerak)
            jx = int(round(math.sin(f * 0.7 + s_idx) * 1.1)) if 0.1 < raw_t < 0.9 else 0
            jy = int(round(math.cos(f * 0.9 + s_idx) * 1.1)) if 0.1 < raw_t < 0.9 else 0
            path.append((max(2, min(WIDTH - 26, bx + jx)), max(2, min(HEIGHT - 34, by + jy)), False))

        for d in range(dwell_frames):
            # Saat menunjuk/membaca, tangan manusia bergeser sangat halus 1-2 px dan klik pada awal dwell terakhir
            is_click = (s_idx == segs - 1 and 2 <= d <= 5)
            ox = int(round(math.sin(d * 0.25) * 1.5))
            oy = int(round(math.cos(d * 0.20) * 1.0))
            path.append((max(2, min(WIDTH - 26, p3[0] + ox)), max(2, min(HEIGHT - 34, p3[1] + oy)), is_click))

    while len(path) < total_frames:
        last = path[-1]
        path.append((last[0], last[1], False))
    return path[:total_frames]


# Daftar lengkap 39 adegan berurutan + koordinat gerakan mouse fokus manusia di setiap layar
SCENES_39 = [
    (
        "00a_yed_graph_editor_erd.png",
        "Assalamualaikum warahmatullahi wabarakatuh. Perkenalkan nama saya Subhan Yoga Maulana, NIM 0 4 4 8 7 6 2 2 3, dari Program Studi Sistem Informasi Universitas Terbuka. Pada video ini saya akan mempraktikkan Tugas 3 Mata Kuliah Basis Data secara bertahap dari dasar. Pertama kita melihat rancangan skema relasi delapan tabel pada database rumah sakit yang telah dibuat menggunakan aplikasi yEd Graph Editor.",
        [(180, 120), (360, 110), (680, 110), (410, 290), (410, 460), (680, 450)],
    ),
    (
        "00b_xampp_control_panel_windows.png",
        "Selanjutnya pada XAMPP Control Panel di Windows, kita pastikan service Apache dan MySQL keduanya telah kita klik Start sehingga berstatus Running berwarna hijau pada port 80 dan 3306.",
        [(640, 520), (460, 260), (460, 292), (578, 292), (480, 445)],
    ),
    (
        "01_struktur_awal_tugas2.png",
        "Kemudian kita membuka browser ke localhost phpmyadmin dan memilih database rumah sakit hasil Tugas 2 yang terdiri dari enam tabel awal dengan storage engine InnoDB.",
        [(90, 305), (340, 225), (650, 225), (650, 310), (735, 105)],
    ),
    (
        "02_data_awal_pasien.png",
        "Kita periksa terlebih dahulu isi tabel pasien. Saat ini terdapat lima baris data pasien awal dengan ID pasien satu sampai dengan lima.",
        [(90, 480), (420, 445), (480, 545), (735, 55)],
    ),
    (
        "03_form_create_routine_transaksi1.png",
        "Kita mulai Praktikum Transaksi dengan membuka menu Routines lalu klik Create new routine. Kita beri nama transaksi satu, parameternya kita drop, lalu pada Definition kita ketik START TRANSACTION, INSERT pasien ID enam atas nama Hanif tanpa perintah COMMIT, diikuti SELECT bintang FROM pasien, lalu klik Go.",
        [(915, 220), (320, 185), (305, 345), (450, 450), (480, 520), (762, 955 if 955 < 700 else 692)],
    ),
    (
        "04_hasil_execute_transaksi1.png",
        "Setelah transaksi satu tersimpan, kita klik tombol Execute. Terlihat data pasien ID enam atas nama Hanif tampil sementara pada hasil eksekusi routine.",
        [(480, 620), (350, 490), (420, 490), (92, 480)],
    ),
    (
        "05_pasien_setelah_transaksi1_tetap_5.png",
        "Namun ketika kita klik kembali tabel pasien pada menu Browse, terlihat jumlah baris tetap lima dan data Hanif belum tersimpan secara permanen karena tidak ada perintah COMMIT.",
        [(92, 480), (430, 445), (430, 555), (735, 55)],
    ),
    (
        "06_form_create_routine_transaksi2.png",
        "Selanjutnya kita klik Create new routine untuk membuat routine kedua bernama transaksi dua. Kita hapus parameternya, lalu kita masukkan perintah yang sama namun ditambahkan perintah COMMIT sebelum SELECT bintang FROM pasien, lalu klik Go.",
        [(915, 220), (320, 185), (430, 465), (340, 505), (762, 692)],
    ),
    (
        "07_hasil_execute_transaksi2.png",
        "Kita klik Execute pada transaksi dua. Terlihat hasil query menampilkan enam baris data pasien termasuk Hanif.",
        [(480, 650), (350, 490), (450, 490), (92, 480)],
    ),
    (
        "08_pasien_setelah_transaksi2_masuk_hanif.png",
        "Saat kita periksa kembali tabel pasien, data ID pasien enam atas nama Hanif kini telah tersimpan secara permanen di dalam tabel pasien karena adanya perintah COMMIT.",
        [(92, 480), (420, 580), (540, 580), (735, 55)],
    ),
    (
        "09_form_create_routine_transaksi3.png",
        "Berikutnya kita membuat routine transaksi tiga untuk menguji perintah ROLLBACK. Pada Definition kita ketik START TRANSACTION, kemudian UPDATE pasien SET nama pasien sama dengan Septin WHERE id pasien sama dengan tiga, diikuti perintah ROLLBACK dan COMMIT.",
        [(915, 220), (320, 185), (420, 435), (350, 490), (762, 692)],
    ),
    (
        "10_hasil_execute_transaksi3.png",
        "Ketika transaksi tiga kita klik Execute, terlihat bahwa nama pasien pada ID tiga tetap Budi Raharjo dan batal berubah menjadi Septin karena dibatalkan oleh perintah ROLLBACK.",
        [(480, 660), (420, 410), (510, 410), (915, 220)],
    ),
    (
        "11_form_create_routine_transaksi4.png",
        "Selanjutnya sesuai Gambar sembilan belas pada modul praktikum, kita buat routine transaksi empat. Di sini kita melakukan INSERT pasien baru ID tujuh atas nama Rudi yang diikuti ROLLBACK, kemudian kita lakukan UPDATE nama pasien ID tiga menjadi Septin yang diikuti COMMIT.",
        [(915, 220), (320, 185), (430, 445), (360, 505), (360, 560), (762, 692)],
    ),
    (
        "12_hasil_execute_transaksi4.png",
        "Saat kita klik Execute pada transaksi empat, terlihat penambahan pasien ID tujuh atas nama Rudi dibatalkan oleh ROLLBACK, sedangkan perubahan nama ID pasien tiga menjadi Septin berhasil disimpan permanen oleh COMMIT.",
        [(480, 665), (410, 410), (460, 490), (915, 220)],
    ),
    (
        "13_form_create_routine_transaksi5.png",
        "Berikutnya kita membuat routine transaksi lima untuk mempraktikkan SAVEPOINT. Kita menyisipkan pasien ID delapan atas nama Dudung, kemudian membuat SAVEPOINT point satu. Setelah itu kita menyisipkan pasien ID sembilan atas nama Maman, namun kita batalkan ke titik point satu dengan perintah ROLLBACK TO point satu, lalu menyisipkan pasien ID sepuluh atas nama Ujang dan diakhiri COMMIT.",
        [(915, 220), (320, 185), (430, 440), (380, 475), (380, 535), (380, 585), (762, 692)],
    ),
    (
        "14_hasil_execute_transaksi5.png",
        "Setelah transaksi lima kita simpan dan klik Execute, hasil eksekusi menampilkan delapan baris data pasien.",
        [(480, 680), (410, 515), (410, 540), (92, 480)],
    ),
    (
        "15_pasien_setelah_transaksi5.png",
        "Ketika kita periksa tabel pasien pada menu Browse, terlihat jelas bahwa ID delapan atas nama Dudung dan ID sepuluh atas nama Ujang berhasil tersimpan permanen, sedangkan ID sembilan atas nama Maman batal masuk karena terkena ROLLBACK TO point satu.",
        [(92, 480), (420, 608), (420, 636), (315, 55)],
    ),
    (
        "16_create_table_obat_dan_transaksi_obat.png",
        "Tahap selanjutnya pada praktikum transaksi adalah pembuatan Trigger. Terlebih dahulu kita buka tab SQL pada database rumah sakit untuk membuat tabel obat dan tabel transaksi obat dengan storage engine InnoDB.",
        [(315, 55), (380, 240), (420, 410), (450, 540), (1165, 680)],
    ),
    (
        "17_relasi_foreign_key_transaksi_obat.png",
        "Setelah kedua tabel terbentuk, kita mengatur indeks dan menghubungkan relasi Foreign Key antara id pasien pada tabel pasien dan id obat pada tabel obat ke tabel transaksi obat dengan aturan ON DELETE CASCADE dan ON UPDATE CASCADE.",
        [(310, 95), (390, 290), (680, 290), (390, 345), (680, 345)],
    ),
    (
        "18_data_awal_tabel_obat.png",
        "Kemudian kita mengisi tiga data awal pada tabel obat, yaitu Paracetamol dengan stok seratus, Amoxicillin dengan stok lima puluh, dan Betadine dengan stok seratus.",
        [(92, 560), (480, 448), (618, 448), (618, 478), (618, 508), (905, 55)],
    ),
    (
        "19_form_create_trigger_tg_stok_obat.png",
        "Selanjutnya pada tabel transaksi obat, kita buka menu Triggers lalu klik Create new trigger. Kita beri nama tg stok obat, waktu AFTER, event INSERT, dan pada Definition kita ketik UPDATE obat SET stok sama dengan stok dikurangi NEW titik jumlah WHERE id obat sama dengan NEW titik id obat.",
        [(905, 55), (320, 185), (295, 295), (295, 345), (480, 405), (762, 692)],
    ),
    (
        "20_daftar_trigger_aktif.png",
        "Setelah kita klik Go, trigger tg stok obat dengan waktu AFTER dan event INSERT telah berhasil terdaftar aktif pada tabel transaksi obat.",
        [(762, 692), (245, 290), (435, 290), (508, 55)],
    ),
    (
        "21_form_insert_transaksi_obat_1.png",
        "Sekarang kita uji trigger tersebut dengan membuka menu Insert pada tabel transaksi obat. Kita isi id transaksi satu, id pasien enam yaitu Hanif, id obat satu yaitu Paracetamol, jumlah beli lima belas, dan total harga tujuh puluh lima ribu rupiah, lalu klik Go.",
        [(508, 55), (565, 268), (565, 312), (565, 355), (565, 405), (565, 445), (218, 502)],
    ),
    (
        "22_stok_obat_paracetamol_berkurang_85.png",
        "Ketika kita buka kembali tabel obat, terlihat stok Paracetamol yang semula seratus kini otomatis berkurang menjadi delapan puluh lima. Dengan demikian praktikum bagian pertama mengenai Transaksi dan Trigger telah berhasil.",
        [(92, 560), (485, 448), (618, 448), (460, 55)],
    ),
    (
        "23_form_add_user_replikasi.png",
        "Sekarang kita masuk ke bagian kedua yaitu Praktikum Basis Data Terdistribusi menggunakan Replikasi Master Slave dari Windows ke Linux Ubuntu di VirtualBox. Langkah pertama di phpMyAdmin Master Windows, kita buka menu User accounts lalu klik Add user account. Kita buat user bernama subhan dengan host persen atau any host, password satu dua tiga empat, serta mencentang hak akses Replication client dan Replication slave.",
        [(460, 55), (480, 305), (365, 372), (480, 445), (215, 882 if 882 < 700 else 685)],
    ),
    (
        "24b_notepad_my_ini_windows.png",
        "Langkah kedua, kita buka file my dot ini pada XAMPP Windows melalui tombol Config MySQL, lalu di bawah bagian mysqld kita tambahkan konfigurasi log bin sama dengan mysql bin, server id sama dengan satu, dan binlog do db sama dengan rumah sakit, serta memberi tanda pagar pada server id satu bawaan di bawahnya.",
        [(310, 62), (260, 315), (260, 342), (260, 368), (260, 650)],
    ),
    (
        "24_form_configure_primary_replication.png",
        "Setelah file my dot ini kita simpan dan service MySQL pada XAMPP Windows kita restart, pada menu Replication terlihat Primary replication telah aktif.",
        [(865, 55), (310, 265), (285, 295), (285, 322)],
    ),
    (
        "25_status_primary_replication_master.png",
        "Kita klik Show primary status untuk melihat posisi Binary Log pada server Master. Tercatat nama File adalah mysql bin 000001 dengan Position 328 yang akan kita gunakan pada konfigurasi Slave di Ubuntu.",
        [(285, 295), (280, 470), (350, 470), (555, 55)],
    ),
    (
        "26_export_database_rumah_sakit.png",
        "Selanjutnya kita buka menu Export pada database rumah sakit lalu klik tombol Export di bagian bawah untuk mengunduh file rumah sakit dot sql yang akan diimpor ke Ubuntu VirtualBox.",
        [(555, 55), (340, 295), (290, 455), (230, 665)],
    ),
    (
        "26b_virtualbox_network_host_only.png",
        "Sebelum beralih ke Ubuntu di VirtualBox, kita pastikan pada pengaturan Network mesin virtual Ubuntu di VirtualBox bahwa Adapter satu telah diatur menggunakan Host only Adapter dengan nama VirtualBox Host Only Ethernet Adapter.",
        [(110, 95), (350, 445), (560, 355), (560, 418), (682, 805 if 805 < 700 else 680)],
    ),
    (
        "26c_cmd_ipconfig_dan_ping_dua_arah.png",
        "Kemudian kita periksa alamat IP dan menguji koneksi jaringan dua arah. Pada Command Prompt Windows terlihat alamat IP Host adalah 192 168 56 1 dan hasil ping ke 192 168 56 101 berhasil tanpa paket yang hilang. Sebaliknya pada Terminal Ubuntu terlihat alamat IP adalah 192 168 56 101 dan hasil ping ke 192 168 56 1 juga berhasil tersambung.",
        [(240, 180), (320, 395), (280, 560), (760, 155), (760, 315)],
    ),
    (
        "26d_ubuntu_xampp_dan_my_cnf.png",
        "Selanjutnya di dalam sistem operasi Linux Ubuntu pada VirtualBox, kita jalankan XAMPP Linux versi 8 2 12 yang sama dengan versi Windows, lalu kita buka file garis miring opt garis miring lampp garis miring etc garis miring my dot cnf menggunakan nano. Di bawah mysqld kita beri tanda pagar pada server id satu, lalu menambahkan server id sama dengan dua dan replicate do db sama dengan rumah sakit, kemudian kita restart MySQL di XAMPP Ubuntu.",
        [(210, 395), (210, 488), (232, 572), (610, 515), (610, 542), (610, 568)],
    ),
    (
        "27_import_database_di_slave_ubuntu.png",
        "Berikutnya kita buka browser Firefox di Ubuntu menuju localhost phpmyadmin, membuat database rumah sakit, lalu pada menu Import kita pilih file rumah sakit dot sql hasil ekspor dari Windows tadi dan klik Go.",
        [(612, 55), (355, 655), (225, 690)],
    ),
    (
        "28_query_change_master_to_di_slave.png",
        "Setelah seluruh tabel masuk ke phpMyAdmin Ubuntu, kita buka tab SQL lalu mengetikkan perintah STOP SLAVE, CHANGE MASTER TO MASTER HOST 192 168 56 1, MASTER USER subhan, MASTER PASSWORD satu dua tiga empat, MASTER LOG FILE mysql bin 000001, dan MASTER LOG POS 328, diikuti perintah START SLAVE, lalu kita klik Go.",
        [(315, 55), (360, 225), (380, 310), (380, 365), (1165, 680)],
    ),
    (
        "29_status_slave_io_sql_yes.png",
        "Sekarang kita periksa status replikasi pada menu Replication di phpMyAdmin Ubuntu dengan mengklik See replica status table. Terlihat Master Host telah terhubung ke 192 168 56 1, serta parameter Slave IO Running bernilai Yes dan Slave SQL Running bernilai Yes.",
        [(785, 55), (535, 102), (570, 380), (570, 408), (520, 438)],
    ),
    (
        "30_insert_transaksi_2_di_master.png",
        "Untuk membuktikan replikasi basis data terdistribusi berjalan secara real time, kita kembali ke phpMyAdmin Master di Windows lalu menginput transaksi kedua pada tabel transaksi obat, yaitu pembelian Betadine dengan ID obat tiga sebanyak dua puluh lima buah oleh pasien ID delapan atas nama Dudung.",
        [(508, 55), (565, 268), (565, 312), (565, 355), (565, 405), (565, 445), (218, 502)],
    ),
    (
        "31_stok_betadine_master_75.png",
        "Pada tabel obat di server Master Windows, terlihat stok Betadine yang semula seratus kini telah berkurang menjadi tujuh puluh lima.",
        [(92, 560), (485, 508), (618, 508)],
    ),
    (
        "32_slave_transaksi_obat_tereplikasi.png",
        "Sekarang kita beralih ke phpMyAdmin Slave di Ubuntu lalu menekan tombol Refresh pada tabel transaksi obat. Terlihat data transaksi kedua yaitu pembelian dua puluh lima Betadine oleh pasien ID delapan otomatis muncul di Ubuntu tanpa kita menginput manual di Ubuntu.",
        [(92, 650), (528, 235), (450, 478), (585, 478)],
    ),
    (
        "33_slave_stok_betadine_75.png",
        "Dan ketika kita membuka tabel obat pada server Slave di Ubuntu, stok Betadine juga otomatis berkurang menjadi tujuh puluh lima, sama persis dengan server Master di Windows. Dengan demikian seluruh tahapan Praktikum Tugas 3 Mata Kuliah Basis Data mengenai Transaksi dan Basis Data Terdistribusi telah berhasil dilaksanakan. Terima kasih, wassalamualaikum warahmatullahi wabarakatuh.",
        [(92, 560), (485, 448), (618, 448), (485, 508), (618, 508)],
    ),
]


async def gen_tts_one(idx: int, text: str, out_mp3: str, sem: asyncio.Semaphore):
    async with sem:
        if os.path.exists(out_mp3) and os.path.getsize(out_mp3) > 1000:
            return
        proc = await asyncio.create_subprocess_exec(
            EDGE_TTS,
            "--voice",
            "id-ID-ArdiNeural",
            "--rate=+2%",
            "--text",
            text,
            "--write-media",
            out_mp3,
            stdout=asyncio.subprocess.DEVNULL,
            stderr=asyncio.subprocess.DEVNULL,
        )
        await proc.communicate()


async def ensure_all_39_tts():
    os.makedirs(AUDIO_39_DIR, exist_ok=True)
    sem = asyncio.Semaphore(6)
    await asyncio.gather(
        *[gen_tts_one(i, text, os.path.join(AUDIO_39_DIR, f"seg_{i:02d}.mp3"), sem) for i, (_, text, _) in enumerate(SCENES_39)]
    )


def get_dur(path: str) -> float:
    return float(
        subprocess.check_output(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", path],
            text=True,
        ).strip()
    )


def render_realtime_video():
    cursor_sprite = make_win11_cursor_sprite()
    aconcat = "/tmp/subhan_39_aconcat.txt"
    with open(aconcat, "w") as f:
        for i in range(len(SCENES_39)):
            f.write(f"file '{os.path.join(AUDIO_39_DIR, f'seg_{i:02d}.mp3')}'\n")

    out_vo_mp3 = os.path.join(BASE_DIR, "VO_BAHASA_INDONESIA_TUGAS3_SUBHAN_YOGA_MAULANA_044876223.mp3")
    subprocess.run(
        ["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", aconcat, "-c", "copy", out_vo_mp3],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    out_mp4 = os.path.join(BASE_DIR, "VIDEO_TUGAS3_SUBHAN_YOGA_MAULANA_044876223_BERSIH_TANPA_SUBTITLE.mp4")

    ff_proc = subprocess.Popen(
        [
            "ffmpeg",
            "-y",
            "-f",
            "rawvideo",
            "-vcodec",
            "rawvideo",
            "-pix_fmt",
            "rgb24",
            "-s",
            f"{WIDTH}x{HEIGHT}",
            "-r",
            str(FPS),
            "-i",
            "-",
            "-i",
            out_vo_mp3,
            "-c:v",
            "libx264",
            "-preset",
            "veryfast",
            "-crf",
            "20",
            "-pix_fmt",
            "yuv420p",
            "-c:a",
            "aac",
            "-b:a",
            "128k",
            "-shortest",
            out_mp4,
        ],
        stdin=subprocess.PIPE,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    last_pos = (640, 360)
    total_frames_written = 0

    for i, (img_name, _, waypoints) in enumerate(SCENES_39):
        mp3_path = os.path.join(AUDIO_39_DIR, f"seg_{i:02d}.mp3")
        dur = get_dur(mp3_path)
        n_frames = max(12, int(round(dur * FPS)))

        bg_rgb = Image.open(os.path.join(IMG_DIR, img_name)).convert("RGB")
        if bg_rgb.size != (WIDTH, HEIGHT):
            bg_rgb = bg_rgb.resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS)

        full_wps = [last_pos] + list(waypoints)
        last_pos = full_wps[-1]
        cursor_path = generate_human_cursor_path(full_wps, n_frames)

        ripple = Image.new("RGBA", (36, 36), (0, 0, 0, 0))
        ImageDraw.Draw(ripple).ellipse((2, 2, 34, 34), outline=(37, 99, 235, 165), width=2)

        for cx, cy, is_click in cursor_path:
            frame = bg_rgb.copy()
            if is_click:
                frame.paste(ripple, (max(0, cx - 16), max(0, cy - 16)), ripple)
            frame.paste(cursor_sprite, (cx, cy), cursor_sprite)
            ff_proc.stdin.write(frame.tobytes())
            total_frames_written += 1

        print(f"[ENCODED SCENE {i+1:02d}/39] {img_name} ({n_frames} frames @ {FPS}fps)")

    ff_proc.stdin.close()
    ff_proc.wait()
    print(f"[OK] Total frames: {total_frames_written} ({total_frames_written/FPS:.1f}s) -> {out_mp4}")


if __name__ == "__main__":
    asyncio.run(ensure_all_39_tts())
    render_realtime_video()
