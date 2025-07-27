# Mengimpor fungsi extract dan transform dari folder etl/
from etl.extract import fetch_university_data
from etl.transform import clean_university_data
from etl.load import load_to_bigquery # Import fungsi untuk mengupload data ke BigQuery
import os  # Untuk mengelola path sistem file

# Menentukan path dasar proyek (lokasi utama proyek)
BASE_PATH = "C:/PURWADHIKA/PortoUniv"

# Menentukan path ke file data mentah yang akan diambil dari API
RAW_PATH = os.path.join(BASE_PATH, "data/raw_universities.json")

# Menentukan path ke file data bersih hasil transformasi
CLEAN_PATH = os.path.join(BASE_PATH, "data/cleaned_universities.csv")

# Menjalankan proses ETL
# 1. Extract: ambil data dari API dan simpan ke JSON lokal
fetch_university_data(RAW_PATH)

# 2. Transform: bersihkan dan olah data lalu simpan ke CSV
clean_university_data(RAW_PATH, CLEAN_PATH)

# 3. Load: mengunggah data ke tabel BigQuery
# Tentukan path ke file kredensial Google Cloud (service account JSON)
GCP_CRED = os.path.join(BASE_PATH, "config/gcp_key.json")

# Tentukan ID tabel tujuan di BigQuery: project_id.dataset_id.table_id
TABLE_ID = "university-etl-project.university_data.universities"  # Ganti jika nama project atau dataset berbeda

# Jalankan fungsi untuk mengupload data ke BigQuery
load_to_bigquery(CLEAN_PATH, TABLE_ID, GCP_CRED)