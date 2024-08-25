import gzip
import csv
import json

def convert_to_csv(**kwargs):
    input_file = '/tmp/data.ndjson'
    output_file = '/tmp/data.csv.gz'

    with gzip.open(output_file, 'wt', newline='') as gzfile:
        writer = csv.writer(gzfile)
        with open(input_file, 'r') as f:
            for line in f:
                data = json.loads(line)
                writer.writerow(data.values())
