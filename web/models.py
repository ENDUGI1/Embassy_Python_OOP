"""
Model OOP untuk versi web SIPMI (Sistem Pengaduan & Bantuan Perlindungan PMI).

Class di sini hasil port dari versi CLI (SafeMigran.py / mulaiDariAwal.py).
Struktur OOP dipertahankan: pewarisan (Admin -> User), @classmethod, dan
@staticmethod. Yang berubah hanya layer penyimpanan: dari file CSV menjadi
database SQLite (lihat database.py). Pola lama tetap sama — data dimuat ke
daftar di memori (User.users, dst.), lalu disimpan kembali ke database.

Password tidak lagi disimpan polos; lihat security.py.
"""

import time

from database import get_conn, init_db
from security import verify_password


# ---------------------------------------------------------------------------
# Kelas User untuk mengelola data pengguna
# ---------------------------------------------------------------------------
class User:
    users = []  # Menyimpan daftar semua pengguna (cache di memori)

    def __init__(self, name, phone, nik, passport, password, country):
        self.name = name
        self.phone = phone
        self.nik = nik
        self.passport = passport
        self.password = password  # sudah dalam bentuk hash (kecuali admin)
        self.country = country
        User.users.append(self)

    # Cari pengguna berdasarkan NIK lalu verifikasi password (mendukung hash)
    @classmethod
    def find_user(cls, nik, password):
        for user in cls.users:
            if user.nik == nik and verify_password(user.password, password):
                return user
        return None

    # Cari pengguna berdasarkan NIK saja
    @classmethod
    def find_by_nik(cls, nik):
        for user in cls.users:
            if user.nik == nik:
                return user
        return None

    # Simpan seluruh daftar pengguna ke database (akun admin tidak disimpan)
    @staticmethod
    def save_all():
        conn = get_conn()
        conn.execute("DELETE FROM users")
        for u in User.users:
            if u.name == "admin":
                continue
            conn.execute(
                "INSERT INTO users (name, phone, nik, passport, password, country) "
                "VALUES (?,?,?,?,?,?)",
                (u.name, u.phone, u.nik, u.passport, u.password, u.country),
            )
        conn.commit()

    # Muat seluruh pengguna dari database ke memori
    @staticmethod
    def load_all():
        conn = get_conn()
        rows = conn.execute(
            "SELECT name, phone, nik, passport, password, country FROM users ORDER BY id"
        ).fetchall()
        for r in rows:
            User(r["name"], r["phone"], r["nik"], r["passport"], r["password"], r["country"])

    # Hapus duplikat pengguna dari daftar di memori
    @staticmethod
    def remove_duplicates():
        seen = set()
        result = []
        for user in User.users:
            key = (user.name, user.phone, user.nik, user.passport, user.password, user.country)
            if key not in seen:
                seen.add(key)
                result.append(user)
        User.users = result


# ---------------------------------------------------------------------------
# Kelas Admin yang mewarisi dari kelas User
# ---------------------------------------------------------------------------
class Admin(User):
    def __init__(self):
        super().__init__("admin", "admin", "admin", "admin", "admin", "admin")


# ---------------------------------------------------------------------------
# Kelas Laporan untuk mengelola data laporan
# ---------------------------------------------------------------------------
class Laporan:
    reports = []

    def __init__(self, deskripsi, user, status="Belum Ditindaklanjuti"):
        self.deskripsi = deskripsi
        self.user = user
        self.status = status
        Laporan.reports.append(self)

    @classmethod
    def user_reports(cls, user):
        return [laporan for laporan in cls.reports if laporan.user == user.name]

    @staticmethod
    def save_all():
        conn = get_conn()
        conn.execute("DELETE FROM reports")
        for r in Laporan.reports:
            conn.execute(
                "INSERT INTO reports (deskripsi, user, status) VALUES (?,?,?)",
                (r.deskripsi, r.user, r.status),
            )
        conn.commit()

    @staticmethod
    def load_all():
        conn = get_conn()
        rows = conn.execute(
            "SELECT deskripsi, user, status FROM reports ORDER BY id"
        ).fetchall()
        for r in rows:
            Laporan(r["deskripsi"], r["user"], r["status"])

    @staticmethod
    def remove_duplicates():
        seen = set()
        result = []
        for laporan in Laporan.reports:
            key = (laporan.deskripsi, laporan.user, laporan.status)
            if key not in seen:
                seen.add(key)
                result.append(laporan)
        Laporan.reports = result


