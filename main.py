import os
import logging
from etl.extract import fetch_university_data
from etl.transform import clean_university_data
from etl.load import load_to_bigquery

# Logging agar ada status di terminal
logging.basicConfig(level=logging.INFO)

def run_pipeline():
    BASE_PATH = "C:/PURWADHIKA/PortoUniv"
    raw_path = os.path.join(BASE_PATH, "data/raw_universities.json")
    clean_path = os.path.join(BASE_PATH, "data/cleaned_universities.csv")
    credentials = os.path.join(BASE_PATH, "config/gcp_key.json")
    table_id = "university-etl-project.university_data.universities"

    logging.info("📦 Memulai pipeline ETL untuk data universitas...")
    fetch_university_data(raw_path)
    logging.info("✅ Data berhasil diambil")

    clean_university_data(raw_path, clean_path)
    logging.info("✅ Data berhasil dibersihkan")

    load_to_bigquery(clean_path, table_id, credentials)
    logging.info("✅ Data berhasil diupload ke BigQuery")

if __name__ == "__main__":
    run_pipeline()
