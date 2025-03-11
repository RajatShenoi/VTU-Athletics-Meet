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
            "Bhadra": 2,
            "Tunga": 3,
            "Krishna": 4,
            "Mess Rooms": 5,
            "Guest House": 6
        }

        entry["location_id"] = ids[entry["location_id"]]

        response = requests.post(api_url, json=entry, headers={'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc0MTY3NDU4MCwianRpIjoiZDcxOWUyNDktYjI4MC00ZmE5LWJjMDctMmIyOTg0ZWU2ZWJjIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjEiLCJuYmYiOjE3NDE2NzQ1ODAsImNzcmYiOiJkYjQzODZkZS1mMjQ4LTQzM2UtYjE2YS04ZDA4MmM1ZDNmODUiLCJleHAiOjE3NDE2NzU0ODB9.XIGShRSbFHTGj5Wa8EwsHbf5bn7gsPcR2upIRlWs1cU'})
        if response.ok:
            print(f"Successfully pushed {entry['location_id']}, {entry['number']} to the API.")
        else:
            print(f"Failed to push {entry['location_id']}, {entry['number']} to the API. Status code: {response.status_code}, {response.json()}")

if __name__ == "__main__":
    file_path = '/Users/rajat/Downloads/hostel_data.csv'
    api_url = 'http://127.0.0.1:5000/api/room/create'
    
    data = read_csv(file_path)
    push_to_api(data, api_url)