"""
Layer database SQLite untuk versi web SIPMI.

Memakai modul bawaan `sqlite3` (tanpa dependency tambahan). Database disimpan
dalam satu file `sipmi.db`. Jika tabel `users` masih kosong, data awal di-seed
dari file CSV yang sudah ada (kompatibel dengan versi CLI), dan password polos
otomatis di-hash saat proses seeding.
"""

import csv
import sqlite3
from pathlib import Path

from security import hash_password

BASE_DIR = Path(__file__).resolve().parent          # folder web/
ROOT_DIR = BASE_DIR.parent                           # root project (lokasi CSV)
DB_PATH = BASE_DIR / "sipmi.db"

# Satu koneksi dipakai bersama. check_same_thread=False karena FastAPI dapat
# menjalankan handler di thread berbeda.
_conn = sqlite3.connect(DB_PATH, check_same_thread=False)
_conn.row_factory = sqlite3.Row


def get_conn() -> sqlite3.Connection:
    return _conn


def init_db():
    """Buat tabel jika belum ada, lalu seed data awal dari CSV bila kosong."""
    cur = _conn.cursor()
    cur.executescript(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT, phone TEXT, nik TEXT, passport TEXT,
            password TEXT, country TEXT
        );
        CREATE TABLE IF NOT EXISTS reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            deskripsi TEXT, user TEXT, status TEXT
        );
        CREATE TABLE IF NOT EXISTS announcements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT, description TEXT, date TEXT
        );
        CREATE TABLE IF NOT EXISTS notifications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user TEXT, message TEXT, timestamp TEXT
        );
        """
    )
    _conn.commit()
    _seed_if_empty()


def _rows(csv_name: str, expected_cols: int):
    """Baca baris CSV dari root project, strip tiap kolom. Lewati jika tak ada."""
    path = ROOT_DIR / csv_name
    if not path.exists():
        return
    with open(path, "r", newline="") as f:
        # skipinitialspace agar field ber-spasi sebelum tanda kutip (mis. di
        # notifications.csv) tetap terbaca sebagai satu kolom yang benar.
        for row in csv.reader(f, skipinitialspace=True):
            if len(row) == expected_cols:
                yield [c.strip() for c in row]


def _seed_if_empty():
    """Isi database dari CSV hanya jika tabel users masih kosong."""
    cur = _conn.cursor()
    if cur.execute("SELECT COUNT(*) FROM users").fetchone()[0] > 0:
        return

    seen_users = set()
    for name, phone, nik, passport, password, country in _rows("users.csv", 6):
        if name == "admin":                 # akun admin di-handle khusus, tak disimpan
            continue
        if nik in seen_users:               # buang duplikat berdasarkan NIK
            continue
        seen_users.add(nik)
        cur.execute(
            "INSERT INTO users (name, phone, nik, passport, password, country) "
            "VALUES (?,?,?,?,?,?)",
            (name, phone, nik, passport, hash_password(password), country),
        )

    for deskripsi, user, status in _rows("reports.csv", 3):
        cur.execute(
            "INSERT INTO reports (deskripsi, user, status) VALUES (?,?,?)",
            (deskripsi, user, status),
        )

    for title, description, date in _rows("announcements.csv", 3):
        cur.execute(
            "INSERT INTO announcements (title, description, date) VALUES (?,?,?)",
            (title, description, date),
        )

    for user, message, timestamp in _rows("notifications.csv", 3):
        cur.execute(
            "INSERT INTO notifications (user, message, timestamp) VALUES (?,?,?)",
            (user, message, timestamp),
        )

    _conn.commit()
