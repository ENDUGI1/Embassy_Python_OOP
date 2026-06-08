"""
Model OOP untuk versi web Sistem Pengaduan & Bantuan Perlindungan PMI.

Class di sini adalah hasil port dari mulaiDariAwal.py (versi CLI). Struktur OOP
dipertahankan apa adanya: pewarisan (Admin -> User), @classmethod, dan
@staticmethod untuk operasi CSV. Yang berubah hanya:
  - Path CSV dibuat absolut (mengarah ke root project), bukan relatif.
  - Setiap kolom di-strip() saat load agar data lama yang ber-spasi tetap cocok.
  - Logika input/print khas terminal dipindah ke layer web (main.py).
"""

import csv
import time
from pathlib import Path

# Direktori data = root project (satu level di atas folder web/).
# CSV lama (users.csv, reports.csv, dst.) tetap dipakai supaya data tidak hilang.
DATA_DIR = Path(__file__).resolve().parent.parent

USERS_CSV = DATA_DIR / "users.csv"
REPORTS_CSV = DATA_DIR / "reports.csv"
ANNOUNCEMENTS_CSV = DATA_DIR / "announcements.csv"
NOTIFICATIONS_CSV = DATA_DIR / "notifications.csv"


# ---------------------------------------------------------------------------
# Kelas User untuk mengelola data pengguna
# ---------------------------------------------------------------------------
class User:
    users = []  # Menyimpan daftar semua pengguna

    def __init__(self, name, phone, nik, passport, password, country):
        self.name = name
        self.phone = phone
        self.nik = nik
        self.passport = passport
        self.password = password
        self.country = country
        User.users.append(self)  # Tambahkan pengguna baru ke daftar

    # Metode kelas untuk mencari pengguna berdasarkan NIK dan password
    @classmethod
    def find_user(cls, nik, password):
        for user in cls.users:
            if user.nik == nik and user.password == password:
                return user
        return None

    # Metode kelas untuk mencari pengguna berdasarkan NIK saja
    @classmethod
    def find_by_nik(cls, nik):
        for user in cls.users:
            if user.nik == nik:
                return user
        return None

    # Metode statis untuk menyimpan data pengguna ke file CSV
    @staticmethod
    def save_to_csv():
        with open(USERS_CSV, 'w', newline='') as file:
            writer = csv.writer(file)
            for user in User.users:
                writer.writerow([user.name, user.phone, user.nik, user.passport, user.password, user.country])

    # Metode statis untuk memuat data pengguna dari file CSV
    @staticmethod
    def load_from_csv():
        try:
            with open(USERS_CSV, 'r') as file:
                reader = csv.reader(file)
                for row in reader:
                    if len(row) == 6:  # Pastikan baris memiliki 6 kolom sesuai dengan data user
                        cleaned = [field.strip() for field in row]
                        User(*cleaned)
        except FileNotFoundError:
            # Jika file CSV belum ada, program akan membuat file kosong
            with open(USERS_CSV, 'w', newline=''):
                pass

    # Metode statis untuk menghapus duplikat pengguna dari daftar
    @staticmethod
    def remove_duplicates():
        seen = set()
        result = []
        for user in User.users:
            user_tuple = (user.name, user.phone, user.nik, user.passport, user.password, user.country)
            if user_tuple not in seen:
                seen.add(user_tuple)
                result.append(user)
        User.users = result  # Update atribut users dengan hasil yang sudah dihapus duplikat


# ---------------------------------------------------------------------------
# Kelas Admin yang mewarisi dari kelas User, mewakili admin sistem
# ---------------------------------------------------------------------------
class Admin(User):
    def __init__(self):
        super().__init__('admin', 'admin', 'admin', 'admin', 'admin', 'admin')


