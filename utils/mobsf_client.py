# mobsf_client.py
import requests
import os

MOBSF_URL = "http://127.0.0.1:8000/api/v1/"
API_KEY = os.getenv("MOBSF_API_KEY", "your-key-here")

def upload_apk(filepath):
    with open(filepath, 'rb') as f:
        files = {'file': (os.path.basename(filepath), f)}
        headers = {'Authorization': API_KEY}
        response = requests.post(MOBSF_URL + 'upload', files=files, headers=headers)
    return response.json()

def scan_uploaded(scan_hash):
    headers = {'Authorization': API_KEY}
    data = {'hash': scan_hash}
    response = requests.post(MOBSF_URL + 'scan', data=data, headers=headers)
    return response.json()

def get_scan_report(scan_hash):
    headers = {'Authorization': API_KEY}
    params = {'hash': scan_hash}
    response = requests.get(MOBSF_URL + 'report_json', headers=headers, params=params)
    return response.json()

