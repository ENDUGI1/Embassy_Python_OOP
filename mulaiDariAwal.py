import os
import time
import pwinput

# Fungsi untuk membersihkan layar
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# Fungsi untuk memberikan jeda
def delay(seconds):
    time.sleep(seconds)

# Data storage
users = []
reports = []
announcements = []

# Fungsi untuk menampilkan heading
def heading():
    clear_screen()
    print("+=========================================================+")
    print("||                                                        ||")
    print("||                   SELAMAT DATANG                       ||")
    print("||          SAFE MIGRANT: Sistem Pengaduan & Bantuan      ||")
    print("||       Perlindungan Pekerja Migran Indonesia            ||")
    print("||                                                        ||")
    print("+=========================================================+")
    delay(2.5)
    clear_screen()
    menu_utama()

# Fungsi untuk keluar dari aplikasi
def keluar_app():
    clear_screen()
    print("""==========================================================""")
    print("""|                                                        |""")
    print("""|                                                        |""")
    print("""|          TERIMA KASIH SUDAH MEMAKAI LAYANAN KAMI       |""")
    print("""|          JANGAN LUPA AGAR SELALU JAGA KESEHATAN!       |""")
    print("""|                                                        |""")
    print("""|                                                        |""")
    print("""==========================================================""")
    delay(2.5)
    clear_screen()
    credit()
    exit()

# Fungsi untuk menampilkan menu utama
def menu_utama():
    while True:
        clear_screen()
        print("============================================================")
        print("||                  M E N U    U T A M A                  ||")
        print("============================================================")
        print("||                                                        ||")
        print("||       [1] REGISTER                                     ||")
        print("||       [2] LOGIN                                        ||")
        print("||       [3] EXIT                                         ||")
        print("||                                                        ||")
        print("============================================================")
        menu = input("Masukkan Pilihan : ")
        if menu == "1":
            register()
        elif menu == "2":
            login()
        elif menu == "3":
            keluar_app()
        else:
            print("Pilihan tidak ada")  #error handling maszeh
            delay(1.5)
            
# Fungsi untuk menampilkan kredit
def credit():
    clear_screen()
    print("""==========================================================""")
    print("""|                                                        |""")
    print("""|                                                        |""")
    print("""|                                                        |""")
    print("""|                                                        |""")
    print("""|                                                        |""")
    print("""|                                                        |""")
    print("""|                                                        |""")
    print("""==========================================================""")
    delay(2.5)

# Fungsi untuk register
def register():
    clear_screen()
    print("== Register ==")
    name = input("Nama: ")
    phone = input("No Telpon: ")
    nik = input("NIK: ")
    passport = input("No Passport: ")
    password = pwinput.pwinput(prompt='Password: ', mask='*')
    country = input("Negara: ")

    if any(u for u in users if u['nik'] == nik or u['passport'] == passport):
        print("NIK atau Passport sudah terdaftar!")
        delay(2)
    else:
        user = {
            'id': len(users) + 1,
            'name': name,
            'phone': phone,
            'nik': nik,
            'passport': passport,
            'password': password,
            'country': country
        }
        users.append(user)
        print("Registrasi berhasil! Silakan login.")
        delay(2)

# Fungsi untuk login
def login():
    clear_screen()
    print("== Login ==")
    nik = input("NIK: ")
    password = pwinput.pwinput(prompt='Password: ', mask='*')
    user = next((u for u in users if u['nik'] == nik and u['password'] == password), None)
    if user:
        user_menu(user)
    elif nik == 'admin' and password == 'admin':
        admin_menu()
    else:
        print("Login gagal! Periksa NIK dan Password.")
        delay(2)

# Fungsi untuk menu user
def user_menu(user):
    while True:
        clear_screen()
        print("==========================================================")
        print("||                  M E N U    U S E R                  ||")
        print("==========================================================")
        print("||                                                      ||")
        print("||       [1] MANAJEMEN LAPORAN                          ||")
        print("||       [2] CEK NOTIFIKASI                             ||")
        print("||       [3] PENGUMUMAN                                 ||")
        print("||       [4] KONTAK KEDUTAAN                             ||")
        print("||       [5] LOG OUT                                    ||")
        print("||                                                      ||")
        print("==========================================================")
        menu = input("Masukkan Pilihan : ")
        if menu == "1":
            buat_laporan()
        elif menu == "2":
            pass  # Tambahkan fungsi untuk cek notifikasi
        elif menu == "3":
            pass  # Tambahkan fungsi untuk melihat pengumuman
        elif menu == "4":
            pass  # Tambahkan fungsi untuk kontak kedutaan
        elif menu == "5":
            break

# Fungsi untuk menu admin
def admin_menu():
    while True:
        clear_screen()
        print("==========================================================")
        print("||                  M E N U    A D M I N                ||")
        print("==========================================================")
        print("||                                                      ||")
        print("||       [1] MANAJEMEN PENGUMUMAN                       ||")
        print("||       [2] TINJAU LAPORAN                             ||")
        print("||       [3] TAMPILKAN DATA PMI                         ||")
        print("||       [4] HUBUNGI PMI                                ||")
        print("||       [5] LOG OUT                                    ||")
        print("||                                                      ||")
        print("==========================================================")
        menu = input("Masukkan Pilihan : ")
        if menu == "1":
            pass  # Tambahkan fungsi untuk manajemen pengumuman
        elif menu == "2":
            pass  # Tambahkan fungsi untuk tinjau laporan
        elif menu == "3":
            pass  # Tambahkan fungsi untuk menampilkan data PMI
        elif menu == "4":
            pass  # Tambahkan fungsi untuk menghubungi PMI
        elif menu == "5":
            break

# Fungsi untuk membuat laporan
def buat_laporan():
    clear_screen()
    print("== Buat Laporan ==")
    deskripsi = input("Masukkan deskripsi laporan: ")
    reports.append(deskripsi)
    print("Laporan berhasil dibuat!")
    delay(2)

#
def lihat_laporan():
    clear_screen()
    print("== Lihat Laporan ==")
    if not reports:
        print("Belum ada laporan.")
    else:
        for i, laporan in enumerate(reports, start=1):
            print(f"{i}. {laporan}")
    input("Tekan 'Enter' untuk kembali ke menu.")

def edit_laporan():
    clear_screen()
    print("== Edit Laporan ==")
    if not reports:
        print("Belum ada laporan.")
    else:
        for i, laporan in enumerate(reports, start=1):
            print(f"{i}. {laporan}")
        nomor_laporan = int(input("Pilih nomor laporan yang ingin diubah: "))
        if 1 <= nomor_laporan <= len(reports):
            deskripsi_baru = input("Masukkan deskripsi laporan yang baru: ")
            reports[nomor_laporan - 1] = deskripsi_baru
            print("Laporan berhasil diubah!")
        else:
            print("Nomor laporan tidak valid.")
    input("Tekan 'Enter' untuk kembali ke menu.")


def hapus_laporan():
    clear_screen()
    print("== Hapus Laporan ==")
    if not reports:
        print("Belum ada laporan.")
    else:
        for i, laporan in enumerate(reports, start=1):
            print(f"{i}. {laporan}")
        nomor_laporan = int(input("Pilih nomor laporan yang ingin dihapus: "))
        if 1 <= nomor_laporan <= len(reports):
            del reports[nomor_laporan - 1]
            print("Laporan berhasil dihapus!")
        else:
            print("Nomor laporan tidak valid.")
    input("Tekan 'Enter' untuk kembali ke menu.")


heading()