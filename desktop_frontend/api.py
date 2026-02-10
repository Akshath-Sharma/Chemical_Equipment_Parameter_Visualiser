import requests

BASE_URL = "http://127.0.0.1:8000"

def login_request(username, password):
    return requests.post(f"{BASE_URL}/token/", json={'username': username, 'password': password})

def register_request(username, password):
    return requests.post(f"{BASE_URL}/register/", data={'username': username, 'password': password})

def upload_csv_request(file_path, token):
    headers = {'Authorization': f'Bearer {token}'}
    with open(file_path, 'rb') as f:
        return requests.post(f"{BASE_URL}/equipment/", files={'file': f}, headers=headers)

def get_history_request(token):
    headers = {'Authorization': f'Bearer {token}'}
    # We use the same equipment endpoint for history retrieval
    return requests.get(f"{BASE_URL}/equipment/", headers=headers)

def download_report_request(report_id, token):
    headers = {'Authorization': f'Bearer {token}'}
    return requests.get(f"{BASE_URL}/report/{report_id}/", headers=headers)

def download_csv_request(csv_id, token):
    headers = {'Authorization': f'Bearer {token}'}
    return requests.get(f"{BASE_URL}/csv/{csv_id}/", headers=headers)

