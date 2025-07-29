from google.cloud import bigquery
from google.oauth2 import service_account
from prefect_gcp.credentials import GcpCredentials
import pandas as pd
import os

def load_to_bigquery(csv_path, table_id):
    # Load credentials dari Prefect Block
    gcp_block = GcpCredentials.load("gcp-cred-univ")  
    credentials = gcp_block.get_credentials_from_service_account()
    client = bigquery.Client(credentials=credentials, project=gcp_block.project)

    # Baca data baru yang ingin di-upload
    df_new = pd.read_csv(csv_path)

    # Ambil data lama dari BigQuery
    try:
        query = f"SELECT * FROM `{table_id}`"
        df_existing = client.query(query).to_dataframe()
    except Exception as e:
        print(f"⚠️ Tidak bisa mengambil data existing dari BigQuery, diasumsikan kosong. Error: {e}")
        df_existing = pd.DataFrame()

    # Bandingkan apakah ada data baru
    df_combined = pd.concat([df_existing, df_new]).drop_duplicates(keep=False)

    if df_combined.empty:
        print("⚠️ Tidak ada data baru, tidak ada perubahan di tabel BigQuery.")
    else:
        # Filter hanya baris baru
        df_only_new = pd.concat([df_new, df_existing]).drop_duplicates(keep=False)
        print(f"✅ Ada {len(df_only_new)} baris baru yang akan ditambahkan ke BigQuery.")

        # Upload data ke BigQuery
        job_config = bigquery.LoadJobConfig(
            source_format=bigquery.SourceFormat.CSV,
            skip_leading_rows=1,
            autodetect=True,
            write_disposition=bigquery.WriteDisposition.WRITE_APPEND
        )

        with open(csv_path, "rb") as source_file:
            load_job = client.load_table_from_file(source_file, table_id, job_config=job_config)

        load_job.result()
        print(f"✅ Data berhasil ditambahkan ke BigQuery table: {table_id}")