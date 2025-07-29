from prefect import flow
from etl.extract import fetch_university_data
from etl.transform import clean_university_data
from etl.load import load_to_bigquery
import os

BASE_PATH = "C:/PURWADHIKA/PortoUniv"
RAW_PATH = os.path.join(BASE_PATH, "data/raw_universities.json")
CLEAN_PATH = os.path.join(BASE_PATH, "data/cleaned_universities.csv")
GCP_CRED = os.path.join(BASE_PATH, "config/gcp_key.json")
TABLE_ID = "university-etl-project.university_data.universities"

@flow(name="etl_flow")  # ⬅️ wajib pakai ini agar Prefect bisa mengenali
def etl_flow():
    fetch_university_data(RAW_PATH)
    clean_university_data(RAW_PATH, CLEAN_PATH)
    load_to_bigquery(CLEAN_PATH, TABLE_ID, GCP_CRED)

# Untuk testing lokal (opsional)
if __name__ == "__main__":
    etl_flow()