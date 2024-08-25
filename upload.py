import os
from google.cloud import storage
from concurrent.futures import ThreadPoolExecutor

def upload_part(bucket_name, file_path, destination_blob_name, start_byte, end_byte):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    
    with open(file_path, 'rb') as file:
        file.seek(start_byte)
        blob.upload_from_file(file, size=end_byte - start_byte)

def split_and_upload_to_gcs(file_path, bucket_name, destination_blob_name, chunk_size=50 * 1024 * 1024):
    file_size = os.path.getsize(file_path)
    part_number = 0
    futures = []

    with ThreadPoolExecutor() as executor:
        for start_byte in range(0, file_size, chunk_size):
            end_byte = min(start_byte + chunk_size, file_size)
            part_blob_name = f"{destination_blob_name}.part{part_number}"
            futures.append(executor.submit(upload_part, bucket_name, file_path, part_blob_name, start_byte, end_byte))
            part_number += 1
        
        for future in futures:
            future.result()

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blobs = [bucket.blob(f"{destination_blob_name}.part{i}") for i in range(part_number)]
    bucket.blob(destination_blob_name).compose(blobs)

    for blob in blobs:
        blob.delete()

def setup_gcs_lifecycle_policy(bucket_name):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)

    rule = {
        "action": {"type": "SetStorageClass", "storageClass": "COLDLINE"},
        "condition": {"age": 30}
    }
    bucket.lifecycle_rules.append(rule)
    bucket.patch()

def upload_to_gcs(**kwargs):
    split_and_upload_to_gcs('/tmp/data.csv.gz', 'gcs-bucket', 'data/data.csv.gz')
    setup_gcs_lifecycle_policy('gcs-bucket')
