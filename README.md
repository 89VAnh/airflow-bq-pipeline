# Airflow Pipeline for ndjson Processing

This project sets up an Apache Airflow pipeline on a Debian 10 VPS to download, process, and upload ndjson files to Google Cloud Storage (GCS) and import them into Google BigQuery.

## Prerequisites

Before you start, make sure you have:

- **Debian 10 VPS**
- **Python 3** and `pip`
- **Google Cloud SDK** with authentication configured
- **Apache Airflow**

## Step 1: System Setup

### 1.1. Update the System

```bash
sudo apt update && sudo apt upgrade -y
```

### 1.2. Install Python and Required Libraries

```bash
sudo apt install python3-pip python3-venv -y
python3 -m venv airflow_env
source airflow_env/bin/activate
pip install apache-airflow[gcp]==2.5.0 requests google-cloud-storage google-cloud-bigquery
```

### 1.3. Install and Configure Apache Airflow

```bash
AIRFLOW_VERSION=2.5.0
PYTHON_VERSION="$(python --version | cut -d ' ' -f 2 | cut -d '.' -f 1-2)"
CONSTRAINT_URL="https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-${PYTHON_VERSION}.txt"
pip install "apache-airflow[gcp]==${AIRFLOW_VERSION}" --constraint "${CONSTRAINT_URL}"
```

### 1.4. Initialize Airflow Database

```bash
airflow db init
```

### 1.5. Create an Admin User for Airflow

```bash
airflow users create \
    --username admin \
    --firstname Admin \
    --lastname User \
    --role Admin \
    --email admin@example.com \
    --password admin
```

### 1.6. Start Airflow Webserver and Scheduler

```bash
airflow webserver --port 8080
airflow scheduler
```

## Step 2: Configure the DAG 
### 2.1. Create Python Files for DAG Tasks

Create the following files in your project directory:

* `dag.py`: Define the Airflow DAG and tasks.
* `download.py`: Handles downloading ndjson files in chunks.
* `convert.py`: Converts ndjson files to gzipped CSV format.
* `upload.py`: Uploads the gzipped CSV to Google Cloud Storage and sets a lifecycle policy.
* `bigquery.py`: Imports the CSV data from GCS into BigQuery.

### 2.2. Place Files in Airflow's DAG Folder

Move the created Python files to Airflow’s DAGs folder, typically located at ~/airflow/dags/.

## Step 3: Verify and Test

1. Access Airflow Web Interface

    Open a web browser and navigate to `http://<your-vps-ip>:8080`(`http://localhost:8080`). Log in using the admin credentials created earlier.

2. Trigger the DAG

    In the Airflow UI, you should see the `daily_ndjson_pipeline` DAG. Trigger it manually to ensure everything is working as expected.

3. Check Logs

    Monitor the logs for each task to ensure they are running without errors. Logs can be accessed from the Airflow UI.

# Manual Execution of ndjson Processing Pipeline

This guide provides instructions to manually run each step of the ndjson processing pipeline. You need to execute the following Python scripts in sequence to download, process, and upload ndjson files, and then import the data into Google BigQuery.

## Prerequisites

Ensure you have:

- **Python 3** installed with necessary libraries (`requests`, `google-cloud-storage`, `google-cloud-bigquery`)
- **Google Cloud SDK** authenticated and configured

## Manual Execution Steps

### 1. Download ndjson File

Run the `download.py` script to download the ndjson file from the specified URL.

```bash
python download.py
```

### 2. Convert ndjson to CSV

Run the `convert.py` script to convert the downloaded ndjson file into a gzipped CSV format.

```bash
python convert.py
```

### 3. Upload CSV to Google Cloud Storage

Run the `upload.py` script to upload the gzipped CSV file to Google Cloud Storage (GCS).

```bash
python upload.py
```

### 4. Import Data into Google BigQuery

Run the `bigquery.py` script to import the CSV file from GCS into Google BigQuery.

```bash
python bigquery.py
```