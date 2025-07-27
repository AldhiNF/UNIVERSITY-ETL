import requests         # Untuk mengirim permintaan HTTP ke API
import json             # Untuk menyimpan hasil sebagai file JSON
import os               # Untuk membuat folder (jika belum ada)

# Fungsi untuk mengambil data universitas dari API publik
def fetch_university_data(output_path):
    # Membuat folder tempat menyimpan file output jika belum ada
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # URL API JSON data universitas dari GitHub
    url = "https://raw.githubusercontent.com/Hipo/university-domains-list/master/world_universities_and_domains.json"

    # Mengirim request GET ke URL
    response = requests.get(url)

    # Jika berhasil (kode status 200)
    if response.status_code == 200:
        # Simpan hasil JSON ke file
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(response.json(), f, indent=2)
        print(f"✅ Data berhasil disimpan ke {output_path}")
    else:
        # Tampilkan pesan error jika request gagal
        print("❌ Gagal mengambil data:", response.status_code)

# Jalankan fungsi utama jika script ini dijalankan langsung
if __name__ == "__main__":
    os.makedirs("data", exist_ok=True)  # Pastikan folder 'data/' ada
    fetch_university_data("data/raw_universities.json")  # Jalankan fetch dan simpan hasil
