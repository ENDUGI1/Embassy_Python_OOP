"""
FastAPI app — versi web dari Sistem Pengaduan & Bantuan Perlindungan PMI.

Backend memakai ulang class OOP dari models.py (port dari versi CLI).
Penyimpanan memakai SQLite (lihat database.py), password di-hash
(lihat security.py), dan autentikasi memakai session cookie.
"""

import io
import os
from pathlib import Path

import qrcode
from fastapi import FastAPI, Request, Form, status
from fastapi.responses import HTMLResponse, RedirectResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware

from models import User, Admin, Laporan, Pengumuman, Notification, KEDUTAAN, load_all
from security import hash_password, is_hashed

BASE_DIR = Path(__file__).resolve().parent

app = FastAPI(title="SIPMI — Sistem Pengaduan & Bantuan PMI")
# Secret key diambil dari environment saat deploy; ada default untuk lokal.
app.add_middleware(
    SessionMiddleware,
    secret_key=os.environ.get("SECRET_KEY", "sipmi-pbo-rahasia-2024"),
)
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")

templates = Jinja2Templates(directory=BASE_DIR / "templates")

# Pastikan admin selalu tersedia, lalu muat seluruh data dari database.
Admin()
load_all()


# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------
def flash(request: Request, message: str, kind: str = "success"):
    request.session.setdefault("_flash", []).append({"msg": message, "kind": kind})


def pop_flash(request: Request):
    return request.session.pop("_flash", [])


def current_user(request: Request):
    """Kembalikan objek User yang sedang login, atau None."""
    nik = request.session.get("nik")
    if not nik:
        return None
    return User.find_by_nik(nik)


def is_admin(request: Request) -> bool:
    return request.session.get("is_admin", False)


def render(request: Request, name: str, **ctx):
    ctx.update({
        "request": request,
        "flashes": pop_flash(request),
        "user": current_user(request),
        "is_admin": is_admin(request),
    })
    return templates.TemplateResponse(name, ctx)


def redirect(url: str):
    return RedirectResponse(url, status_code=status.HTTP_303_SEE_OTHER)


# ---------------------------------------------------------------------------
# Landing & Auth
# ---------------------------------------------------------------------------
@app.get("/", response_class=HTMLResponse)
def landing(request: Request):
    if is_admin(request):
        return redirect("/admin")
    if current_user(request):
        return redirect("/dashboard")
    return render(request, "landing.html",
                  jumlah_pengumuman=len(Pengumuman.announcements),
                  jumlah_negara=len(KEDUTAAN))


@app.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return render(request, "login.html")


@app.post("/login")
def login(request: Request, nik: str = Form(...), password: str = Form(...)):
    nik = nik.strip()
    if nik == "admin" and password == "admin":
        request.session["nik"] = "admin"
        request.session["is_admin"] = True
        flash(request, "Selamat datang kembali, Admin.")
        return redirect("/admin")

    user = User.find_user(nik, password)
    if user and user.name != "admin":
        # Upgrade otomatis: jika password lama masih plaintext, simpan sebagai hash.
        if not is_hashed(user.password):
            user.password = hash_password(password)
            User.save_all()
        request.session["nik"] = user.nik
        request.session["is_admin"] = False
        flash(request, f"Selamat datang, {user.name}.")
        return redirect("/dashboard")

    flash(request, "Login gagal! Periksa NIK dan Password.", "error")
    return redirect("/login")


@app.get("/register", response_class=HTMLResponse)
def register_page(request: Request):
    return render(request, "register.html")


@app.post("/register")
def register(
    request: Request,
    name: str = Form(...),
    phone: str = Form(...),
    nik: str = Form(...),
    passport: str = Form(...),
    password: str = Form(...),
    country: str = Form(...),
):
    name, phone, nik = name.strip(), phone.strip(), nik.strip()
    passport, country = passport.strip(), country.strip()

    # Validasi mengikuti aturan versi CLI.
    if not name.replace(" ", "").isalpha():
        flash(request, "Nama hanya boleh mengandung huruf!", "error")
        return redirect("/register")
    if not phone.isdigit():
        flash(request, "No Telpon harus berupa angka!", "error")
        return redirect("/register")
    if not nik.isdigit():
        flash(request, "NIK harus berupa angka!", "error")
        return redirect("/register")
    if not country.replace(" ", "").isalpha():
        flash(request, "Negara hanya boleh mengandung huruf!", "error")
        return redirect("/register")

    if any(u for u in User.users if u.nik == nik or u.name == name or u.passport == passport):
        flash(request, "NIK, Nama, atau Passport sudah terdaftar!", "error")
        return redirect("/register")

    User(name, phone, nik, passport, hash_password(password), country)
    User.remove_duplicates()
    User.save_all()
    flash(request, "Registrasi berhasil! Silakan login.")
    return redirect("/login")


