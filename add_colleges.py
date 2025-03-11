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
        response = requests.post(api_url, json=entry, headers={'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc0MTY3NDM0OCwianRpIjoiYzUyMDVjNzMtYzMyNi00YThjLTk3OGUtZGFmZjFhZDQwYTEzIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjEiLCJuYmYiOjE3NDE2NzQzNDgsImNzcmYiOiI5NzdlZGMxZi04NjdjLTQ3OWQtYmZiMi03ODU1ZTU0MzU5OWYiLCJleHAiOjE3NDE2NzUyNDh9.m_R3mu6f_l6p7z3-gFjaZ2CAfti6PPLTCzg1Xz4vzHs'})
        if response.ok:
            print(f"Successfully pushed {entry['code']} to the API.")
        else:
            print(f"Failed to push {entry['code']} to the API. Status code: {response.status_code}, {response.json()}")

if __name__ == "__main__":
    file_path = '/Users/rajat/Downloads/credentials.csv'
    api_url = 'http://127.0.0.1:5000/api/college/create'
    
    data = read_csv(file_path)
    push_to_api(data, api_url)