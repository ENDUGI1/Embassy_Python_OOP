import os
import time
import pwinput
from tabulate import tabulate

# buat qrcode
import qrcode

# Buat GUI
from tkinter import Tk, Label
from PIL import ImageTk

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def delay(seconds):
    time.sleep(seconds)

class User:
    users = []

    def __init__(self, name, phone, nik, passport, password, country):
        self.name = name
        self.phone = phone
        self.nik = nik
        self.passport = passport
        self.password = password
        self.country = country
        User.users.append(self)

    @classmethod
    def find_user(cls, nik, password):
        for user in cls.users:
            if user.nik == nik and user.password == password:
                return user
        return None

class Admin(User):
    def __init__(self):
        super().__init__('admin', 'admin', 'admin', 'admin', 'admin', 'admin')

class Laporan:
    reports = []

    def __init__(self, deskripsi, user):
        self.deskripsi = deskripsi
        self.user = user
        self.status = "Belum Ditindaklanjuti"
        Laporan.reports.append(self)

    @classmethod
    def user_reports(cls, user):
        return [laporan for laporan in cls.reports if laporan.user == user]

class Pengumuman:
    announcements = []

    def __init__(self, title, description):
        self.title = title
        self.description = description
        self.date = time.strftime("%Y-%m-%d %H:%M:%S")
        Pengumuman.announcements.append(self)

    @classmethod
    def find_announcement(cls, title):
        for announcement in cls.announcements:
            if announcement.title == title:
                return announcement
        return None

class Notification:
    notifications = []

    def __init__(self, user, message):
        self.user = user
        self.message = message
        self.timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        Notification.notifications.append(self)

    @classmethod
    def user_notifications(cls, user):
        return [notif for notif in cls.notifications if notif.user == user]