@app.get("/logout")
def logout(request: Request):
    request.session.clear()
    return redirect("/")


# ---------------------------------------------------------------------------
# Area User
# ---------------------------------------------------------------------------
@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request):
    user = current_user(request)
    if not user or is_admin(request):
        return redirect("/login")
    laporan = Laporan.user_reports(user)
    notif = Notification.user_notifications(user)
    return render(
        request, "user/dashboard.html",
        laporan=laporan,
        notif=notif,
        jumlah_pengumuman=len(Pengumuman.announcements),
        belum=sum(1 for l in laporan if l.status == "Belum Ditindaklanjuti"),
        selesai=sum(1 for l in laporan if l.status != "Belum Ditindaklanjuti"),
    )


@app.get("/laporan", response_class=HTMLResponse)
def laporan_page(request: Request):
    user = current_user(request)
    if not user or is_admin(request):
        return redirect("/login")
    reports = Laporan.user_reports(user)
    # Sertakan index global agar aksi edit/hapus menunjuk objek yang tepat.
    items = [(Laporan.reports.index(l), l) for l in reports]
    return render(request, "user/laporan.html", items=items)


@app.post("/laporan/create")
def laporan_create(request: Request, deskripsi: str = Form(...)):
    user = current_user(request)
    if not user or is_admin(request):
        return redirect("/login")
    if not deskripsi.strip():
        flash(request, "Deskripsi laporan tidak boleh kosong.", "error")
        return redirect("/laporan")
    Laporan(deskripsi.strip(), user.name)
    Laporan.remove_duplicates()
    Laporan.save_all()
    flash(request, "Laporan berhasil dibuat!")
    return redirect("/laporan")


@app.post("/laporan/{idx}/edit")
def laporan_edit(request: Request, idx: int, deskripsi: str = Form(...)):
    user = current_user(request)
    if not user or is_admin(request):
        return redirect("/login")
    if not (0 <= idx < len(Laporan.reports)):
        flash(request, "Laporan tidak ditemukan.", "error")
        return redirect("/laporan")
    laporan = Laporan.reports[idx]
    if laporan.user != user.name:
        flash(request, "Anda tidak berhak mengubah laporan ini.", "error")
        return redirect("/laporan")
    if laporan.status != "Belum Ditindaklanjuti":
        flash(request, "Laporan sudah ditindaklanjuti dan tidak bisa diubah.", "error")
        return redirect("/laporan")
    if not deskripsi.strip():
        flash(request, "Deskripsi tidak boleh kosong.", "error")
        return redirect("/laporan")
    laporan.deskripsi = deskripsi.strip()
    Laporan.remove_duplicates()
    Laporan.save_all()
    flash(request, "Laporan berhasil diubah.")
    return redirect("/laporan")


@app.post("/laporan/{idx}/delete")
def laporan_delete(request: Request, idx: int):
    user = current_user(request)
    if not user or is_admin(request):
        return redirect("/login")
    if not (0 <= idx < len(Laporan.reports)):
        flash(request, "Laporan tidak ditemukan.", "error")
        return redirect("/laporan")
    laporan = Laporan.reports[idx]
    if laporan.user != user.name:
        flash(request, "Anda tidak berhak menghapus laporan ini.", "error")
        return redirect("/laporan")
    if laporan.status != "Belum Ditindaklanjuti":
        flash(request, "Laporan sudah ditindaklanjuti dan tidak bisa dihapus.", "error")
        return redirect("/laporan")
    Laporan.reports.remove(laporan)
    Laporan.remove_duplicates()
    Laporan.save_all()
    flash(request, "Laporan berhasil dihapus.")
    return redirect("/laporan")


@app.get("/notifikasi", response_class=HTMLResponse)
def notifikasi_page(request: Request):
    user = current_user(request)
    if not user or is_admin(request):
        return redirect("/login")
    notif = list(reversed(Notification.user_notifications(user)))
    return render(request, "user/notifikasi.html", notif=notif)


@app.get("/pengumuman", response_class=HTMLResponse)
def pengumuman_page(request: Request):
    user = current_user(request)
    if not user or is_admin(request):
        return redirect("/login")
    return render(request, "user/pengumuman.html",
                  announcements=list(reversed(Pengumuman.announcements)))


@app.get("/kontak", response_class=HTMLResponse)
def kontak_page(request: Request):
    user = current_user(request)
    if not user or is_admin(request):
        return redirect("/login")
    info = KEDUTAAN.get(user.country.lower())
    return render(request, "user/kontak.html", info=info)


