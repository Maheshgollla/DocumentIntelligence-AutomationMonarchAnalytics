import requests

def scan_file_with_attachmentav(file_path, api_key):
    url = "https://eu.developer.attachmentav.com/v1/scan/sync/binary"
    headers = {"x-api-key": api_key, "Content-Type": "application/octet-stream"}
    with open(file_path, "rb") as f:
        file_content = f.read()
    response = requests.post(url, headers=headers, data=file_content, timeout=60)
    return response.json()