# ---------------------------------------------------------------------------
# Kelas Laporan untuk mengelola data laporan
# ---------------------------------------------------------------------------
class Laporan:
    reports = []  # Menyimpan daftar semua laporan

    def __init__(self, deskripsi, user, status="Belum Ditindaklanjuti"):
        self.deskripsi = deskripsi
        self.user = user
        self.status = status
        Laporan.reports.append(self)  # Tambahkan laporan baru ke daftar

    # Metode kelas untuk mendapatkan laporan berdasarkan pengguna
    @classmethod
    def user_reports(cls, user):
        return [laporan for laporan in cls.reports if laporan.user == user.name]

    # Metode statis untuk menyimpan data laporan ke file CSV
    @staticmethod
    def save_to_csv():
        with open(REPORTS_CSV, 'w', newline='') as file:
            writer = csv.writer(file)
            for report in Laporan.reports:
                writer.writerow([report.deskripsi, report.user, report.status])

    # Metode statis untuk memuat data laporan dari file CSV
    @staticmethod
    def load_from_csv():
        try:
            with open(REPORTS_CSV, 'r') as file:
                reader = csv.reader(file)
                for row in reader:
                    if len(row) == 3:  # Pastikan baris memiliki 3 kolom sesuai dengan data reports
                        deskripsi, user, status = [field.strip() for field in row]
                        Laporan(deskripsi, user, status)
        except FileNotFoundError:
            # Jika file CSV belum ada, program akan membuat file kosong
            with open(REPORTS_CSV, 'w', newline=''):
                pass

    # Metode statis untuk menghapus duplikat laporan dari daftar
    @staticmethod
    def remove_duplicates():
        seen = set()
        result = []
        for laporan in Laporan.reports:
            laporan_tuple = (laporan.deskripsi, laporan.user, laporan.status)
            if laporan_tuple not in seen:
                seen.add(laporan_tuple)
                result.append(laporan)
        Laporan.reports = result


# ---------------------------------------------------------------------------
# Kelas Pengumuman untuk mengelola data pengumuman
# ---------------------------------------------------------------------------
class Pengumuman:
    announcements = []  # Menyimpan daftar semua pengumuman

    def __init__(self, title, description, date=None):
        self.title = title
        self.description = description
        self.date = date if date else time.strftime("%Y-%m-%d %H:%M:%S")
        Pengumuman.announcements.append(self)  # Tambahkan pengumuman baru ke daftar

    # Metode kelas untuk mencari pengumuman berdasarkan judul
    @classmethod
    def find_announcement(cls, title):
        for announcement in cls.announcements:
            if announcement.title == title:
                return announcement
        return None

    # Metode statis untuk menyimpan data pengumuman ke file CSV
    @staticmethod
    def save_to_csv():
        with open(ANNOUNCEMENTS_CSV, 'w', newline='') as file:
            writer = csv.writer(file)
            for announcement in Pengumuman.announcements:
                writer.writerow([announcement.title, announcement.description, announcement.date])

    # Metode statis untuk memuat data pengumuman dari file CSV
    @staticmethod
    def load_from_csv():
        try:
            with open(ANNOUNCEMENTS_CSV, 'r') as file:
                reader = csv.reader(file)
                for row in reader:
                    if len(row) == 3:  # Pastikan baris memiliki 3 kolom sesuai dengan data pengumuman
                        title, description, date = [field.strip() for field in row]
                        Pengumuman(title, description, date)
        except FileNotFoundError:
            # Jika file CSV belum ada, program akan membuat file kosong
            with open(ANNOUNCEMENTS_CSV, 'w', newline=''):
                pass

    # Metode statis untuk menghapus duplikat pengumuman dari daftar
    @staticmethod
    def remove_duplicates():
        seen = set()
        result = []
        for announcement in Pengumuman.announcements:
            announcement_tuple = (announcement.title, announcement.description, announcement.date)
            if announcement_tuple not in seen:
                seen.add(announcement_tuple)
                result.append(announcement)
        Pengumuman.announcements = result


