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
            "location_id": entry["Hostel name"],
            "number": entry["Room No"],
            "max_occupancy": entry["Max Capacity"]
        }

        ids = {
            "Sharavathi": 1,
            "Krishna": 2,
            "Bhadra": 3,
            "Tunga": 4
        }

        entry["location_id"] = ids[entry["location_id"]]

        response = requests.post(api_url, json=entry)
        if response.ok:
            print(f"Successfully pushed {entry['location_id']}, {entry['number']} to the API.")
        else:
            print(f"Failed to push {entry['location_id']}, {entry['number']} to the API. Status code: {response.status_code}, {response.json()}")

if __name__ == "__main__":
    file_path = '/Users/rajat/Downloads/hostel_data.csv'
    api_url = 'http://127.0.0.1:5000/api/room/create'
    
    data = read_csv(file_path)
    push_to_api(data, api_url)