class App:
    def __init__(self):
        self.admin = Admin()

    def start(self):
        self.heading()

    def heading(self):
        clear_screen()
        print("============================================================")
        print("||                                                        ||")
        print("||                   SELAMAT DATANG                       ||")
        print("||            SISTEM PENGADUAN & BANTUAN                  ||")
        print("||       PERLINDUNGAN PEKERJA MIGRAN INDONESIA            ||")
        print("||                                                        ||")
        print("============================================================")
        delay(2.5)
        clear_screen()
        self.menu_utama()

    def menu_utama(self):
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
                self.register()
            elif menu == "2":
                self.login()
            elif menu == "3":
                self.keluar_app()
            else:
                print("Pilihan tidak ada")
                delay(1.5)

    def keluar_app(self):
        clear_screen()
        print("""==========================================================""")
        print("""|                                                        |""")
        print("""|          TERIMA KASIH SUDAH MEMAKAI LAYANAN KAMI       |""")
        print("""|          JANGAN LUPA AGAR SELALU JAGA KESEHATAN!       |""")
        print("""|                                                        |""")
        print("""==========================================================""")
        delay(2.5)
        clear_screen()
        self.credit()
        exit()

    def credit(self):
        clear_screen()
        print("""==========================================================""")
        print("""|                                                        |""")
        print("""==========================================================""")
        delay(2.5)

    def register(self):
        clear_screen()
        print("==========================================================")
        print("||                     REGISTER                          ||")
        print("==========================================================")
        name = input("Nama: ")
        while True:
            phone = input("No Telpon: ")
            nik = input("NIK: ")
            try:
                int(phone)
                int(nik)
                break
            except ValueError:
                print("Harus Berupa angka!")
                continue
        passport = input("No Passport: ")
        password = pwinput.pwinput(prompt='Password: ', mask='*')
        country = input("Negara Saat Ini: ")

        if any(u for u in User.users if u.nik == nik or u.passport == passport):
            print("NIK atau Passport sudah terdaftar!")
            delay(2)
        else:
            User(name, phone, nik, passport, password, country)
            print("Registrasi berhasil! Silakan login.")
            delay(2)

    def login(self):
        clear_screen()
        print("==========================================================")
        print("||                        LOGIN                          ||")
        print("==========================================================")
        nik = input("NIK: ")
        password = pwinput.pwinput(prompt='Password: ', mask='*')
        
        if nik == 'admin' and password == 'admin':
            self.admin_menu()
        else:
            user = User.find_user(nik, password)
            if user:
                self.user_menu(user)
            else:
                print("Login gagal! Periksa NIK dan Password.")
                delay(2)

    def user_menu(self, user):
        while True:
            clear_screen()
            print("==========================================================")
            print("||                  M E N U    U S E R                  ||")
            print("==========================================================")
            print("||                                                      ||")
            print("||       [1] MANAJEMEN LAPORAN                          ||")
            print("||       [2] CEK NOTIFIKASI                             ||")
            print("||       [3] PENGUMUMAN                                 ||")
            print("||       [4] KONTAK KEDUTAAN                            ||")
            print("||       [5] LOG OUT                                    ||")
            print("||                                                      ||")
            print("==========================================================")
            menu = input("Masukkan Pilihan : ")
            if menu == "1":
                self.manajemen_laporan(user)
            elif menu == "2":
                self.cek_notifikasi(user)
            elif menu == "3":
                self.tampilkan_pengumuman_user()
            elif menu == "4":
                self.kontak_kedutaan(user)
            elif menu == "5":
                break

    def manajemen_laporan(self, user):
        while True:
            clear_screen()
            print("===========================================================")
            print("||               MANAJEMEN LAPORAN                       ||")
            print("===========================================================")
            print("|| [1] Buat Laporan                                      ||")
            print("|| [2] Lihat Laporan                                     ||")
            print("|| [3] Ubah Laporan                                      ||")
            print("|| [4] Hapus Laporan                                     ||")
            print("|| [5] Kembali                                           ||")
            print("===========================================================")
            pilihan = input("Masukkan Pilihan: ")
            if pilihan == "1":
                self.buat_laporan(user)
            elif pilihan == "2":
                self.lihat_laporan(user)
            elif pilihan == "3":
                self.edit_laporan(user)
            elif pilihan == "4":
                self.hapus_laporan(user)
            elif pilihan == "5":
                break
            else:
                print("Pilihan tidak valid.")
                delay(1.5)

    def buat_laporan(self, user):
        clear_screen()
        print("==========================================================")
        print("||                 BUAT LAPORAN                          ||")
        print("==========================================================")
        deskripsi = input("Masukkan deskripsi laporan: ")
        Laporan(deskripsi, user)
        print("----------------------------------------------------------")
        print("Laporan berhasil dibuat!")
        print("==========================================================")
        delay(2)

    def lihat_laporan(self, user):
        clear_screen()
        print("==========================================================")
        print("||                LIHAT LAPORAN                         ||")
        print("==========================================================")
        user_reports = Laporan.user_reports(user)
        if not user_reports:
            print("Anda belum memiliki laporan.")
        else:
            table = [[i, laporan.deskripsi, laporan.status] for i, laporan in enumerate(user_reports, start=1)]
            print(tabulate(table, headers=["No", "Deskripsi", "Status"], tablefmt="grid"))
        input("Tekan 'Enter' untuk kembali ke menu.")

    def edit_laporan(self, user):
        clear_screen()
        print("==========================================================")
        print("||                UBAH LAPORAN                           ||")
        print("==========================================================")
        user_reports = Laporan.user_reports(user)
        if not user_reports:
            print("Anda belum memiliki laporan.")
            delay(2)
            return
        table = [[i, laporan.deskripsi, laporan.status] for i, laporan in enumerate(user_reports, start=1)]
        print(tabulate(table, headers=["No", "Deskripsi", "Status"], tablefmt="grid"))
        print("----------------------------------------------------------")
        while True:
            nomor = input("Masukkan nomor laporan yang ingin diubah: ")
            try:
                nomorBaru = int(nomor) - 1
                break
            except ValueError:
                print("Harus Berupa angka!")
                continue
        if 0 <= nomorBaru < len(user_reports):
            laporan = user_reports[nomorBaru]
            if laporan.status != "Belum Ditindaklanjuti":
                print("Laporan sudah ditindaklanjuti dan tidak bisa diubah.")
                delay(2)
                return
            deskripsi_baru = input("Masukkan deskripsi baru: ")
            laporan.deskripsi = deskripsi_baru
            print("Laporan berhasil diubah.")
        else:
            print("Nomor laporan tidak valid.")
        delay(2)

    def hapus_laporan(self, user):
        clear_screen()
        print("==========================================================")
        print("||                HAPUS LAPORAN                          ||")
        print("==========================================================")
        user_reports = Laporan.user_reports(user)
        if not user_reports:
            print("Anda belum memiliki laporan.")
            delay(2)
            return
        table = [[i, laporan.deskripsi, laporan.status] for i, laporan in enumerate(user_reports, start=1)]
        print(tabulate(table, headers=["No", "Deskripsi", "Status"], tablefmt="grid"))
        print("----------------------------------------------------------")
        while True:
            nomor = input("Masukkan nomor laporan yang ingin dihapus: ")
            try:
                nomorBaru = int(nomor) - 1
                break
            except ValueError:
                print("Harus Berupa angka!")
                continue
        if 0 <= nomorBaru < len(user_reports):
            laporan = user_reports[nomorBaru]
            if laporan.status != "Belum Ditindaklanjuti":
                print("Laporan sudah ditindaklanjuti dan tidak bisa dihapus.")
                delay(2)
                return
            Laporan.reports.remove(laporan)
            print("Laporan berhasil dihapus.")
        else:
            print("Nomor laporan tidak valid.")
        delay(2)

    def cek_notifikasi(self, user):
        clear_screen()
        print("==========================================================")
        print("||                   NOTIFIKASI                          ||")
        print("==========================================================")
        user_notifications = Notification.user_notifications(user)
        if not user_notifications:
            print("Anda belum memiliki notifikasi.")
        else:
            table = [[notif.timestamp, notif.message] for notif in user_notifications]
            print(tabulate(table, headers=["Waktu", "Pesan"], tablefmt="grid"))
        input("Tekan 'Enter' untuk kembali ke menu.")

    def tampilkan_pengumuman_user(self):
        clear_screen()
        print("==========================================================")
        print("||                  PENGUMUMAN                           ||")
        print("==========================================================")
        if not Pengumuman.announcements:
            print("Belum ada pengumuman.")
        else:
            table = [[i, pengumuman.title, pengumuman.description, pengumuman.date] for i, pengumuman in enumerate(Pengumuman.announcements, start=1)]
            print(tabulate(table, headers=["No", "Judul", "Deskripsi", "Tanggal"], tablefmt="grid"))
        input("Tekan 'Enter' untuk kembali ke menu.")

    def kontak_kedutaan(self, user):
        clear_screen()
        print("==========================================================")
        print("||                  KONTAK KEDUTAAN                      ||")
        print("==========================================================")
        country = user.country.lower()
        kedutaan = {
            'indonesia': {
                'alamat': 'Jl. Merdeka No. 1, Jakarta, Indonesia',
                'email': 'contact@indonesia-embassy.com',
                'phone': '+62 21 12345678'
            },
            'singapore': {
                'alamat': '7 Chatsworth Road, Singapore',
                'email': 'contact@indonesianembassy.sg',
                'phone': '+65 6737 7422'
            }
            # Add more countries as needed
        }
        info = kedutaan.get(country, None)
        if info:
            print(f"Negara: {user.country}")
            print(f"Alamat: {info['alamat']}")
            print(f"Email: {info['email']}")
            print(f"Nomor Telepon: {info['phone']}")
            confirm = input("Tampilkan QRCODE website kemlu? (ketik 'y' jika iya) ")
            if confirm == "y":
                data = "https://www.kemlu.go.id/portal/id"

                # generate qrcodenya
                img = qrcode.make(data)
 
                root = Tk()
                root.title("WEBSTIE OFFICIAL KEMLU")

                tk_img = ImageTk.PhotoImage(img)

                # Create a label widget to display the image
                label = Label(root, image=tk_img)
                label.pack()

                root.mainloop()

        else:
            print(f"Informasi kedutaan untuk negara {user.country} tidak tersedia.")
        input("Tekan 'Enter' untuk kembali ke menu.")

    def hubungi_user(self):
        clear_screen()
        print("==========================================================")
        print("||                   HUBUNGI USER                       ||")
        print("==========================================================")
        self.lihat_semua_laporan()
        
        while True:
            nama = input("Masukkan nama user yang ingin dihubungi (atau 'batal' untuk membatalkan): ").strip()
            if nama.lower() == 'batal':
                print("Operasi dibatalkan.")
                delay(2)
                return
            
            user = next((user for user in User.users if user.name == nama), None)
            
            if user:
                pesan = input("Masukkan pesan yang ingin dikirim: ").strip()
                Notification(user, pesan)
                print("Pesan berhasil dikirim!")
                delay(2)
                return
            else:
                print("Nama user tidak valid. Silakan coba lagi.")
                delay(1)

    def admin_menu(self):
        while True:
            clear_screen()
            print("==========================================================")
            print("||                  M E N U    A D M I N                ||")
            print("==========================================================")
            print("||                                                      ||")
            print("||       [1] LIHAT SEMUA LAPORAN                        ||")
            print("||       [2] TINDAK LANJUTI LAPORAN                     ||")
            print("||       [3] MANAJEMEN PENGUMUMAN                       ||")
            print("||       [4] HUBUNGI USER                               ||")
            print("||       [5] LOG OUT                                    ||")
            print("||                                                      ||")
            print("==========================================================")
            menu = input("Masukkan Pilihan : ")
            if menu == "1":
                self.lihat_semua_laporan()
                input("Tekan 'Enter' untuk kembali ke menu.")
            elif menu == "2":
                self.tindak_lanjuti_laporan()
            elif menu == "3":
                self.manajemen_pengumuman()
            elif menu == "4":
                self.hubungi_user()
            elif menu == "5":
                break

    def lihat_semua_laporan(self):
        clear_screen()
        print("==========================================================")
        print("||                SEMUA LAPORAN                         ||")
        print("==========================================================")
        if not Laporan.reports:
            print("Belum ada laporan.")
        else:
            table = [[i, laporan.deskripsi, laporan.status, laporan.user.name] for i, laporan in enumerate(Laporan.reports, start=1)]
            print(tabulate(table, headers=["No", "Deskripsi", "Status", "User"], tablefmt="grid"))

    def tindak_lanjuti_laporan(self):
        clear_screen()
        print("==========================================================")
        print("||              TINDAK LANJUTI LAPORAN                  ||")
        print("==========================================================")
        if not Laporan.reports:
            print("Belum ada laporan.")
            delay(2)
            return
        table = [[i, laporan.deskripsi, laporan.status, laporan.user.name] for i, laporan in enumerate(Laporan.reports, start=1)]
        print(tabulate(table, headers=["No", "Deskripsi", "Status", "User"], tablefmt="grid"))
        print("----------------------------------------------------------")
        while True:
            nomor = input("Masukkan nomor laporan yang ingin ditindaklanjuti: ")
            try:
                nomorBaru = int(nomor) - 1
                break
            except ValueError:
                print("Harus Berupa angka!")
                continue
        if 0 <= nomorBaru < len(Laporan.reports):
            laporan = Laporan.reports[nomorBaru]
            laporan.status = "Sudah Ditindaklanjuti"
            print("Laporan berhasil ditindaklanjuti.")
        else:
            print("Nomor laporan tidak valid.")
        delay(2)

    def manajemen_pengumuman(self):
        while True:
            clear_screen()
            print("==========================================================")
            print("||               MANAJEMEN PENGUMUMAN                   ||")
            print("==========================================================")
            print("|| [1] Buat Pengumuman                                  ||")
            print("|| [2] Lihat Pengumuman                                 ||")
            print("|| [3] Ubah Pengumuman                                  ||")
            print("|| [4] Hapus Pengumuman                                 ||")
            print("|| [5] Kembali                                          ||")
            print("==========================================================")
            pilihan = input("Masukkan Pilihan: ")
            if pilihan == "1":
                self.buat_pengumuman()
            elif pilihan == "2":
                self.lihat_pengumuman()
            elif pilihan == "3":
                self.ubah_pengumuman()
            elif pilihan == "4":
                self.hapus_pengumuman()
            elif pilihan == "5":
                break
            else:
                print("Pilihan tidak valid.")
                delay(1.5)

    def buat_pengumuman(self):
        clear_screen()
        print("==========================================================")
        print("||                 BUAT PENGUMUMAN                      ||")
        print("==========================================================")
        title = input("Masukkan judul pengumuman: ")
        description = input("Masukkan deskripsi pengumuman: ")
        Pengumuman(title, description)
        print("Pengumuman berhasil dibuat.")
        delay(2)

    def lihat_pengumuman(self):
        clear_screen()
        print("==========================================================")
        print("||                 LIHAT PENGUMUMAN                     ||")
        print("==========================================================")
        if not Pengumuman.announcements:
            print("Belum ada pengumuman.")
        else:
            table = [[i, pengumuman.title, pengumuman.description, pengumuman.date] for i, pengumuman in enumerate(Pengumuman.announcements, start=1)]
            print(tabulate(table, headers=["No", "Judul", "Deskripsi", "Tanggal"], tablefmt="grid"))
        input("Tekan 'Enter' untuk kembali ke menu.")

    def ubah_pengumuman(self):
        clear_screen()
        print("==========================================================")
        print("||                 UBAH PENGUMUMAN                      ||")
        print("==========================================================")
        if not Pengumuman.announcements:
            print("Belum ada pengumuman.")
            delay(2)
            return
        table = [[i, pengumuman.title, pengumuman.description, pengumuman.date] for i, pengumuman in enumerate(Pengumuman.announcements, start=1)]
        print(tabulate(table, headers=["No", "Judul", "Deskripsi", "Tanggal"], tablefmt="grid"))
        print("----------------------------------------------------------")
        while True:
            nomor = input("Masukkan nomor pengumuman yang ingin diubah: ")
            try:
                nomorBaru = int(nomor) - 1
                break
            except ValueError:
                print("Harus Berupa angka!")
                continue
        if 0 <= nomorBaru < len(Pengumuman.announcements):
            pengumuman = Pengumuman.announcements[nomorBaru]
            title_baru = input("Masukkan judul baru: ")
            description_baru = input("Masukkan deskripsi baru: ")
            pengumuman.title = title_baru
            pengumuman.description = description_baru
            print("Pengumuman berhasil diubah.")
        else:
            print("Nomor pengumuman tidak valid.")
        delay(2)

    def hapus_pengumuman(self):
        clear_screen()
        print("==========================================================")
        print("||                 HAPUS PENGUMUMAN                     ||")
        print("==========================================================")
        if not Pengumuman.announcements:
            print("Belum ada pengumuman.")
            delay(2)
            return
        table = [[i, pengumuman.title, pengumuman.description, pengumuman.date] for i, pengumuman in enumerate(Pengumuman.announcements, start=1)]
        print(tabulate(table, headers=["No", "Judul", "Deskripsi", "Tanggal"], tablefmt="grid"))
        print("----------------------------------------------------------")
        while True:
            nomor = input("Masukkan nomor pengumuman yang ingin dihapus: ")
            try:
                nomorBaru = int(nomor) - 1
                break
            except ValueError:
                print("Harus Berupa angka!")
                continue
        if 0 <= nomorBaru < len(Pengumuman.announcements):
            Pengumuman.announcements.pop(nomorBaru)
            print("Pengumuman berhasil dihapus.")
        else:
            print("Nomor pengumuman tidak valid.")
        delay(2)


app = App()
app.start()
