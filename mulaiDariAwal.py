import os
import time
import pwinput
from tabulate import tabulate

# buat qrcode
import qrcode

# CSV
import csv

# Buat GUI
from tkinter import Tk, Label
from PIL import ImageTk

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def delay(seconds):
    time.sleep(seconds)

class User: # Class User
    users = [] # List untuk menyimpan data users

    def __init__(self, name, phone, nik, passport, password, country):
        self.name = name
        self.phone = phone
        self.nik = nik
        self.passport = passport
        self.password = password
        self.country = country
        User.users.append(self)

    @classmethod
    def find_user(cls, nik, password): # Method untuk mencari nik dan password (digunakan ketika login)
        for user in cls.users:
            if user.nik == nik and user.password == password:
                return user
        return None
    @staticmethod
    def save_to_csv(): # Method untuk menyimpan data user ke file users.csv (digunakan ketika registrasi akun)
        with open('users.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            for user in User.users:
                writer.writerow([user.name, user.phone, user.nik, user.passport, user.password, user.country])

    @staticmethod
    def load_from_csv(): # Method untuk mengambil data user dari file users.csv (digunakan saat program dijalankan)
        try:
            with open('users.csv', 'r') as file:
                reader = csv.reader(file)
                for row in reader:
                    if len(row) == 6:  # Pastikan baris memiliki 6 kolom sesuai dengan data user
                        User(row[0], row[1], row[2], row[3], row[4], row[5])
        except FileNotFoundError:
            # Jika file CSV belum ada, program akan membuat file kosong
            with open('users.csv', 'w', newline=''):
                pass
    @staticmethod
    def remove_duplicates(): # Method untuk menghapus data yang duplikat pada data user
        seen = set()
        result = []
        for user in User.users:
            user_tuple = (user.name, user.phone, user.nik, user.passport, user.password, user.country)
            if user_tuple not in seen:
                seen.add(user_tuple)
                result.append(user)
        User.users = result  # Update atribut users dengan hasil yang sudah dihapus duplikat

class Admin(User): # Class admin inheritent dengan class user
    def __init__(self):
        super().__init__('admin', 'admin', 'admin', 'admin', 'admin', 'admin')

class Laporan: # Class Laporan
    reports = [] # list untuk menyimpan laporan

    def __init__(self, deskripsi, user):
        self.deskripsi = deskripsi
        self.user = user
        self.status = "Belum Ditindaklanjuti"
        Laporan.reports.append(self)

    @classmethod
    def user_reports(cls, user): # Method untuk mengambil data laporan (digunakan saat akan melihat laporan)
        return [laporan for laporan in cls.reports if laporan.user == user.name]
    @staticmethod
    def save_to_csv(): # Method untuk menyimpan data laporan ke file reports.csv (digunakan saat membuat, mengubah, dan menghapus laporan)
        with open('reports.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            for report in Laporan.reports:
                nama = report.user
                writer.writerow([report.deskripsi, nama, report.status])
    @staticmethod
    def load_from_csv(): # Method untuk mengambil data Laporan dari file reports.csv (digunakan saat program dijalankan)
        try:
            with open('reports.csv', 'r') as file:
                reader = csv.reader(file)
                for row in reader:
                    if len(row) == 3:  # Pastikan baris memiliki 3 kolom sesuai dengan data reports
                        deskripsi, user, status = row
                        Laporan(deskripsi, user)
        except FileNotFoundError:
            # Jika file CSV belum ada, program akan membuat file kosong
            with open('reports.csv', 'w', newline=''):
                pass
    @staticmethod
    def remove_duplicates(): # Method untuk menghapus data yang duplikat pada data laporan
        seen = set()
        result = []
        for laporan in Laporan.reports:
            laporan_tuple = (laporan.deskripsi, laporan.user, laporan.status)
            if laporan_tuple not in seen:
                seen.add(laporan_tuple)
                result.append(laporan)
        Laporan.reports = result 

class Pengumuman: # Class Pengumuman
    announcements = [] # List untuk menyimpan pengumuman

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
    @staticmethod
    def save_to_csv(): # Method untuk menyimpan data pengumuman ke file announcements.csv (digunakan saat membuat, mengubah, dan menghapus pengumuman)
        with open('announcements.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            for announcement in Pengumuman.announcements:
                writer.writerow([announcement.title, announcement.description, announcement.date])

    @staticmethod
    def load_from_csv(): # Method untuk mengambil data pengumuman dari file announcements.csv (digunakan saat program dijalankan)
        try:
            with open('announcements.csv', 'r') as file:
                reader = csv.reader(file)
                for row in reader:
                    if len(row) == 3:  # Pastikan baris memiliki 3 kolom sesuai dengan data pengumuman
                        title, description, date = row
                        Pengumuman(title, description)
        except FileNotFoundError:
            # Jika file CSV belum ada, program akan membuat file kosong
            with open('announcements.csv', 'w', newline=''):
                pass

    @staticmethod
    def remove_duplicates(): # Method untuk menghapus data yang duplikat pada data pengumuman
        seen = set()
        result = []
        for announcement in Pengumuman.announcements:
            announcement_tuple = (announcement.title, announcement.description, announcement.date)
            if announcement_tuple not in seen:
                seen.add(announcement_tuple)
                result.append(announcement)
        Pengumuman.announcements = result 

class Notification: # Class Notification
    notifications = [] # List untuk menyimpan notofikasi

    def __init__(self, user, message):
        self.user = user
        self.message = message
        self.timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        Notification.notifications.append(self)

    @classmethod
    def user_notifications(cls, user): # Method untuk melihat notifikasi (digunakan saat user melihat notifikasi)
        return [notif for notif in cls.notifications if notif.user == user.name]
    @staticmethod
    def save_to_csv(): # Method untuk menyimpan data notifikasi ke file notifications.csv (digunakan saat membuat mengirim pesan ke user)
        with open('notifications.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            for notification in Notification.notifications:
                writer.writerow([notification.user, notification.message, notification.timestamp])

    @staticmethod
    def load_from_csv(): # Method untuk mengambil data notifikasi dari file notifications.csv (digunakan saat program dijalankan)
        try:
            with open('notifications.csv', 'r') as file:
                reader = csv.reader(file)
                for row in reader:
                    if len(row) == 3:  # Pastikan baris memiliki 3 kolom sesuai dengan data notification
                        user, message, timestamp = row
                        Notification(user, message)
        except FileNotFoundError:
            # Jika file CSV belum ada, program akan membuat file kosong
            with open('notifications.csv', 'w', newline=''):
                pass

    @staticmethod
    def remove_duplicates(): # Method untuk menghapus data yang duplikat pada data notifikasi
        seen = set()
        result = []
        for notification in Notification.notifications:
            notification_tuple = (notification.user, notification.message, notification.timestamp)
            if notification_tuple not in seen:
                seen.add(notification_tuple)
                result.append(notification)
        Notification.notifications = result  # Update atribut notifications dengan hasil yang sudah dihapus duplikat

class App: # Class App
    def __init__(self):
        self.admin = Admin()

    def start(self): # fungsi saat program dijalankan (akan mengambil data dari file csv)
        User.load_from_csv() 
        Laporan.load_from_csv()
        Pengumuman.load_from_csv()
        Notification.load_from_csv()
        self.heading()

    def heading(self): # heading tampilan saat program dijalankan
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

    def menu_utama(self): # menu utama
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
                self.register() # menuju ke registrasi
            elif menu == "2":
                self.login() # menuju ke login
            elif menu == "3":
                self.keluar_app() # Logout
            else:
                print("Pilihan tidak ada") # erro handling jika pilihan tidak ada
                delay(1.5)

    def keluar_app(self): # tampilan saat keluar program
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

    def credit(self): #creadit aplikasi
        clear_screen()
        print("""==========================================================""")
        print("""|                                                        |""")
        print("""==========================================================""")
        delay(2.5)

    def register(self): # fungsi registrasi
        clear_screen()
        print("==========================================================")
        print("||                     REGISTER                          ||")
        print("==========================================================")
        
        while True:
            name = input("Nama: ") # input nama
            if name.replace(" ", "").isalpha(): # error handling input nama hanya bisa huruf
                break
            else:
                print("Nama hanya boleh mengandung huruf!")
        
        while True:
            phone = input("No Telpon: ") # input nomor telepon
            if phone.isdigit(): # error handling input nomor telepon hanya bisa angka
                break
            else:
                print("No Telpon harus berupa angka!")
        
        while True:
            nik = input("NIK: ") # input nik
            if nik.isdigit(): # error handling input nik hanya bisa angka
                break
            else:
                print("NIK harus berupa angka!")

        passport = input("No Passport: ") # input passport
        password = pwinput.pwinput(prompt='Password: ', mask='*') # input password (saat menginput password akan di samarkan dengan *)
        
        while True:
            country = input("Negara Saat Ini: ") # input negara
            if country.replace(" ", "").isalpha(): # error handling input negara hanya bisa huruf
                break
            else:
                print("Negara hanya boleh mengandung huruf!")

        if any(u for u in User.users if u.nik == nik or u.name == name or u.passport == passport): # error jika NIK, Nama, Passport sudah terdaftar
            print("NIK, Nama, Passport sudah terdaftar!")
            delay(2)
        else:
            User(name, phone, nik, passport, password, country) # menyimpan registrasi
            User.remove_duplicates()
            User.save_to_csv() # menyimpan data user ke file users.csv
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
        Laporan(deskripsi, user.name)
        Laporan.remove_duplicates()
        Laporan.save_to_csv()
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
            Laporan.remove_duplicates()
            Laporan.save_to_csv()
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
            Laporan.remove_duplicates()
            Laporan.save_to_csv()
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
            },
            'taiwan': {
                'alamat': 'No. 550, Rui Guang Road, Neihu District, Taipei, Taiwan',
                'email': 'contact@indonesian-embassy.tw',
                'phone': '+886 2 8752 6170'
            },
            'malaysia': {
                'alamat': '233 Jalan Tun Razak, Kuala Lumpur, Malaysia',
                'email': 'contact@indonesia.org.my',
                'phone': '+60 3 2116 4016'
            },
            'hongkong': {
                'alamat': '127-129 Leighton Road, Causeway Bay, Hong Kong',
                'email': 'contact@indonesia-consulate.hk',
                'phone': '+852 2890 4421'
            },
            'korea selatan': {
                'alamat': '380 Yeouido-dong, Yeongdeungpo-gu, Seoul, South Korea',
                'email': 'contact@indonesian-embassy.kr',
                'phone': '+82 2 783 5675'
            },
            'jepang': {
                'alamat': '5-2-9 Higashi Gotanda, Shinagawa-ku, Tokyo, Japan',
                'email': 'contact@indonesian-embassy.jp',
                'phone': '+81 3 3441 4201'
            },
            'arab saudi': {
                'alamat': 'Diplomatic Quarter, Riyadh, Saudi Arabia',
                'email': 'contact@indonesian-embassy.sa',
                'phone': '+966 11 488 2800'
            },
            'italia': {
                'alamat': 'Via Campania 55, Rome, Italy',
                'email': 'contact@indonesian-embassy.it',
                'phone': '+39 06 420 0911'
            },
            'brunei darussalam': {
                'alamat': 'No. 29, Simpang 336, Jalan Duta, Kampong Sungai Hanching, Brunei',
                'email': 'contact@indonesian-embassy.bn',
                'phone': '+673 233 0180'
            },
            'turki': {
                'alamat': 'Abdullah Cevdet Sokak No.12, Çankaya, Ankara, Turkey',
                'email': 'contact@indonesian-embassy.tr',
                'phone': '+90 312 438 2190'
            }
        }
        info = kedutaan.get(country, None)
        if info:
            print(f"Negara: {user.country}")
            print(f"Alamat: {info['alamat']}")
            print(f"Email: {info['email']}")
            print(f"Nomor Telepon: {info['phone']}")
        else:
            print(f"Informasi kedutaan untuk negara {user.country} tidak tersedia.")
        
        confirm = input("Tampilkan QRCODE website kemlu? (ketik 'y' jika iya) ")
        if confirm == "y":
            data = "https://www.kemlu.go.id/portal/id"
            
            # generate qrcode
            img = qrcode.make(data)

            root = Tk()
            root.title("WEBSTIE OFFICIAL KEMLU")

            tk_img = ImageTk.PhotoImage(img)

            # Create a label widget to display the image
            label = Label(root, image=tk_img)
            label.pack()

            root.mainloop()

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
                Notification(nama, pesan)
                print("Pesan berhasil dikirim!")
                Notification.remove_duplicates()
                Notification.save_to_csv()
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
            table = [[i, laporan.deskripsi, laporan.status, laporan.user] for i, laporan in enumerate(Laporan.reports, start=1)]
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
        table = [[i, laporan.deskripsi, laporan.status, laporan.user] for i, laporan in enumerate(Laporan.reports, start=1)]
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
            Laporan.remove_duplicates()
            Laporan.save_to_csv()
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
        Pengumuman.remove_duplicates()
        Pengumuman.save_to_csv()
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
            Pengumuman.remove_duplicates()
            Pengumuman.save_to_csv()
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
            Pengumuman.remove_duplicates()
            Pengumuman.save_to_csv()
        else:
            print("Nomor pengumuman tidak valid.")
        delay(2)


app = App()
app.start()
