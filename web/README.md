# SIPMI — Versi Web (FastAPI)

Versi web dari Sistem Pengaduan & Bantuan Perlindungan PMI. Backend memakai ulang
class OOP dari `mulaiDariAwal.py` (lihat `models.py`), penyimpanan tetap memakai
file CSV yang sama di root project, dan tampilan dibangun dengan Tailwind CSS.

## Cara Menjalankan

1. Install dependency (sekali saja):

   ```bash
   pip install -r web/requirements.txt
   ```

2. Jalankan server dari folder `web/`:

   ```bash
   cd web
   uvicorn main:app --reload
   ```

3. Buka di browser: <http://127.0.0.1:8000>

## Akun

- **Admin** — NIK: `admin`, Password: `admin`
- **User** — daftar lewat halaman Register, atau pakai data contoh di `users.csv`
  (password semua user contoh: `123`).

## Struktur

```
web/
├── main.py            # Aplikasi FastAPI (routing + auth session)
├── models.py          # Class OOP (User, Admin, Laporan, Pengumuman, Notification)
├── requirements.txt
├── static/            # Aset statis
└── templates/         # Halaman Jinja2 + Tailwind
    ├── base.html, app_base.html
    ├── landing.html, login.html, register.html
    ├── user/          # dashboard, laporan, notifikasi, pengumuman, kontak
    └── admin/         # dashboard, laporan, pengumuman, hubungi
```

Data CSV (`users.csv`, `reports.csv`, `announcements.csv`, `notifications.csv`)
dibaca dari root project sehingga kompatibel dengan versi CLI.
