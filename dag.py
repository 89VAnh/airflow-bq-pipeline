from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from download import download_ndjson
from convert import convert_to_csv
from upload import upload_to_gcs
from bigquery import import_bigquery

# Default arguments for DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 8, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# DAG definition
dag = DAG(
    'daily_ndjson_pipeline',
    default_args=default_args,
    description='A daily pipeline to process ndjson files',
    schedule='0 7 * * *',
    catchup=False,
    tags=['ndjson', 'data_processing']
)

# Define tasks
download_task = PythonOperator(
    task_id='download_ndjson',
    python_callable=download_ndjson,
    dag=dag,
)

convert_task = PythonOperator(
    task_id='convert_to_csv',
    python_callable=convert_to_csv,
    dag=dag,
)

upload_task = PythonOperator(
    task_id='upload_to_gcs',
    python_callable=upload_to_gcs,
    dag=dag,
)

bq_task = PythonOperator(
    task_id='bq_import',
    python_callable=import_bigquery,
    dag=dag,
)

# Task dependencies
download_task >> convert_task >> upload_task >> bq_task