from google.cloud import bigquery
from google.oauth2 import service_account
import pandas as pd
import os

def load_to_bigquery(csv_path, table_id, credentials_path):

    # Gunakan kredensial eksplisit dari file JSON
    credentials = service_account.Credentials.from_service_account_file(credentials_path)

    # Inisialisasi client BigQuery
    client = bigquery.Client(credentials=credentials, project=credentials.project_id)

    # Konfigurasi job upload
    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.CSV,
        skip_leading_rows=1,
        autodetect=True
    )

    # Buka file CSV dan upload ke BigQuery
    with open(csv_path, "rb") as source_file:
        load_job = client.load_table_from_file(source_file, table_id, job_config=job_config)

    # Tunggu hingga proses selesai
    load_job.result()
    print(f"✅ Data berhasil diupload ke BigQuery table: {table_id}")