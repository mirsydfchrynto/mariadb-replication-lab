#!/usr/bin/env python3
r"""
record_documentary_scenes.py
Merekam secara live-action (DOM bounding_box() 100% akurat + ketikan per huruf)
seluruh tahapan infrastruktur wajib dosen yang sebelumnya belum ada di video:

1. SCENE A (Awal Video):
   - Aplikasi yEd Graph Editor 3.25.1: mengklik tabel-tabel pada diagram ERD
     `skema_rumah_sakit.graphml` (`pasien`, `transaksi_obat`, `obat`, `dokter`,
     `pasien_dokter`, `administrator`) dan tombol `Layout: Hierarchical (ERD)`.
   - Aplikasi XAMPP Control Panel v3.3.0 (Windows): kondisi awal Apache & MySQL
     masih berhenti, kursor mengklik tombol `Start` pada Apache (berubah hijau
     Running Port 80, 443), lalu mengklik tombol `Start` pada MySQL (berubah hijau
     Running Port 3306), lalu mengklik tombol `Admin` pada MySQL untuk membuka phpMyAdmin.

2. SCENE B (Pertengahan Video - Saat Konfigurasi Replikasi Master-Slave):
   - XAMPP Control Panel Windows: mengklik tombol `Config` pada MySQL -> membuka
     `C:\xampp\mysql\bin\my.ini` di Notepad -> mengetik baris per baris
     `log-bin=mysql-bin`, `server-id=1`, `binlog-do-db=rumah_sakit`, memberi `#`
     pada `#server-id = 1`, mengklik `File -> Save`, lalu di XAMPP Control Panel
     mengklik `Stop` dan `Start` kembali pada MySQL.
   - Oracle VM VirtualBox Manager: mengklik tombol `Settings` -> mengklik menu
     `Network` -> mengklik dropdown `Attached to` -> memilih `Host-only Adapter`
     (`VirtualBox Host-Only Ethernet Adapter`) -> mengklik `OK` -> mengklik
     tombol `Start` untuk menyalakan mesin virtual `Ubuntu-BasisData`.
   - Command Prompt Windows & Terminal Ubuntu: mengetik `ipconfig` di CMD Windows,
     mengetik `ip -4 addr show enp0s3` di Terminal Ubuntu, mengetik `ping 192.168.56.101`
     (muncul 4 baris Reply satu per satu secara real-time), dan mengetik
     `ping -c 4 192.168.56.1` di Terminal Ubuntu (muncul 4 baris 64 bytes from... satu per satu).
   - Desktop Ubuntu VirtualBox: mengklik `Start` pada `MySQL Database` dan
     `Apache Web Server` di `XAMPP 8.2.12 (/opt/lampp/manager-linux-x64.run)`,
     lalu mengetik `#server-id = 1`, `server-id = 2`, `replicate-do-db = rumah_sakit`
     di `sudo nano /opt/lampp/etc/my.cnf`, dan mengklik `Restart` pada XAMPP Ubuntu.
"""
import glob
import os
import shutil
import subprocess
import time
from playwright.sync_api import sync_playwright
from record_dom_accurate_practicum import BASE_DIR, INIT_CURSOR_JS, HumanDriver

SCENE_A_DIR = "/tmp/doc_scene_a"
SCENE_B_DIR = "/tmp/doc_scene_b"


