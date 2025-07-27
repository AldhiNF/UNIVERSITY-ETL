# etl-deployment/flow.py

from prefect import flow, task
from etl.extract import fetch_university_data
from etl.transform import clean_university_data
from etl.load import load_to_bigquery
import os

# Path utama proyek
BASE_PATH = "C:/PURWADHIKA/PortoUniv"

# Path file yang digunakan dalam pipeline
RAW_PATH = os.path.join(BASE_PATH, "data/raw_universities.json")
CLEAN_PATH = os.path.join(BASE_PATH, "data/cleaned_universities.csv")
CREDENTIALS_PATH = os.path.join(BASE_PATH, "config/gcp_key.json")
TABLE_ID = "university-etl-project.university_data.universities"

@flow(name="ETL Universitas")
def etl_flow():
    # Ambil data dari API
    fetch_university_data(RAW_PATH)

    # Bersihkan dan transformasi data
    clean_university_data(RAW_PATH, CLEAN_PATH)

    # Upload ke BigQuery
    load_to_bigquery(CLEAN_PATH, TABLE_ID, CREDENTIALS_PATH)

# Jika file ini dijalankan langsung, eksekusi fungsi etl_flow()
if __name__ == "__main__":
    etl_flow()