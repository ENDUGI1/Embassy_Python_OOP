# SIPMI — Versi Web (FastAPI)

Versi web dari Sistem Pengaduan & Bantuan Perlindungan PMI. Backend memakai ulang
class OOP dari versi CLI (lihat `models.py`), penyimpanan memakai **SQLite**, dan
tampilan dibangun dengan Tailwind CSS.

## Fitur teknis

- **OOP dipertahankan** — class `User`, `Admin` (mewarisi `User`), `Laporan`,
  `Pengumuman`, `Notification` dengan `@classmethod`/`@staticmethod`.
- **SQLite** (`web/sipmi.db`, dibuat otomatis) lewat modul bawaan `sqlite3`.
  Saat pertama jalan, data di-*seed* dari file CSV di root project (kompatibel
  dengan versi CLI).
- **Password di-hash** dengan PBKDF2-HMAC-SHA256 (`security.py`) — tidak lagi
  disimpan polos. Akun lama berpassword plaintext otomatis di-hash saat login.
- **Auth** memakai session cookie.

## Cara Menjalankan (lokal)

```bash
pip install -r web/requirements.txt
cd web
uvicorn main:app --reload
```

Buka <http://127.0.0.1:8000>. Database `sipmi.db` dibuat & di-seed otomatis.

> Catatan: jalankan **satu** instance server saja. Menjalankan dua server ke
> file `sipmi.db` yang sama secara bersamaan bisa saling menimpa data.

## Akun

- **Admin** — NIK: `admin`, Password: `admin`
- **User contoh** — password semua `123` (mis. NIK `6571023541` = Abdullah Azam).
  Atau daftar lewat halaman Register.

## Deploy ke Render.com

Konfigurasi sudah disiapkan di `render.yaml` (root project).

1. Pastikan repo sudah di-push ke GitHub.
2. Buka <https://render.com> → **New +** → **Blueprint**.
3. Hubungkan repo `Embassy_Python_OOP`. Render membaca `render.yaml` dan membuat
   service-nya otomatis (build `pip install`, start `uvicorn`).
4. Tunggu build selesai, lalu buka URL publik yang diberikan Render.

> ⚠️ Di paket gratis Render, filesystem bersifat *ephemeral*: file `sipmi.db`
> bisa ter-reset saat service restart/redeploy, sehingga data kembali ke kondisi
> seed dari CSV. Cukup untuk demo. Untuk data permanen, gunakan database hosted
> (mis. Postgres) atau Render Persistent Disk.

## Struktur

```
web/
├── main.py            # Aplikasi FastAPI (routing + auth session)
├── models.py          # Class OOP (persistensi via SQLite)
├── database.py        # Setup SQLite + seed dari CSV
├── security.py        # Hash & verifikasi password
├── requirements.txt
├── static/
└── templates/         # Halaman Jinja2 + Tailwind
    ├── base.html, app_base.html
    ├── landing.html, login.html, register.html
    ├── user/          # dashboard, laporan, notifikasi, pengumuman, kontak
    └── admin/         # dashboard, laporan, pengumuman, hubungi
```
