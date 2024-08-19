from sqlalchemy import create_engine, MetaData, text
from sqlalchemy.exc import OperationalError
from models import generate_model
from controllers import generate_controller
#from views import generate_view
from routes import generate_routes
#from auth import generate_auth
from template.index_template import generate_index_template
from template.create_template import generate_create_template
from template.edit_template import generate_edit_template
from template.show_template import generate_show_template

#include component
from component.syncGit import copy_repo

import pymysql
import time
import os
import sys

# Fungsi untuk menampilkan header FH PROJECT
def display_header():
    print("\033[92m" + """
    ███████╗██╗  ██╗    ███████╗██╗  ██╗
    ██╔════╝██║  ██║    ██╔════╝██║  ██║
    ███████╗███████║    █████╗  ███████║
    ╚════██║██╔══██║    ██╔══╝  ██╔══██║
    ███████║██║  ██║    ██║     ██║  ██║
    ╚══════╝╚═╝  ╚═╝    ╚═╝     ╚═╝  ╚═╝
    """ + "\033[0m")
    time.sleep(1)

# Fungsi untuk menampilkan teks seperti hacker
def hacker_text(text):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(0.01)
    print()

# Fungsi untuk membuat direktori jika belum ada
def ensure_directory_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

# Fungsi untuk menampilkan progress bar
def print_progress_bar(iteration, total, prefix='', suffix='', decimals=1, length=50, fill='█', print_end="\r"):
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '-' * (length - filled_length)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end=print_end)
    if iteration == total:
        print()

# Tampilkan header
display_header()

# Ganti dengan detail koneksi database Anda
DATABASE_URI = 'mysql+pymysql://root:@localhost/'

# Koneksi ke database tanpa menentukan nama database
engine = create_engine(DATABASE_URI)
connection = engine.connect()

# Tampilkan nama-nama database yang ada
result = connection.execute(text("SHOW DATABASES"))
databases = [row[0] for row in result if row[0] not in ['information_schema', 'mysql', 'performance_schema', 'sys']]

hacker_text("Daftar database yang tersedia:")
for i, db in enumerate(databases):
    hacker_text(f"{i + 1}. {db}")

# Pilih nama database
while True:
    db_choice = input("Pilih nomor database atau masukkan nama database baru: ")

    if db_choice.isdigit() and 1 <= int(db_choice) <= len(databases):
        dbname = databases[int(db_choice) - 1]
        break
    elif db_choice.strip() == "":
        print("Input tidak boleh kosong, silakan pilih ulang.")
    else:
        dbname = db_choice
        # Buat database baru jika belum ada
        if dbname not in databases:
            connection.execute(f"CREATE DATABASE {dbname}")
            hacker_text(f"Database '{dbname}' telah dibuat.")
            break
        else:
            print("Pilihan tidak tersedia, silakan pilih ulang.")

# Update DATABASE_URI dengan nama database yang dipilih
DATABASE_URI += dbname

#tanyakan repo github
while True:
    generate_laravel = input("apakah anda ingin menambahkan laravel? (y/n)").strip().lower()
    if generate_laravel in ['y', 'n']:
        break
    else:
        print("Input tidak valid, silakan masukkan 'yes' atau 'no'.")

if generate_laravel == 'y':
    # Jalankan proses clone repo
    copy_repo(dbname)

# Koneksi ulang dengan nama database yang dipilih
engine = create_engine(DATABASE_URI)
metadata = MetaData()
metadata.reflect(bind=engine)

# Tampilkan nama-nama tabel yang ada
tables = list(metadata.tables.keys())
excluded_tables = ['activity_log','cache', 'cache_locks', 'failed_jobs','job_batches','jobs','migrations','model_has_permissions','model_has_roles','password_reset_tokens','permissions','role_has_permissions','roles','sessions','users']  # add the table names you want to exclude
metadata.tables = {table: metadata.tables[table] for table in tables if table not in excluded_tables}

hacker_text("Daftar tabel yang tersedia:")
for i, table in enumerate(tables):
    hacker_text(f"{i + 1}. {table}")

# Pilih tabel atau semua tabel
while True:
    table_choice = input("Pilih nomor tabel, masukkan nama tabel, atau ketik 'all' untuk semua tabel: ")

    if table_choice.lower() == 'all':
        selected_tables = metadata.tables.values()
        break
    elif table_choice.isdigit() and 1 <= int(table_choice) <= len(tables):
        selected_tables = [metadata.tables[tables[int(table_choice) - 1]]]
        break
    elif table_choice.strip() == "":
        print("Input tidak boleh kosong, silakan pilih ulang.")
    elif table_choice in tables:
        selected_tables = [metadata.tables[table_choice]]
        break
    else:
        print("Pilihan tidak tersedia, silakan pilih ulang.")

total_tables = len(selected_tables)
print_progress_bar(0, total_tables, prefix='Progress:', suffix='Complete', length=50)

for i, table in enumerate(selected_tables, 1):
    # Periksa direktori jika belum ada, buat direktori tersebut
    ensure_directory_exists('output/'+dbname+'/app/Http/Controllers')
    ensure_directory_exists('output/'+dbname+'/app/Models')
    ensure_directory_exists('output/'+dbname+'/resources/views')

    generate_model(table, dbname)
    generate_controller(table, dbname)
    generate_index_template(table, dbname)
    generate_create_template(table, dbname)
    generate_edit_template(table, dbname)
    generate_show_template(table, dbname)
    #generate_view(table)
    
    # Update progress bar
    print_progress_bar(i, total_tables, prefix='Progress:', suffix='Complete', length=50)

ensure_directory_exists('output/'+dbname+'/routes')
generate_routes([t.name for t in selected_tables], dbname)

# Konfirmasi untuk generate auth
#while True:
#    auth_choice = input("Apakah Anda ingin membuat auth? (yes/no): ").strip().lower()
#    if auth_choice in ['yes', 'no']:
#        break
#    else:
#        print("Input tidak valid, silakan masukkan 'yes' atau 'no'.")

#if auth_choice == 'yes':
#    generate_auth()
    # Tambahkan progress loading di bawah generate auth
#    print_progress_bar(1, 1, prefix='Progress:', suffix='Auth Complete', length=50)

# Laporan selesai

print("\033[92m" + "Proses pembuatan model, controller, view, dan route telah selesai!" + "\033[0m")

# Tanyakan kepada user apakah mereka ingin mengulang proses dari awal
while True:
    repeat_choice = input("Apakah Anda ingin mengulang proses dari awal? (yes/no): ").strip().lower()
    if repeat_choice in ['yes', 'no']:
        break
    else:
        print("Input tidak valid, silakan masukkan 'yes' atau 'no'.")

if repeat_choice == 'yes':
    # Jalankan proses dari awal
    os.system('python ' + sys.argv[0])
else:
    # Keluar dari program
    print("Terima kasih telah menggunakan program ini!")
    sys.exit(0)