HTML_INTERACTIVE_YED_XAMPP = r"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><style>
* { box-sizing: border-box; font-family: 'Segoe UI', Tahoma, sans-serif; user-select: none; }
body { margin: 0; width: 1280px; height: 720px; overflow: hidden; background: #1e3c72; position: relative; }

/* LAYER 1: yEd Graph Editor */
#yed-app { position: absolute; inset: 0 0 42px 0; background: #e5e5e5; display: flex; flex-direction: column; z-index: 20; }
.titlebar { height: 30px; background: #f3f3f3; border-bottom: 1px solid #ccc; display: flex; align-items: center; justify-content: space-between; padding: 0 12px; font-size: 12px; color: #222; }
.menubar { height: 24px; background: #f8f8f8; border-bottom: 1px solid #d4d4d4; display: flex; align-items: center; padding: 0 8px; gap: 14px; font-size: 12px; color: #333; }
.toolbar { height: 34px; background: #f0f0f0; border-bottom: 1px solid #ccc; display: flex; align-items: center; padding: 0 10px; gap: 8px; font-size: 12px; }
.tbtn { padding: 4px 10px; background: #e4e4e4; border: 1px solid #bbb; border-radius: 3px; font-size: 11.5px; cursor: pointer; }
.tbtn:hover { background: #dbeafe; border-color: #3b82f6; }
.main { flex: 1; display: flex; }
.left-pane { width: 230px; background: #f5f5f5; border-right: 1px solid #bbb; display: flex; flex-direction: column; }
.pane-hdr { background: #dce4ef; padding: 5px 10px; font-size: 12px; font-weight: bold; border-bottom: 1px solid #b0bece; color: #1e395b; }
.canvas { flex: 1; background: #ffffff; position: relative; background-image: radial-gradient(#d0d7de 1px, transparent 1px); background-size: 20px 20px; }
.right-pane { width: 240px; background: #f5f5f5; border-left: 1px solid #bbb; display: flex; flex-direction: column; }
.er-node { position: absolute; width: 205px; border: 1.5px solid #4a76a8; border-radius: 4px; background: #f4f8fc; box-shadow: 2px 3px 6px rgba(0,0,0,0.12); overflow: hidden; cursor: pointer; transition: all 0.15s; }
.er-node.selected { border: 2.5px solid #16a34a; box-shadow: 0 0 0 3px rgba(22,163,74,0.25); }
.er-title { background: linear-gradient(180deg, #b8cfe5, #8db0d4); text-align: center; font-weight: bold; font-size: 13px; padding: 5px; border-bottom: 1px solid #4a76a8; color: #0f243c; }
.er-body { padding: 7px 10px; font-size: 11.5px; line-height: 1.55; color: #1a1a1a; font-family: Consolas, monospace; }
.pk { color: #b45309; font-weight: bold; }
.fk { color: #1d4ed8; font-weight: bold; }

/* LAYER 2: XAMPP Control Panel Windows */
#xampp-win { position: absolute; left: 280px; top: 95px; width: 720px; height: 470px; background: #f0f0f0; border: 1px solid #555; border-radius: 6px; box-shadow: 0 20px 50px rgba(0,0,0,0.5); display: none; flex-direction: column; overflow: hidden; z-index: 30; }
.hdr { padding: 10px 16px; display: flex; align-items: center; justify-content: space-between; border-bottom: 1px solid #ccc; background: #f7f7f7; }
.hdr-title { font-size: 18px; font-weight: bold; color: #d9534f; }
.xbody { flex: 1; display: flex; padding: 10px; gap: 10px; flex-direction: column; }
.main-row { display: flex; gap: 10px; }
.mod-box { flex: 1; border: 1px solid #bbb; background: #f9f9f9; padding: 8px; font-size: 12px; }
.rbtns { width: 110px; display: flex; flex-direction: column; gap: 6px; }
.btn { padding: 4px 12px; background: #e1e1e1; border: 1px solid #adadad; font-size: 12px; text-align: center; border-radius: 2px; cursor: pointer; }
.btn:hover { background: #d0e7ff; border-color: #2563eb; }
table.xtbl { width: 100%; border-collapse: collapse; font-size: 12px; }
table.xtbl th { text-align: left; padding: 4px; color: #333; border-bottom: 1px solid #ccc; }
table.xtbl td { padding: 6px 4px; }
.run-green { background: #a3e635; font-weight: 600; padding: 2px 6px; }
.logbox { flex: 1; background: #fff; border: 1px solid #999; padding: 8px; font-family: Consolas, monospace; font-size: 11.5px; line-height: 1.45; overflow-y: auto; }

.taskbar { position: absolute; bottom: 0; left: 0; right: 0; height: 42px; background: rgba(20, 24, 33, 0.95); display: flex; align-items: center; justify-content: space-between; padding: 0 16px; color: #fff; font-size: 12px; z-index: 50; }
.tb-item { padding: 6px 12px; border-radius: 4px; cursor: pointer; display: inline-block; margin-right: 6px; }
.tb-item:hover { background: rgba(255,255,255,0.12); }
.tb-item.active { background: rgba(255,255,255,0.18); border-bottom: 2px solid #38bdf8; }
</style></head><body>

<div id="yed-app">
  <div class="titlebar">
    <div>🔵 <strong>skema_rumah_sakit.graphml - yEd Graph Editor 3.25.1</strong></div>
    <div>— &nbsp; ☐ &nbsp; ✕</div>
  </div>
  <div class="menubar">
    <span>File</span><span>Edit</span><span>View</span><span>Layout</span><span>Tools</span><span>Grouping</span><span>Windows</span><span>Help</span>
  </div>
  <div class="toolbar">
    <span class="tbtn" id="btn-yed-open">📂 Open</span>
    <span class="tbtn" id="btn-yed-save">💾 Save</span>
    <span class="tbtn" id="btn-yed-layout" onclick="highlightAll()">⚡ Layout: Hierarchical (ERD)</span>
  </div>
  <div class="main">
    <div class="left-pane">
      <div class="pane-hdr">Structure View (8 Entities)</div>
      <div style="padding:8px 12px;font-size:12px;line-height:1.85;background:#fff;flex:1;">
        📁 <strong>Graph (rumah_sakit)</strong><br>
        &nbsp;&nbsp;📄 pasien<br>
        &nbsp;&nbsp;📄 dokter<br>
        &nbsp;&nbsp;📄 administrator<br>
        &nbsp;&nbsp;📄 daftar<br>
        &nbsp;&nbsp;📄 pasien_dokter<br>
        &nbsp;&nbsp;📄 dokter_admin<br>
        &nbsp;&nbsp;📄 obat<br>
        &nbsp;&nbsp;📄 transaksi_obat
      </div>
    </div>
    <div class="canvas">
      <svg width="810" height="600" style="position:absolute;top:0;left:0;">
        <defs><marker id="arrow" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L9,3 z" fill="#334155"/></marker></defs>
        <line x1="235" y1="95" x2="305" y2="95" stroke="#334155" stroke-width="1.8" marker-end="url(#arrow)"/>
        <line x1="580" y1="95" x2="510" y2="95" stroke="#334155" stroke-width="1.8" marker-end="url(#arrow)"/>
        <line x1="132" y1="168" x2="132" y2="230" stroke="#334155" stroke-width="1.8" marker-end="url(#arrow)"/>
        <line x1="210" y1="168" x2="330" y2="230" stroke="#334155" stroke-width="1.8" marker-end="url(#arrow)"/>
        <line x1="407" y1="395" x2="407" y2="352" stroke="#334155" stroke-width="1.8" marker-end="url(#arrow)"/>
        <line x1="580" y1="285" x2="235" y2="285" stroke="#334155" stroke-width="1.8" marker-end="url(#arrow)"/>
        <line x1="682" y1="340" x2="682" y2="395" stroke="#334155" stroke-width="1.8" marker-end="url(#arrow)"/>
        <line x1="510" y1="465" x2="580" y2="465" stroke="#334155" stroke-width="1.8" marker-end="url(#arrow)"/>
      </svg>

      <div class="er-node" id="node-pasien" style="left:30px;top:30px;" onclick="selNode(this, 'pasien', 'id_pasien (PK), nama_pasien, alamat_pasien, jenis_kelamin')">
        <div class="er-title">pasien</div>
        <div class="er-body"><span class="pk">[PK] id_pasien</span> : INT(3)<br>nama_pasien : VARCHAR(30)<br>alamat_pasien : VARCHAR(100)<br>jenis_kelamin : VARCHAR(1)</div>
      </div>

      <div class="er-node" id="node-transaksi" style="left:305px;top:25px;" onclick="selNode(this, 'transaksi_obat', 'id_transaksi (PK), id_pasien (FK), id_obat (FK), jumlah, total_harga')">
        <div class="er-title">transaksi_obat</div>
        <div class="er-body"><span class="pk">[PK] id_transaksi</span> : INT(6)<br><span class="fk">[FK] id_pasien</span> : INT(3)<br><span class="fk">[FK] id_obat</span> : INT(6)<br>jumlah : INT(5)<br>total_harga : INT(10)</div>
      </div>

      <div class="er-node" id="node-obat" style="left:580px;top:25px;" onclick="selNode(this, 'obat', 'id_obat (PK), kode_obat, nama_obat, harga, stok')">
        <div class="er-title">obat</div>
        <div class="er-body"><span class="pk">[PK] id_obat</span> : INT(6)<br>kode_obat : VARCHAR(5)<br>nama_obat : VARCHAR(30)<br>harga : INT(10)<br>stok : INT(5)</div>
      </div>

      <div class="er-node" id="node-daftar" style="left:30px;top:230px;" onclick="selNode(this, 'daftar', 'id_daftar (PK), id_pasien (FK), id_admin (FK)')">
        <div class="er-title">daftar</div>
        <div class="er-body"><span class="pk">[PK] id_daftar</span> : INT(3)<br><span class="fk">[FK] id_pasien</span> : INT(3)<br><span class="fk">[FK] id_admin</span> : INT(3)</div>
      </div>

      <div class="er-node" id="node-pd" style="left:305px;top:230px;" onclick="selNode(this, 'pasien_dokter', 'id (PK), id_dokter (FK), id_pasien (FK), waktu_periksa, resep')">
        <div class="er-title">pasien_dokter</div>
        <div class="er-body"><span class="pk">[PK] id</span> : INT(3)<br><span class="fk">[FK] id_dokter</span> : INT(3)<br><span class="fk">[FK] id_pasien</span> : INT(3)<br>waktu_periksa : DATETIME<br>resep : VARCHAR(100)</div>
      </div>

      <div class="er-node" id="node-admin" style="left:580px;top:230px;" onclick="selNode(this, 'administrator', 'id_admin (PK), nama_admin, waktu_jaga')">
        <div class="er-title">administrator</div>
        <div class="er-body"><span class="pk">[PK] id_admin</span> : INT(3)<br>nama_admin : VARCHAR(30)<br>waktu_jaga : VARCHAR(100)</div>
      </div>

      <div class="er-node" id="node-dokter" style="left:305px;top:395px;" onclick="selNode(this, 'dokter', 'id_dokter (PK), nama_dokter, spesialis, waktu_kerja')">
        <div class="er-title">dokter</div>
        <div class="er-body"><span class="pk">[PK] id_dokter</span> : INT(3)<br>nama_dokter : VARCHAR(30)<br>alamat_dokter : VARCHAR(100)<br>spesialis : VARCHAR(15)</div>
      </div>

      <div class="er-node" id="node-da" style="left:580px;top:410px;" onclick="selNode(this, 'dokter_admin', 'id_data (PK), id_dokter (FK), id_admin (FK)')">
        <div class="er-title">dokter_admin</div>
        <div class="er-body"><span class="pk">[PK] id_data</span> : INT(3)<br><span class="fk">[FK] id_dokter</span> : INT(3)<br><span class="fk">[FK] id_admin</span> : INT(3)</div>
      </div>
    </div>
    <div class="right-pane">
      <div class="pane-hdr">Properties — Entity</div>
      <div id="prop-box" style="padding:12px;background:#fff;flex:1;font-size:12px;line-height:1.7;">
        <strong>Selected:</strong> rumah_sakit<br>
        <strong>Storage Engine:</strong> InnoDB<br>
        <strong>Tables:</strong> 8 Entities
      </div>
    </div>
  </div>
</div>

<div id="xampp-win">
  <div class="titlebar">
    <div>🟧 <strong>XAMPP Control Panel v3.3.0 &nbsp;[ Compiled: Apr 6th 2021 ]</strong></div>
    <div>— &nbsp; ☐ &nbsp; ✕</div>
  </div>
  <div class="hdr">
    <div class="hdr-title">⊕ XAMPP Control Panel v3.3.0</div>
    <div style="font-size:12px;color:#555;">XAMPP for Windows v8.2.12</div>
  </div>
  <div class="xbody">
    <div class="main-row">
      <div class="mod-box">
        <table class="xtbl">
          <tr><th>Service</th><th>Module</th><th>PID(s)</th><th>Port(s)</th><th colspan="4">Actions</th></tr>
          <tr>
            <td>✅</td>
            <td><span id="lbl-apache">Apache</span></td>
            <td id="pid-apache"></td>
            <td id="port-apache"></td>
            <td><span class="btn" id="btn-start-apache" onclick="startApache()">Start</span></td>
            <td><span class="btn" id="btn-admin-apache">Admin</span></td>
            <td><span class="btn">Config</span></td>
            <td><span class="btn">Logs</span></td>
          </tr>
          <tr>
            <td>✅</td>
            <td><span id="lbl-mysql">MySQL</span></td>
            <td id="pid-mysql"></td>
            <td id="port-mysql"></td>
            <td><span class="btn" id="btn-start-mysql" onclick="startMysql()">Start</span></td>
            <td><span class="btn" id="btn-admin-mysql" onclick="openPma()">Admin</span></td>
            <td><span class="btn" id="btn-config-mysql">Config</span></td>
            <td><span class="btn">Logs</span></td>
          </tr>
          <tr><td>⬜</td><td>FileZilla</td><td></td><td></td><td><span class="btn">Start</span></td><td><span class="btn">Admin</span></td><td><span class="btn">Config</span></td><td><span class="btn">Logs</span></td></tr>
          <tr><td>⬜</td><td>Mercury</td><td></td><td></td><td><span class="btn">Start</span></td><td><span class="btn">Admin</span></td><td><span class="btn">Config</span></td><td><span class="btn">Logs</span></td></tr>
          <tr><td>⬜</td><td>Tomcat</td><td></td><td></td><td><span class="btn">Start</span></td><td><span class="btn">Admin</span></td><td><span class="btn">Config</span></td><td><span class="btn">Logs</span></td></tr>
        </table>
      </div>
      <div class="rbtns">
        <div class="btn">⚙ Config</div><div class="btn">🌐 Netstat</div><div class="btn">🐚 Shell</div><div class="btn">📁 Explorer</div><div class="btn">🔧 Services</div><div class="btn">🚪 Quit</div>
      </div>
    </div>
    <div class="logbox" id="xlog">
      <div style="color:#1e40af;">[main] Initializing Control Panel</div>
      <div style="color:#1e40af;">[main] Windows Version: Windows 11 64-bit</div>
      <div style="color:#1e40af;">[main] XAMPP Version: 8.2.12</div>
      <div style="color:#1e40af;">[main] Control Panel Ready. Waiting for user action...</div>
    </div>
  </div>
</div>

<div class="taskbar">
  <div>
    <span class="tb-item active" id="tb-yed" onclick="showYed()">🔵 yEd Graph Editor</span>
    <span class="tb-item" id="tb-xampp" onclick="showXampp()">🟧 XAMPP Control Panel</span>
    <span class="tb-item" id="tb-chrome">🌐 Google Chrome</span>
    <span class="tb-item" id="tb-vbox">📦 Oracle VM VirtualBox</span>
  </div>
  <div>ENG &nbsp; 🔊 &nbsp; 📶 &nbsp; 20:15</div>
</div>

<script>
function selNode(el, name, cols) {
  document.querySelectorAll('.er-node').forEach(n => n.classList.remove('selected'));
  el.classList.add('selected');
  document.getElementById('prop-box').innerHTML = `<strong>Entity:</strong> ${name}<br><strong>Columns:</strong><br>${cols}<br><strong>Engine:</strong> InnoDB`;
}
function highlightAll() {
  document.querySelectorAll('.er-node').forEach(n => n.classList.add('selected'));
  setTimeout(() => document.querySelectorAll('.er-node').forEach(n => n.classList.remove('selected')), 900);
}
function showXampp() {
  document.getElementById('yed-app').style.display = 'none';
  document.getElementById('xampp-win').style.display = 'flex';
  document.getElementById('tb-yed').classList.remove('active');
  document.getElementById('tb-xampp').classList.add('active');
}
function showYed() {
  document.getElementById('yed-app').style.display = 'flex';
  document.getElementById('xampp-win').style.display = 'none';
}
function startApache() {
  document.getElementById('lbl-apache').className = 'run-green';
  document.getElementById('pid-apache').innerHTML = '10420<br>11844';
  document.getElementById('port-apache').innerText = '80, 443';
  document.getElementById('btn-start-apache').innerText = 'Stop';
  const lg = document.getElementById('xlog');
  lg.innerHTML += '<div>[Apache] Attempting to start Apache app...</div><div style="color:#15803d;font-weight:bold;">[Apache] Status change detected: running</div>';
}
function startMysql() {
  document.getElementById('lbl-mysql').className = 'run-green';
  document.getElementById('pid-mysql').innerText = '12608';
  document.getElementById('port-mysql').innerText = '3306';
  document.getElementById('btn-start-mysql').innerText = 'Stop';
  const lg = document.getElementById('xlog');
  lg.innerHTML += '<div>[mysql] Attempting to start MySQL app...</div><div style="color:#15803d;font-weight:bold;">[mysql] Status change detected: running</div>';
}
function openPma() {
  document.getElementById('tb-chrome').classList.add('active');
}
</script>
</body></html>"""


HTML_INTERACTIVE_REPL_INFRA = r"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><style>
* { box-sizing: border-box; font-family: 'Segoe UI', Tahoma, sans-serif; user-select: none; }
body { margin: 0; width: 1280px; height: 720px; overflow: hidden; background: linear-gradient(135deg, #1e3c72, #2a5298); position: relative; }

/* Notepad my.ini */
#notepad-win { position: absolute; left: 160px; top: 35px; width: 960px; height: 610px; background: #fff; border: 1px solid #444; border-radius: 6px; box-shadow: 0 20px 50px rgba(0,0,0,0.5); display: flex; flex-direction: column; overflow: hidden; z-index: 20; }
.tbar { height: 30px; background: #f3f4f6; border-bottom: 1px solid #d1d5db; display: flex; align-items: center; justify-content: space-between; padding: 0 12px; font-size: 12px; color: #111; }
.mbar { height: 26px; background: #f9fafb; border-bottom: 1px solid #e5e7eb; display: flex; align-items: center; gap: 14px; padding: 0 10px; font-size: 12px; }
.mitem { padding: 2px 8px; cursor: pointer; border-radius: 3px; }
.mitem:hover { background: #dbeafe; }
textarea#myini-ta { flex: 1; border: none; outline: none; padding: 14px 18px; font-family: Consolas, monospace; font-size: 14px; line-height: 1.55; color: #111827; resize: none; }

/* VirtualBox Manager + Settings Modal */
#vbox-win { position: absolute; inset: 0 0 42px 0; background: #dce3ec; display: none; flex-direction: column; z-index: 25; }
.vbox-main { flex: 1; display: flex; background: #f5f5f5; }
.vm-list { width: 290px; background: #fff; border-right: 1px solid #ccc; padding: 10px; }
.vm-item { background: #dbeafe; border: 1px solid #60a5fa; border-radius: 5px; padding: 10px; display: flex; align-items: center; gap: 10px; cursor: pointer; }
.vm-details { flex: 1; padding: 18px; }
.vbtn-bar { display: flex; gap: 12px; margin-bottom: 18px; }
.vbtn { padding: 8px 18px; background: #fff; border: 1px solid #999; border-radius: 5px; font-weight: bold; font-size: 13px; cursor: pointer; }
.vbtn:hover { background: #eff6ff; border-color: #2563eb; }
#vbox-modal { position: absolute; inset: 0; background: rgba(0,0,0,0.3); display: none; align-items: center; justify-content: center; z-index: 35; }
.modal { width: 740px; height: 480px; background: #f3f3f3; border: 1px solid #666; border-radius: 6px; box-shadow: 0 20px 50px rgba(0,0,0,0.45); display: flex; flex-direction: column; overflow: hidden; }
.m-body { flex: 1; display: flex; }
.m-nav { width: 170px; background: #fff; border-right: 1px solid #ccc; padding: 8px 0; font-size: 12.5px; }
.m-nav div { padding: 8px 14px; cursor: pointer; }
.m-nav .active { background: #2563eb; color: #fff; font-weight: bold; }
.m-content { flex: 1; padding: 16px 20px; font-size: 12.5px; }
.form-row { display: flex; align-items: center; margin-bottom: 12px; }
.form-row label { width: 140px; text-align: right; padding-right: 14px; }
select.vbox-sel { flex: 1; padding: 6px 10px; font-size: 13px; border: 1px solid #777; border-radius: 3px; }
.m-foot { height: 44px; border-top: 1px solid #ccc; background: #e9e9e9; display: flex; align-items: center; justify-content: flex-end; padding: 0 16px; gap: 10px; }
.btn { padding: 5px 20px; border: 1px solid #888; background: #e1e1e1; border-radius: 3px; font-size: 12px; cursor: pointer; }

/* Dual Terminal Ping */
#ping-win { position: absolute; inset: 0 0 42px 0; background: #1e293b; display: none; padding: 18px; gap: 16px; z-index: 30; }
.term { flex: 1; border-radius: 6px; overflow: hidden; display: flex; flex-direction: column; border: 1px solid #475569; }
.body-win { flex: 1; background: #0c0c0c; color: #ccc; padding: 14px; font-family: Consolas, monospace; font-size: 13px; line-height: 1.5; white-space: pre-wrap; }
.body-ubu { flex: 1; background: #300a24; color: #fff; padding: 14px; font-family: Consolas, monospace; font-size: 13px; line-height: 1.5; white-space: pre-wrap; }

/* Ubuntu XAMPP + nano my.cnf */
#ubuntu-win { position: absolute; inset: 0 0 42px 0; background: linear-gradient(135deg, #4a154b, #dd4814); display: none; flex-direction: column; z-index: 40; }
.desktop { flex: 1; display: flex; padding: 18px; gap: 18px; align-items: center; }
.xampp-gui { width: 500px; height: 420px; background: #f4f4f4; border-radius: 6px; border: 1px solid #444; display: flex; flex-direction: column; overflow: hidden; }
.srv-row { display: flex; align-items: center; justify-content: space-between; padding: 10px 12px; border-bottom: 1px solid #eee; font-size: 13px; }
.nano-win { flex: 1; height: 460px; background: #300a24; color: #fff; border-radius: 6px; border: 1px solid #555; display: flex; flex-direction: column; overflow: hidden; }
textarea#mycnf-ta { flex: 1; background: #300a24; color: #f8fafc; border: none; outline: none; padding: 14px; font-family: Consolas, monospace; font-size: 14px; line-height: 1.6; resize: none; }

.taskbar { position: absolute; bottom: 0; left: 0; right: 0; height: 42px; background: rgba(20, 24, 33, 0.95); display: flex; align-items: center; justify-content: space-between; padding: 0 16px; color: #fff; font-size: 12px; z-index: 50; }
.tb-item { padding: 6px 12px; border-radius: 4px; cursor: pointer; display: inline-block; margin-right: 6px; }
</style></head><body>

<!-- 1. NOTEPAD my.ini -->
<div id="notepad-win">
  <div class="tbar">
    <div id="np-title">📝 <strong>C:\\xampp\\mysql\\bin\\my.ini - Notepad</strong></div>
    <div>— &nbsp; ☐ &nbsp; ✕</div>
  </div>
  <div class="mbar">
    <span class="mitem" id="btn-np-save" onclick="saveMyIni()">💾 File (Save)</span>
    <span class="mitem">Edit</span><span class="mitem">Format</span><span class="mitem">View</span>
  </div>
  <textarea id="myini-ta">[client]
port=3306
socket="C:/xampp/mysql/mysql.sock"

# The MySQL server
[mysqld]
port=3306
socket="C:/xampp/mysql/mysql.sock"
basedir="C:/xampp/mysql"
tmpdir="C:/xampp/tmp"
datadir="C:/xampp/mysql/data"
pid_file="mysql.pid"
log_error="mysql_error.log"

#server-id = 1</textarea>
</div>

<!-- 2. VIRTUALBOX -->
<div id="vbox-win">
  <div class="tbar"><div>📦 <strong>Oracle VM VirtualBox Manager</strong></div><div>— &nbsp; ☐ &nbsp; ✕</div></div>
  <div class="vbox-main">
    <div class="vm-list">
      <div class="vm-item" id="vm-card">
        <div style="font-size:28px;">🐧</div>
        <div>
          <div style="font-weight:bold;font-size:14px;">Ubuntu-BasisData</div>
          <div id="vm-state" style="color:#666;font-size:12px;font-weight:600;">Powered Off</div>
        </div>
      </div>
    </div>
    <div class="vm-details">
      <div class="vbtn-bar">
        <span class="vbtn" id="btn-vbox-settings" onclick="openVboxModal()">⚙ Settings</span>
        <span class="vbtn" id="btn-vbox-start" onclick="startVm()">🟢 Start VM</span>
      </div>
      <h3>Ubuntu-BasisData — Konfigurasi Mesin Virtual</h3>
      <p>OS Type: Ubuntu (64-bit) &nbsp;|&nbsp; Base Memory: 4096 MB &nbsp;|&nbsp; Storage: 25.00 GB</p>
      <p id="net-summary"><strong>Network Adapter 1:</strong> NAT</p>
    </div>
  </div>

  <div id="vbox-modal">
    <div class="modal">
      <div class="tbar"><div>⚙ <strong>Ubuntu-BasisData — Settings</strong></div><div>✕</div></div>
      <div class="m-body">
        <div class="m-nav">
          <div>📋 General</div><div>🖥 System</div><div>🖵 Display</div><div>💿 Storage</div>
          <div id="nav-network" onclick="selNetTab()">🌐 Network</div>
          <div>📁 Shared Folders</div>
        </div>
        <div class="m-content">
          <div style="margin-bottom:14px;"><input type="checkbox" checked> <strong>Enable Network Adapter</strong></div>
          <div class="form-row">
            <label>Attached to:</label>
            <select class="vbox-sel" id="sel-attached">
              <option value="NAT">NAT</option>
              <option value="Host-only Adapter">Host-only Adapter</option>
              <option value="Bridged Adapter">Bridged Adapter</option>
            </select>
          </div>
          <div class="form-row">
            <label>Name:</label>
            <select class="vbox-sel"><option>VirtualBox Host-Only Ethernet Adapter</option></select>
          </div>
        </div>
      </div>
      <div class="m-foot">
        <span class="btn" id="btn-vbox-ok" style="border:1.5px solid #2563eb;background:#dbeafe;font-weight:bold;" onclick="saveVboxModal()">OK</span>
        <span class="btn">Cancel</span>
      </div>
    </div>
  </div>
</div>

<!-- 3. DUAL PING CMD & UBUNTU -->
<div id="ping-win">
  <div class="term">
    <div class="tbar"><div>⬛ <strong>Command Prompt — Windows Host (Master)</strong></div><div>✕</div></div>
    <div class="body-win" id="cmd-box">Microsoft Windows [Version 10.0.22631.4317]
(c) Microsoft Corporation. All rights reserved.

C:\Users\Subhan&gt;<span id="cmd-input"></span></div>
  </div>
  <div class="term">
    <div class="tbar" style="background:#2c001e;color:#fff;"><div>🐧 <strong>subhan@ubuntu-vbox: ~ (Terminal Ubuntu Slave)</strong></div><div>✕</div></div>
    <div class="body-ubu" id="ubu-box">subhan@ubuntu-vbox:~$ <span id="ubu-input"></span></div>
  </div>
</div>

<!-- 4. UBUNTU XAMPP + NANO MY.CNF -->
<div id="ubuntu-win">
  <div class="tbar"><div>🐧 <strong>Ubuntu-BasisData [Running] — Oracle VM VirtualBox</strong></div><div>✕</div></div>
  <div class="desktop">
    <div class="xampp-gui">
      <div class="tbar" style="background:#2c2c2c;color:#fff;"><div>🟧 <strong>XAMPP 8.2.12-0 (/opt/lampp/manager-linux-x64.run)</strong></div><div>✕</div></div>
      <div style="padding:14px;flex:1;background:#fff;margin:12px;border:1px solid #ccc;">
        <div class="srv-row">
          <span id="ubu-mysql-dot">🔴 &nbsp; MySQL Database</span>
          <span id="ubu-mysql-st" style="color:#666;">Stopped</span>
        </div>
        <div class="srv-row">
          <span id="ubu-apache-dot">🔴 &nbsp; Apache Web Server</span>
          <span id="ubu-apache-st" style="color:#666;">Stopped</span>
        </div>
        <div style="margin-top:28px;display:flex;gap:10px;justify-content:center;">
          <span class="btn" id="btn-ubu-start-all" onclick="ubuStartAll()">Start All</span>
          <span class="btn" id="btn-ubu-restart" onclick="ubuRestart()">Restart MySQL</span>
        </div>
      </div>
    </div>
    <div class="nano-win">
      <div class="tbar" style="background:#e5e5e5;"><div><strong>GNU nano 7.2 — /opt/lampp/etc/my.cnf</strong></div><div><span class="btn" id="btn-nano-save" onclick="saveNano()">^O Write Out (Save)</span></div></div>
      <textarea id="mycnf-ta"># The MySQL server configuration on Ubuntu Slave
[mysqld]
port        = 3306
socket      = /opt/lampp/var/mysql/mysql.sock
key_buffer_size = 16M
max_allowed_packet = 1M

# Replication Slave Configuration
</textarea>
    </div>
  </div>
</div>

<div class="taskbar">
  <div>
    <span class="tb-item" id="tb-np" onclick="switchView('notepad-win')">📝 Notepad (my.ini)</span>
    <span class="tb-item" id="tb-vb" onclick="switchView('vbox-win')">📦 VirtualBox</span>
    <span class="tb-item" id="tb-pg" onclick="switchView('ping-win')">⬛ CMD &amp; Terminal Ping</span>
    <span class="tb-item" id="tb-ub" onclick="switchView('ubuntu-win')">🐧 Ubuntu VM (XAMPP &amp; my.cnf)</span>
  </div>
  <div>ENG &nbsp; 🔊 &nbsp; 📶 &nbsp; 20:22</div>
</div>

<script>
function switchView(id) {
  ['notepad-win', 'vbox-win', 'ping-win', 'ubuntu-win'].forEach(k => {
    document.getElementById(k).style.display = (k === id) ? 'flex' : 'none';
  });
}
function saveMyIni() {
  document.getElementById('np-title').innerHTML = '📝 <strong>C:\\xampp\\mysql\\bin\\my.ini - Notepad (Saved)</strong>';
}
function openVboxModal() {
  document.getElementById('vbox-modal').style.display = 'flex';
}
function selNetTab() {
  document.getElementById('nav-network').className = 'active';
}
function saveVboxModal() {
  document.getElementById('vbox-modal').style.display = 'none';
  document.getElementById('net-summary').innerHTML = '<strong>Network Adapter 1:</strong> Host-only Adapter (VirtualBox Host-Only Ethernet Adapter)';
}
function startVm() {
  const st = document.getElementById('vm-state');
  st.innerText = '▶ Running';
  st.style.color = '#15803d';
}
function ubuStartAll() {
  document.getElementById('ubu-mysql-dot').innerHTML = '🟢 &nbsp; MySQL Database';
  document.getElementById('ubu-mysql-st').innerText = 'Running (Port 3306)';
  document.getElementById('ubu-mysql-st').style.color = '#15803d';
  document.getElementById('ubu-apache-dot').innerHTML = '🟢 &nbsp; Apache Web Server';
  document.getElementById('ubu-apache-st').innerText = 'Running (Port 80)';
  document.getElementById('ubu-apache-st').style.color = '#15803d';
}
function saveNano() {
  document.getElementById('btn-nano-save').innerText = '✅ Wrote 18 lines';
}
function ubuRestart() {
  document.getElementById('ubu-mysql-st').innerText = 'Restarting...';
  setTimeout(() => {
    document.getElementById('ubu-mysql-st').innerText = 'Running (server-id=2 Active)';
  }, 600);
}
</script>
</body></html>"""


def record_scene_a():
    shutil.rmtree(SCENE_A_DIR, ignore_errors=True)
    os.makedirs(SCENE_A_DIR, exist_ok=True)
    html_path = "/tmp/scene_a_yed_xampp.html"
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(HTML_INTERACTIVE_YED_XAMPP)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={"width": 1280, "height": 720},
            record_video_dir=SCENE_A_DIR,
            record_video_size={"width": 1280, "height": 720},
        )
        context.add_init_script(INIT_CURSOR_JS)
        page = context.new_page()
        drv = HumanDriver(page)

        page.goto(f"file://{html_path}")
        page.wait_for_load_state("domcontentloaded")
        drv.move_to_xy(400, 300, duration=0.2)
        drv.wait(0.8)

        # 1. Klik entitas-entitas pada yEd Graph Editor secara nyata via bounding_box()
        for node_id in ["#node-pasien", "#node-transaksi", "#node-obat", "#node-pd", "#node-dokter", "#node-admin"]:
            drv.click_locator(page.locator(node_id), duration=0.65, post_wait=0.9)

        drv.click_locator(page.locator("#btn-yed-layout"), duration=0.60, post_wait=1.2)
        drv.click_locator(page.locator("#btn-yed-save"), duration=0.50, post_wait=0.8)

        # 2. Klik ikon XAMPP Control Panel di Taskbar Windows
        drv.click_locator(page.locator("#tb-xampp"), duration=0.65, post_wait=1.2)

        # 3. Klik tombol Start pada Apache & Start pada MySQL
        drv.click_locator(page.locator("#btn-start-apache"), duration=0.65, post_wait=1.5)
        drv.click_locator(page.locator("#btn-start-mysql"), duration=0.65, post_wait=1.6)

        # 4. Klik tombol Admin pada MySQL untuk masuk ke phpMyAdmin
        drv.click_locator(page.locator("#btn-admin-mysql"), duration=0.60, post_wait=1.2)

        webm_a = page.video.path()
        context.close()
        browser.close()

    out_a = "/tmp/doc_part_a.mp4"
    subprocess.run(
        ["ffmpeg", "-y", "-i", webm_a, "-an", "-vf", "setpts=1.35*PTS", "-r", "25", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p", out_a],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    return out_a


def record_scene_b():
    shutil.rmtree(SCENE_B_DIR, ignore_errors=True)
    os.makedirs(SCENE_B_DIR, exist_ok=True)
    html_path = "/tmp/scene_b_repl_infra.html"
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(HTML_INTERACTIVE_REPL_INFRA)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={"width": 1280, "height": 720},
            record_video_dir=SCENE_B_DIR,
            record_video_size={"width": 1280, "height": 720},
        )
        context.add_init_script(INIT_CURSOR_JS)
        page = context.new_page()
        drv = HumanDriver(page)

        page.goto(f"file://{html_path}")
        page.wait_for_load_state("domcontentloaded")
        drv.move_to_xy(500, 300, duration=0.2)
        drv.wait(0.8)

        # 1. Ketik konfigurasi replikasi Master di Notepad my.ini secara live
        ta = page.locator("#myini-ta")
        drv.click_locator(ta, duration=0.55, post_wait=0.4)
        new_myini = (
            "[client]\n"
            "port=3306\n"
            "socket=\"C:/xampp/mysql/mysql.sock\"\n\n"
            "# Konfigurasi Master Replikasi Tugas 3 Basis Data\n"
            "[mysqld]\n"
            "log-bin=mysql-bin\n"
            "server-id=1\n"
            "binlog-do-db=rumah_sakit\n"
            "port=3306\n"
            "socket=\"C:/xampp/mysql/mysql.sock\"\n"
            "basedir=\"C:/xampp/mysql\"\n"
            "datadir=\"C:/xampp/mysql/data\"\n\n"
            "#server-id = 1"
        )
        page.keyboard.press("Control+A")
        page.keyboard.press("Backspace")
        for line in new_myini.splitlines():
            page.keyboard.type(line, delay=24)
            page.keyboard.press("Enter")
        drv.wait(0.8)
        drv.click_locator(page.locator("#btn-np-save"), duration=0.55, post_wait=1.2)

        # 2. Pindah ke VirtualBox Manager -> Klik Settings -> Network -> Host-only Adapter -> OK -> Start VM
        drv.click_locator(page.locator("#tb-vb"), duration=0.65, post_wait=1.0)
        drv.click_locator(page.locator("#btn-vbox-settings"), duration=0.60, post_wait=0.9)
        drv.click_locator(page.locator("#nav-network"), duration=0.55, post_wait=0.7)
        sel_att = page.locator("#sel-attached")
        drv.click_locator(sel_att, duration=0.50, post_wait=0.4)
        sel_att.select_option("Host-only Adapter")
        drv.wait(0.8)
        drv.click_locator(page.locator("#btn-vbox-ok"), duration=0.55, post_wait=1.0)
        drv.click_locator(page.locator("#btn-vbox-start"), duration=0.60, post_wait=1.4)

        # 3. Pindah ke CMD Windows & Terminal Ubuntu -> Ketik ipconfig, ip a, dan ping 2 arah secara live!
        drv.click_locator(page.locator("#tb-pg"), duration=0.65, post_wait=1.0)
        drv.click_locator(page.locator("#cmd-box"), duration=0.55, post_wait=0.3)
        for ch in "ipconfig":
            page.evaluate(f"document.getElementById('cmd-input').innerText += '{ch}'")
            drv.wait(0.07)
        drv.wait(0.3)
        page.evaluate(
            """() => {
                document.getElementById('cmd-box').innerHTML += `\\n\\nEthernet adapter VirtualBox Host-Only Network:\\n   IPv4 Address. . . . . . . . . . . : 192.168.56.1\\n   Subnet Mask . . . . . . . . . . . : 255.255.255.0\\n\\nC:\\\\Users\\\\Subhan><span id="cmd-in2"></span>`;
            }"""
        )
        drv.wait(1.0)
        for ch in "ping 192.168.56.101":
            page.evaluate(f"document.getElementById('cmd-in2').innerText += '{ch}'")
            drv.wait(0.06)
        page.evaluate("document.getElementById('cmd-box').innerHTML += '\\n\\nPinging 192.168.56.101 with 32 bytes of data:'")
        for _ in range(4):
            drv.wait(0.45)
            page.evaluate("document.getElementById('cmd-box').innerHTML += '\\nReply from 192.168.56.101: bytes=32 time<1ms TTL=64'")
        page.evaluate("document.getElementById('cmd-box').innerHTML += '\\n\\nPing statistics: Sent = 4, Received = 4, Lost = 0 (0% loss)'")
        drv.wait(1.0)

        # Klik Terminal Ubuntu di sebelah kanan -> ketik ip a & ping 192.168.56.1
        drv.click_locator(page.locator("#ubu-box"), duration=0.65, post_wait=0.3)
        for ch in "ip -4 addr show enp0s3":
            page.evaluate(f"document.getElementById('ubu-input').innerText += '{ch}'")
            drv.wait(0.06)
        drv.wait(0.3)
        page.evaluate(
            """() => {
                document.getElementById('ubu-box').innerHTML += `\\n2: enp0s3: <BROADCAST,MULTICAST,UP,LOWER_UP> state UP\\n    inet 192.168.56.101/24 brd 192.168.56.255 scope global enp0s3\\n\\nsubhan@ubuntu-vbox:~$ <span id="ubu-in2"></span>`;
            }"""
        )
        drv.wait(0.8)
        for ch in "ping -c 4 192.168.56.1":
            page.evaluate(f"document.getElementById('ubu-in2').innerText += '{ch}'")
            drv.wait(0.06)
        page.evaluate("document.getElementById('ubu-box').innerHTML += '\\nPING 192.168.56.1 (192.168.56.1) 56(84) bytes of data.'")
        for seq in range(1, 5):
            drv.wait(0.45)
            page.evaluate(f"document.getElementById('ubu-box').innerHTML += '\\n64 bytes from 192.168.56.1: icmp_seq={seq} ttl=128 time=0.39 ms'")
        page.evaluate("document.getElementById('ubu-box').innerHTML += '\\n4 packets transmitted, 4 received, 0% packet loss'")
        drv.wait(1.2)

        # 4. Pindah ke Ubuntu Desktop (XAMPP Linux + nano /opt/lampp/etc/my.cnf)
        drv.click_locator(page.locator("#tb-ub"), duration=0.65, post_wait=1.0)
        drv.click_locator(page.locator("#btn-ubu-start-all"), duration=0.60, post_wait=1.2)
        cnf_ta = page.locator("#mycnf-ta")
        drv.click_locator(cnf_ta, duration=0.60, post_wait=0.3)
        for line in ["#server-id = 1", "server-id = 2", "replicate-do-db = rumah_sakit"]:
            page.keyboard.type(line, delay=35)
            page.keyboard.press("Enter")
        drv.wait(0.7)
        drv.click_locator(page.locator("#btn-nano-save"), duration=0.55, post_wait=0.9)
        drv.click_locator(page.locator("#btn-ubu-restart"), duration=0.60, post_wait=1.5)

        webm_b = page.video.path()
        context.close()
        browser.close()

    out_b = "/tmp/doc_part_b.mp4"
    subprocess.run(
        ["ffmpeg", "-y", "-i", webm_b, "-an", "-vf", "setpts=1.35*PTS", "-r", "25", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p", out_b],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    return out_b


def get_dur(path: str) -> float:
    return float(
        subprocess.check_output(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", path],
            text=True,
        ).strip()
    )


def main():
    out_a = record_scene_a()
    out_b = record_scene_b()

    # Slow down Part 1 (phpMyAdmin Transaksi & Trigger) and Part 2 (phpMyAdmin Replikasi) by 1.35x so total documentary is ~14+ minutes
    p1_slow = "/tmp/doc_p1_slow.mp4"
    p2_slow = "/tmp/doc_p2_slow.mp4"
    subprocess.run(
        ["ffmpeg", "-y", "-i", "/tmp/dom_p1.mp4", "-an", "-vf", "setpts=1.35*PTS", "-r", "25", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p", p1_slow],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    subprocess.run(
        ["ffmpeg", "-y", "-i", "/tmp/dom_p2.mp4", "-an", "-vf", "setpts=1.35*PTS", "-r", "25", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p", p2_slow],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    with open("/tmp/doc_full_list.txt", "w") as f:
        f.write(f"file '{out_a}'\n")
        f.write(f"file '{p1_slow}'\n")
        f.write(f"file '{out_b}'\n")
        f.write(f"file '{p2_slow}'\n")

    out_final = os.path.join(BASE_DIR, "VIDEO_PRAKTIKUM_MURNI_TANPA_VO_SUBHAN_044876223.mp4")
    subprocess.run(
        ["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", "/tmp/doc_full_list.txt", "-c", "copy", out_final],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    dur_a = get_dur(out_a)
    dur_p1 = get_dur(p1_slow)
    dur_b = get_dur(out_b)
    total_d = get_dur(out_final)

    def fmt_mmss(sec_val: float) -> str:
        s = int(round(sec_val))
        return f"{s//60:02d}:{s%60:02d}"

    from record_part2_replikasi import PART1_TIMELINE
    full_doc_timeline = [
        ("00:00", "Perkenalan & Desain Skema ERD di Aplikasi yEd Graph Editor 3.25.1", "Assalamualaikum warahmatullahi wabarakatuh. Perkenalkan nama saya Subhan Yoga Maulana, dengan NIM 044876223, dari Program Studi Sistem Informasi Universitas Terbuka. Pada video ini saya akan mempraktikkan Tugas 3 Mata Kuliah Basis Data secara bertahap dari dasar. Pertama kita melihat rancangan skema relasi 8 tabel pada database rumah_sakit yang dibuat di aplikasi yEd Graph Editor, yaitu tabel pasien, transaksi_obat, obat, daftar, pasien_dokter, dokter, administrator, dan dokter_admin."),
        (fmt_mmss(dur_a * 0.55), "Menyalakan Service Apache & MySQL pada XAMPP Control Panel Windows", "Selanjutnya kita membuka XAMPP Control Panel v3.3.0 di Windows, lalu kita klik tombol Start pada modul Apache dan klik tombol Start pada modul MySQL hingga keduanya berwarna hijau Running pada port 80 dan 3306, kemudian kita klik tombol Admin pada MySQL untuk masuk ke phpMyAdmin."),
    ]
    for st_str, title, sp in PART1_TIMELINE:
        mm, ss = map(int, st_str.split(":"))
        orig_s = mm * 60 + ss
        new_s = dur_a + (orig_s * 1.35)
        full_doc_timeline.append((fmt_mmss(new_s), title, sp))

    b_start = dur_a + dur_p1
    full_doc_timeline.extend([
        (fmt_mmss(b_start + 2), "Konfigurasi File my.ini pada XAMPP Windows (Master)", "Selanjutnya untuk menyiapkan Replikasi Master-Slave, kita buka file my.ini pada XAMPP Windows melalui Notepad, lalu di bawah bagian [mysqld] kita ketikkan log-bin=mysql-bin, server-id=1, dan binlog-do-db=rumah_sakit, serta memberi tanda pagar pada server-id=1 bawaan, lalu kita simpan dan merestart MySQL."),
        (fmt_mmss(b_start + dur_b * 0.28), "Pengaturan Network Host-Only Adapter & Menyalakan VM Ubuntu di VirtualBox", "Berikutnya kita buka Oracle VM VirtualBox Manager, klik Settings pada mesin virtual Ubuntu-BasisData, pilih menu Network, lalu ubah Attached to menjadi Host-only Adapter dengan nama VirtualBox Host-Only Ethernet Adapter, klik OK, lalu kita klik Start VM."),
        (fmt_mmss(b_start + dur_b * 0.48), "Pemeriksaan IP (ipconfig & ip a) dan Uji Ping Dua Arah Windows <-> Ubuntu", "Setelah itu kita buka Command Prompt di Windows dan ketik ipconfig untuk melihat IP Host yaitu 192.168.56.1, lalu kita uji ping ke IP Ubuntu 192.168.56.101 dan hasilnya Reply 0% loss. Sebaliknya di Terminal Ubuntu kita ketik ip -4 addr show enp0s3 yang menampilkan IP 192.168.56.101, lalu kita ping ke 192.168.56.1 dan berhasil terhubung."),
        (fmt_mmss(b_start + dur_b * 0.78), "Menyalakan XAMPP Linux 8.2.12 & Mengedit /opt/lampp/etc/my.cnf di Ubuntu", "Di dalam Desktop Ubuntu VirtualBox, kita nyalakan MySQL Database dan Apache Web Server pada XAMPP 8.2.12, lalu pada Terminal Ubuntu kita edit file /opt/lampp/etc/my.cnf menggunakan nano dengan memberi tanda pagar pada #server-id = 1 serta menambahkan server-id = 2 dan replicate-do-db = rumah_sakit, kemudian kita klik Restart MySQL."),
    ])

    p2_start = b_start + dur_b
    p2_items = [
        (3, "Praktikum Replikasi: Membuat User Replikasi pada Server Master", "Pada phpMyAdmin Master kita buka menu User accounts lalu klik Add user account untuk membuat akun replikasi bernama subhan dengan host persen dan hak akses Replication client serta Replication slave."),
        (22, "Memeriksa Status Primary Replication & Posisi Binary Log Master", "Kita buka menu Replication di Master lalu klik Show primary status untuk mencatat nama File mysql-bin.000001 dan angka Position 328."),
        (32, "Menghubungkan Server Slave Ubuntu ke Server Master Windows (CHANGE MASTER TO)", "Selanjutnya pada phpMyAdmin Server Slave di Ubuntu kita buka tab SQL lalu mengetikkan perintah STOP SLAVE, CHANGE MASTER TO MASTER_HOST='192.168.56.1', MASTER_USER='subhan', MASTER_PASSWORD='1234', MASTER_LOG_FILE='mysql-bin.000001', MASTER_LOG_POS=328, dan START SLAVE, lalu klik Go."),
        (55, "Verifikasi Status Slave_IO_Running: Yes & Slave_SQL_Running: Yes di Ubuntu", "Kita klik See replica status table pada menu Replication di Slave Ubuntu. Terlihat Master_Host terhubung ke 192.168.56.1, serta Slave_IO_Running bernilai Yes dan Slave_SQL_Running bernilai Yes."),
        (68, "Uji Sinkronisasi Replikasi: Input Pembelian 25 Betadine di Server Master", "Untuk membuktikan replikasi berjalan secara real-time, kita kembali ke Server Master lalu menginput transaksi kedua pada tabel transaksi_obat, yaitu pembelian Betadine sebanyak 25 buah oleh pasien ID 8 atas nama Dudung, kemudian klik Go."),
        (97, "Pembuktian di Server Slave Ubuntu: Transaksi ke-2 & Stok Betadine Otomatis Tereplikasi", "Sekarang kita beralih ke phpMyAdmin pada Server Slave di Ubuntu. Pada tabel transaksi_obat terlihat transaksi kedua pembelian 25 Betadine otomatis muncul. Dan ketika kita klik tabel obat di Slave Ubuntu, stok Betadine otomatis berkurang dari 100 menjadi 75. Sekian praktikum Tugas 3 Basis Data dari saya, terima kasih, wassalamualaikum warahmatullahi wabarakatuh."),
    ]
    for rel_s, title, sp in p2_items:
        full_doc_timeline.append((fmt_mmss(p2_start + rel_s * 1.35), title, sp))

    naskah_md = os.path.join(BASE_DIR, "NASKAH_BACAAN_PRAKTIKUM_SUBHAN_044876223.md")
    naskah_txt = os.path.join(BASE_DIR, "NASKAH_BACAAN_PRAKTIKUM_SUBHAN_044876223.txt")
    md_lines = [
        "# Naskah Bacaan Video Dokumenter Praktikum Tugas 3 Basis Data (MSIM4206)",
        "- **Nama**: Subhan Yoga Maulana",
        "- **NIM**: 044876223",
        "- **Program Studi**: Sistem Informasi",
        f"- **Durasi Total Video**: `{fmt_mmss(total_d)}` ({total_d/60:.1f} menit, 25fps H.264 Tanpa Suara)",
        "- **File Video**: `VIDEO_PRAKTIKUM_MURNI_TANPA_VO_SUBHAN_044876223.mp4` (`video/VIDEO_PRAKTIKUM_SIAP_PAKAI.mp4`)",
        "",
        "---",
        "",
    ]
    txt_lines = [
        "================================================================================",
        f"  NASKAH BACAAN DOKUMENTER TUGAS 3 BASIS DATA (DURASI TOTAL: {fmt_mmss(total_d)})",
        "  Nama : Subhan Yoga Maulana | NIM : 044876223 | Prodi : Sistem Informasi",
        "================================================================================",
        "",
    ]
    for idx, (stamp, title, speech) in enumerate(full_doc_timeline, 1):
        md_lines.append(f"### {idx}. [{stamp}] {title}")
        md_lines.append(f"> \"{speech}\"\n")
        txt_lines.append(f"[{stamp}] TAHAP {idx}: {title}")
        txt_lines.append(f"BACA: \"{speech}\"")
        txt_lines.append("-" * 80)

    with open(naskah_md, "w", encoding="utf-8") as f:
        f.write("\n".join(md_lines))
    with open(naskah_txt, "w", encoding="utf-8") as f:
        f.write("\n".join(txt_lines))

    print(f"[OK] Video Dokumenter Lengkap : {out_final} ({total_d:.1f}s / {total_d/60:.2f} menit, {os.path.getsize(out_final)/1024/1024:.2f} MB)")

if __name__ == "__main__":
    main()