@app.get("/qr")
def qr_code():
    """Hasilkan QR code menuju website resmi Kemlu (pengganti popup tkinter)."""
    img = qrcode.make("https://www.kemlu.go.id/portal/id")
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return StreamingResponse(buf, media_type="image/png")


# ---------------------------------------------------------------------------
# Area Admin
# ---------------------------------------------------------------------------
@app.get("/admin", response_class=HTMLResponse)
def admin_dashboard(request: Request):
    if not is_admin(request):
        return redirect("/login")
    total = len(Laporan.reports)
    belum = sum(1 for l in Laporan.reports if l.status == "Belum Ditindaklanjuti")
    return render(
        request, "admin/dashboard.html",
        total_laporan=total,
        belum=belum,
        selesai=total - belum,
        jumlah_user=sum(1 for u in User.users if u.name != "admin"),
        jumlah_pengumuman=len(Pengumuman.announcements),
        recent=list(reversed(Laporan.reports))[:5],
    )


@app.get("/admin/laporan", response_class=HTMLResponse)
def admin_laporan(request: Request):
    if not is_admin(request):
        return redirect("/login")
    items = list(enumerate(Laporan.reports))
    return render(request, "admin/laporan.html", items=items)


@app.post("/admin/laporan/{idx}/tindaklanjuti")
def admin_tindaklanjuti(request: Request, idx: int):
    if not is_admin(request):
        return redirect("/login")
    if 0 <= idx < len(Laporan.reports):
        Laporan.reports[idx].status = "Sudah Ditindaklanjuti"
        Laporan.remove_duplicates()
        Laporan.save_all()
        flash(request, "Laporan berhasil ditindaklanjuti.")
    else:
        flash(request, "Laporan tidak ditemukan.", "error")
    return redirect("/admin/laporan")


@app.get("/admin/pengumuman", response_class=HTMLResponse)
def admin_pengumuman(request: Request):
    if not is_admin(request):
        return redirect("/login")
    items = list(enumerate(Pengumuman.announcements))
    return render(request, "admin/pengumuman.html", items=items)


@app.post("/admin/pengumuman/create")
def admin_pengumuman_create(request: Request, title: str = Form(...), description: str = Form(...)):
    if not is_admin(request):
        return redirect("/login")
    if not title.strip() or not description.strip():
        flash(request, "Judul dan deskripsi tidak boleh kosong.", "error")
        return redirect("/admin/pengumuman")
    Pengumuman(title.strip(), description.strip())
    Pengumuman.remove_duplicates()
    Pengumuman.save_all()
    flash(request, "Pengumuman berhasil dibuat.")
    return redirect("/admin/pengumuman")


@app.post("/admin/pengumuman/{idx}/edit")
def admin_pengumuman_edit(request: Request, idx: int, title: str = Form(...), description: str = Form(...)):
    if not is_admin(request):
        return redirect("/login")
    if 0 <= idx < len(Pengumuman.announcements):
        p = Pengumuman.announcements[idx]
        p.title = title.strip()
        p.description = description.strip()
        Pengumuman.remove_duplicates()
        Pengumuman.save_all()
        flash(request, "Pengumuman berhasil diubah.")
    else:
        flash(request, "Pengumuman tidak ditemukan.", "error")
    return redirect("/admin/pengumuman")


@app.post("/admin/pengumuman/{idx}/delete")
def admin_pengumuman_delete(request: Request, idx: int):
    if not is_admin(request):
        return redirect("/login")
    if 0 <= idx < len(Pengumuman.announcements):
        Pengumuman.announcements.pop(idx)
        Pengumuman.remove_duplicates()
        Pengumuman.save_all()
        flash(request, "Pengumuman berhasil dihapus.")
    else:
        flash(request, "Pengumuman tidak ditemukan.", "error")
    return redirect("/admin/pengumuman")


@app.get("/admin/hubungi", response_class=HTMLResponse)
def admin_hubungi(request: Request):
    if not is_admin(request):
        return redirect("/login")
    users = [u for u in User.users if u.name != "admin"]
    return render(request, "admin/hubungi.html", users=users)


@app.post("/admin/hubungi")
def admin_hubungi_send(request: Request, nama: str = Form(...), pesan: str = Form(...)):
    if not is_admin(request):
        return redirect("/login")
    target = next((u for u in User.users if u.name == nama and u.name != "admin"), None)
    if not target:
        flash(request, "Nama user tidak valid.", "error")
        return redirect("/admin/hubungi")
    if not pesan.strip():
        flash(request, "Pesan tidak boleh kosong.", "error")
        return redirect("/admin/hubungi")
    Notification(nama, pesan.strip())
    Notification.remove_duplicates()
    Notification.save_all()
    flash(request, f"Pesan berhasil dikirim ke {nama}.")
    return redirect("/admin/hubungi")