# ---------------------------------------------------------------------------
# Kelas Notification untuk mengelola data notifikasi
# ---------------------------------------------------------------------------
class Notification:
    notifications = []  # Menyimpan daftar semua notifikasi

    def __init__(self, user, message, timestamp=None):
        self.user = user
        self.message = message
        self.timestamp = timestamp if timestamp else time.strftime("%Y-%m-%d %H:%M:%S")
        Notification.notifications.append(self)  # Tambahkan notifikasi baru ke daftar

    # Metode kelas untuk mendapatkan notifikasi berdasarkan pengguna
    @classmethod
    def user_notifications(cls, user):
        return [notif for notif in cls.notifications if notif.user == user.name]

    # Metode statis untuk menyimpan data notifikasi ke file CSV
    @staticmethod
    def save_to_csv():
        with open(NOTIFICATIONS_CSV, 'w', newline='') as file:
            writer = csv.writer(file)
            for notification in Notification.notifications:
                writer.writerow([notification.user, notification.message, notification.timestamp])

    # Metode statis untuk memuat data notifikasi dari file CSV
    @staticmethod
    def load_from_csv():
        try:
            with open(NOTIFICATIONS_CSV, 'r') as file:
                reader = csv.reader(file)
                for row in reader:
                    if len(row) == 3:  # Pastikan baris memiliki 3 kolom sesuai dengan data notification
                        user, message, timestamp = [field.strip() for field in row]
                        Notification(user, message, timestamp)
        except FileNotFoundError:
            # Jika file CSV belum ada, program akan membuat file kosong
            with open(NOTIFICATIONS_CSV, 'w', newline=''):
                pass

    # Metode statis untuk menghapus duplikat notifikasi dari daftar
    @staticmethod
    def remove_duplicates():
        seen = set()
        result = []
        for notification in Notification.notifications:
            notification_tuple = (notification.user, notification.message, notification.timestamp)
            if notification_tuple not in seen:
                seen.add(notification_tuple)
                result.append(notification)
        Notification.notifications = result


# ---------------------------------------------------------------------------
# Data kontak kedutaan (dipindah dari method kontak_kedutaan versi CLI)
# ---------------------------------------------------------------------------
KEDUTAAN = {
    'indonesia': {
        'alamat': 'Jl. Merdeka No. 1, Jakarta, Indonesia',
        'email': 'contact@indonesia-embassy.com',
        'phone': '+62 21 12345678',
    },
    'singapore': {
        'alamat': '7 Chatsworth Road, Singapore',
        'email': 'contact@indonesianembassy.sg',
        'phone': '+65 6737 7422',
    },
    'taiwan': {
        'alamat': 'No. 550, Rui Guang Road, Neihu District, Taipei, Taiwan',
        'email': 'contact@indonesian-embassy.tw',
        'phone': '+886 2 8752 6170',
    },
    'malaysia': {
        'alamat': '233 Jalan Tun Razak, Kuala Lumpur, Malaysia',
        'email': 'contact@indonesia.org.my',
        'phone': '+60 3 2116 4016',
    },
    'hongkong': {
        'alamat': '127-129 Leighton Road, Causeway Bay, Hong Kong',
        'email': 'contact@indonesia-consulate.hk',
        'phone': '+852 2890 4421',
    },
    'korea selatan': {
        'alamat': '380 Yeouido-dong, Yeongdeungpo-gu, Seoul, South Korea',
        'email': 'contact@indonesian-embassy.kr',
        'phone': '+82 2 783 5675',
    },
    'jepang': {
        'alamat': '5-2-9 Higashi Gotanda, Shinagawa-ku, Tokyo, Japan',
        'email': 'contact@indonesian-embassy.jp',
        'phone': '+81 3 3441 4201',
    },
    'arab saudi': {
        'alamat': 'Diplomatic Quarter, Riyadh, Saudi Arabia',
        'email': 'contact@indonesian-embassy.sa',
        'phone': '+966 11 488 2800',
    },
    'italia': {
        'alamat': 'Via Campania 55, Rome, Italy',
        'email': 'contact@indonesian-embassy.it',
        'phone': '+39 06 420 0911',
    },
    'brunei darussalam': {
        'alamat': 'No. 29, Simpang 336, Jalan Duta, Kampong Sungai Hanching, Brunei',
        'email': 'contact@indonesian-embassy.bn',
        'phone': '+673 233 0180',
    },
    'turki': {
        'alamat': 'Abdullah Cevdet Sokak No.12, Cankaya, Ankara, Turkey',
        'email': 'contact@indonesian-embassy.tr',
        'phone': '+90 312 438 2190',
    },
}


def load_all():
    """Muat semua data dari CSV. Dipanggil sekali saat aplikasi start."""
    User.load_from_csv()
    Laporan.load_from_csv()
    Pengumuman.load_from_csv()
    Notification.load_from_csv()
