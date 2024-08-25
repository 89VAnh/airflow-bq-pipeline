import os
import threading
import requests

def download_chunk(url, start, end, idx, results, output_file):
    headers = {"Range": f"bytes={start}-{end}"}
    response = requests.get(url, headers=headers, stream=True)
    chunk_file = f"{output_file}.part{idx}"
    
    with open(chunk_file, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)

    results[idx] = chunk_file
    print(f"Chunk {idx} downloaded from bytes {start} to {end}")

def combine_chunks(results, output_file, num_threads=8):
    with open(output_file, "wb") as output:
        for idx in range(num_threads):
            with open(results[idx], "rb") as f:
                output.write(f.read())
            os.remove(results[idx])

    print(f"All chunks combined into {output_file}")

def download_file(url, num_threads=8, output_file="data.ndjson"):
    response = requests.head(url)
    file_size = int(response.headers["Content-Length"])
    chunk_size = file_size // num_threads

    threads = []
    results = [None] * num_threads

    for i in range(num_threads):
        start = i * chunk_size
        end = start + chunk_size - 1 if i != num_threads - 1 else file_size - 1

        thread = threading.Thread(
            target=download_chunk, args=(url, start, end, i, results, output_file)
        )
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    combine_chunks(results, output_file, num_threads=num_threads)

def download_ndjson(**kwargs):
    url = "https://drive.usercontent.google.com/download?id=1tMln4e3vepRWsRFpv1t9Yoz1bJ5uxiZp&export=download&authuser=0&confirm=t&uuid=90c09374-90b6-4fca-8cab-88722d42d57a&at=AO7h07cEK7ZmFKrFXFU2aUiMq-O8%3A1724579469153"
    output_file = "data.ndjson"
    download_file(url, num_threads=8, output_file=output_file)