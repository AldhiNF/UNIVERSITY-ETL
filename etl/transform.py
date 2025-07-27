import pandas as pd         # Untuk manipulasi dan analisis data
import json                 # Untuk membaca file JSON mentah
import os                   # Untuk operasi file dan folder

# Fungsi utama untuk membersihkan dan memperkaya data universitas
def clean_university_data(input_path, output_path):
    # Membaca file JSON dari path input
    with open(input_path, encoding='utf-8') as f:
        raw_data = json.load(f)

    # Mengubah list of dict JSON menjadi DataFrame
    df = pd.DataFrame(raw_data)

    # Memilih kolom penting saja dari data mentah
    df_clean = df[['name', 'country', 'alpha_two_code', 'domains', 'web_pages']].copy()

    # Tambahkan kolom baru: jumlah domain per universitas (jumlah elemen di list 'domains')
    df_clean['domain_count'] = df_clean['domains'].apply(lambda x: len(x))

    # Menghapus duplikat berdasarkan kombinasi nama universitas dan negaranya
    df_clean.drop_duplicates(subset=['name', 'country'], inplace=True)

    # Tambahkan kolom baru: top-level domain (misalnya: 'ac.id' → 'id')
    df_clean['top_level_domain'] = df_clean['domains'].apply(lambda x: x[0].split('.')[-1])

    # Dictionary mapping negara ke benua (continent)
    country_to_continent = {
        'United States': 'North America',
        'United Kingdom': 'Europe',
        'Indonesia': 'Asia',
        'Germany': 'Europe',
        'Brazil': 'South America',
        'India': 'Asia',
        'Canada': 'North America',
        'Australia': 'Oceania',
        'South Africa': 'Africa',
        'Japan': 'Asia',
        'France': 'Europe',
        'Nigeria': 'Africa',
        # Tambahkan lebih banyak negara jika perlu
    }

    # Tambahkan kolom 'continent' berdasarkan mapping negara → benua
    df_clean['continent'] = df_clean['country'].map(country_to_continent)

    # Buat folder output jika belum ada
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Simpan data bersih dan diperkaya ke file CSV
    df_clean.to_csv(output_path, index=False)

    # Tampilkan pesan sukses di terminal
    print(f"✅ Data bersih disimpan ke {output_path}")

# Menjalankan fungsi jika script dijalankan langsung
if __name__ == "__main__":
    os.makedirs("data", exist_ok=True)  # Pastikan folder data ada
    clean_university_data("data/raw_universities.json", "data/cleaned_universities.csv")