# ---------------------------------------------------------------------------
# Kelas Pengumuman untuk mengelola data pengumuman
# ---------------------------------------------------------------------------
class Pengumuman:
    announcements = []

    def __init__(self, title, description, date=None):
        self.title = title
        self.description = description
        self.date = date if date else time.strftime("%Y-%m-%d %H:%M:%S")
        Pengumuman.announcements.append(self)

    @classmethod
    def find_announcement(cls, title):
        for announcement in cls.announcements:
            if announcement.title == title:
                return announcement
        return None

    @staticmethod
    def save_all():
        conn = get_conn()
        conn.execute("DELETE FROM announcements")
        for a in Pengumuman.announcements:
            conn.execute(
                "INSERT INTO announcements (title, description, date) VALUES (?,?,?)",
                (a.title, a.description, a.date),
            )
        conn.commit()

    @staticmethod
    def load_all():
        conn = get_conn()
        rows = conn.execute(
            "SELECT title, description, date FROM announcements ORDER BY id"
        ).fetchall()
        for r in rows:
            Pengumuman(r["title"], r["description"], r["date"])

    @staticmethod
    def remove_duplicates():
        seen = set()
        result = []
        for announcement in Pengumuman.announcements:
            key = (announcement.title, announcement.description, announcement.date)
            if key not in seen:
                seen.add(key)
                result.append(announcement)
        Pengumuman.announcements = result


# ---------------------------------------------------------------------------
# Kelas Notification untuk mengelola data notifikasi
# ---------------------------------------------------------------------------
class Notification:
    notifications = []

    def __init__(self, user, message, timestamp=None):
        self.user = user
        self.message = message
        self.timestamp = timestamp if timestamp else time.strftime("%Y-%m-%d %H:%M:%S")
        Notification.notifications.append(self)

    @classmethod
    def user_notifications(cls, user):
        return [notif for notif in cls.notifications if notif.user == user.name]

    @staticmethod
    def save_all():
        conn = get_conn()
        conn.execute("DELETE FROM notifications")
        for n in Notification.notifications:
            conn.execute(
                "INSERT INTO notifications (user, message, timestamp) VALUES (?,?,?)",
                (n.user, n.message, n.timestamp),
            )
        conn.commit()

    @staticmethod
    def load_all():
        conn = get_conn()
        rows = conn.execute(
            "SELECT user, message, timestamp FROM notifications ORDER BY id"
        ).fetchall()
        for r in rows:
            Notification(r["user"], r["message"], r["timestamp"])

    @staticmethod
    def remove_duplicates():
        seen = set()
        result = []
        for notification in Notification.notifications:
            key = (notification.user, notification.message, notification.timestamp)
            if key not in seen:
                seen.add(key)
                result.append(notification)
        Notification.notifications = result


# ---------------------------------------------------------------------------
# Data kontak kedutaan
# ---------------------------------------------------------------------------
KEDUTAAN = {
    'indonesia': {'alamat': 'Jl. Merdeka No. 1, Jakarta, Indonesia', 'email': 'contact@indonesia-embassy.com', 'phone': '+62 21 12345678'},
    'singapore': {'alamat': '7 Chatsworth Road, Singapore', 'email': 'contact@indonesianembassy.sg', 'phone': '+65 6737 7422'},
    'taiwan': {'alamat': 'No. 550, Rui Guang Road, Neihu District, Taipei, Taiwan', 'email': 'contact@indonesian-embassy.tw', 'phone': '+886 2 8752 6170'},
    'malaysia': {'alamat': '233 Jalan Tun Razak, Kuala Lumpur, Malaysia', 'email': 'contact@indonesia.org.my', 'phone': '+60 3 2116 4016'},
    'hongkong': {'alamat': '127-129 Leighton Road, Causeway Bay, Hong Kong', 'email': 'contact@indonesia-consulate.hk', 'phone': '+852 2890 4421'},
    'korea selatan': {'alamat': '380 Yeouido-dong, Yeongdeungpo-gu, Seoul, South Korea', 'email': 'contact@indonesian-embassy.kr', 'phone': '+82 2 783 5675'},
    'jepang': {'alamat': '5-2-9 Higashi Gotanda, Shinagawa-ku, Tokyo, Japan', 'email': 'contact@indonesian-embassy.jp', 'phone': '+81 3 3441 4201'},
    'arab saudi': {'alamat': 'Diplomatic Quarter, Riyadh, Saudi Arabia', 'email': 'contact@indonesian-embassy.sa', 'phone': '+966 11 488 2800'},
    'italia': {'alamat': 'Via Campania 55, Rome, Italy', 'email': 'contact@indonesian-embassy.it', 'phone': '+39 06 420 0911'},
    'brunei darussalam': {'alamat': 'No. 29, Simpang 336, Jalan Duta, Kampong Sungai Hanching, Brunei', 'email': 'contact@indonesian-embassy.bn', 'phone': '+673 233 0180'},
    'turki': {'alamat': 'Abdullah Cevdet Sokak No.12, Cankaya, Ankara, Turkey', 'email': 'contact@indonesian-embassy.tr', 'phone': '+90 312 438 2190'},
}


def load_all():
    """Inisialisasi database (buat tabel + seed dari CSV bila kosong), lalu muat
    seluruh data ke memori. Dipanggil sekali saat aplikasi start."""
    init_db()
    User.load_all()
    Laporan.load_all()
    Pengumuman.load_all()
    Notification.load_all()
