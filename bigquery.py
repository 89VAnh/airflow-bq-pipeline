from google.cloud import bigquery

def import_bigquery(**kwargs):
    gcs_uri = "gs://gcs-bucket/data/data.csv.gz"
    dataset_id = "dataset_id"
    table_id = "table_id"
    project_id = "project_id"
    client = bigquery.Client(project=project_id)

    table_ref = f"{project_id}.{dataset_id}.{table_id}"

    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.CSV,
        skip_leading_rows=1,
        autodetect=True,
        compression="GZIP"
    )

    load_job = client.load_table_from_uri(
        gcs_uri,
        table_ref,
        job_config=job_config
    )

    load_job.result()
    print(f"Loaded {load_job.output_rows} rows into {table_id}.")
