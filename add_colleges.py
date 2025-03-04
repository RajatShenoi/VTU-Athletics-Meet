import csv
import requests

def read_csv(file_path):
    data = []
    with open(file_path, mode='r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            data.append(row)
    return data

def push_to_api(data, api_url):
    for entry in data:
        entry = {
            "code": entry["username"],
            "name": entry["college name"]
        }
        print(entry)
        response = requests.post(api_url, json=entry, headers={'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc0MTExMTUyMCwianRpIjoiZmIzMmFkMzktZDVhNi00NjNmLWE0NzMtYzQ0ZjFmY2U0MTNlIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjEiLCJuYmYiOjE3NDExMTE1MjAsImNzcmYiOiJlNDcyMDVjYi0zNTViLTRhOTYtOWFiZC00OTNjNmJmOGMyN2MiLCJleHAiOjE3NDExMTI0MjB9.XBLXtSJ6h7N1iiUlDN9_ht-QMUZJ3CkgngmliGQridc'})
        if response.ok:
            print(f"Successfully pushed {entry['code']} to the API.")
        else:
            print(f"Failed to push {entry['code']} to the API. Status code: {response.status_code}, {response.json()}")

if __name__ == "__main__":
    file_path = '/Users/rajat/Downloads/credentials.csv'
    api_url = 'http://127.0.0.1:5000/api/college/create'
    
    data = read_csv(file_path)
    push_to_api(data, api_url)