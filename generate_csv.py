import requests
import csv
import os

def fetch_data():
    url = 'http://127.0.0.1:5000/api/college/report'
    headers = {
        'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc0MTY2MDUyMCwianRpIjoiMjYxMDdiYjEtYzBiNC00NGFhLWIzNzItMzYwODJhYTA2ZmFlIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjEiLCJuYmYiOjE3NDE2NjA1MjAsImNzcmYiOiIwYjQ1ZmJhMC1iZWU3LTRkNzMtYWIyZC1iYTc0ODYzYmVlNmEiLCJleHAiOjE3NDE2NjE0MjB9.iplqCfl8OMz3kQd-K856mKhQG0TAjEHIe-OZP5F55Cw'
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

def save_to_csv(data, file_path):
    with open(file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['College Code', 'Location', 'Room Number', 'Occupied By College Count', 'Max Occupancy'])
        for row in data['report']:
            college_code = row['college_code']
            for room in row['rooms']:
                writer.writerow([college_code, room['location'], room['number'], room['occupied_by_college_count'], room['max_occupancy']])


def main():
    data = fetch_data()
    downloads_path = os.path.join(os.path.expanduser('~'), 'Downloads', 'College Allotment.csv')
    save_to_csv(data, downloads_path)
    print(f"Data saved to {downloads_path}")

if __name__ == "__main__":
    main()