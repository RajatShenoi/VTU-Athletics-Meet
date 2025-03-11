import csv
import requests
from termcolor import colored

def get_rooms(api_url, jwt_token):
    headers = {
        "Authorization": f"Bearer {jwt_token}",
        "Content-Type": "application/json"
    }
    response = requests.get(api_url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        rooms = [{
            "id": room["id"],
            "capacity": room["max_occupancy"],
            "remaining": room["max_occupancy"],
            "location": room["location"],
            "number": room["number"],
            "allocations": []
        } for room in data.get("rooms", [])]
        return rooms
    else:
        raise Exception("Failed to retrieve rooms: " + response.text)

def post_allocation(api_url, jwt_token, college_id, room_id, gender, count):
    headers = {
        "Authorization": f"Bearer {jwt_token}",
        "Content-Type": "application/json"
    }
    payload = {
        "college_id": college_id,
        "room_id": room_id,
        "gender": gender,
        "count": count
    }

    for _ in range(count):
        response = requests.post(api_url, headers=headers, json=payload)
        if response.status_code != 200:
            print(f"{college_id}: Failed to post allocation: {response.text}")

def allot_rooms(college_students, rooms, api_url, jwt_token):
    for college, counts in sorted(college_students.items(), key=lambda x: sum(x[1]), reverse=True):
        male_count, female_count = counts

        if female_count > 0:
            female_rooms = [room for room in rooms if room["location"] == "Krishna (Girls)"]
            female_rooms = sorted(female_rooms, key=lambda r: r["remaining"], reverse=True)
            remaining_female_count = female_count
            for room in female_rooms:
                if remaining_female_count <= 0:
                    break
                if room["remaining"] > 0:
                    allocate = min(room["remaining"], remaining_female_count)
                    room["allocations"].append((college, allocate, "Female"))
                    room["remaining"] -= allocate
                    remaining_female_count -= allocate
                    post_allocation(api_url, jwt_token, college, room["id"], "Female", allocate)
            if remaining_female_count > 0:
                print(colored(f"Warning: Female students from {college}, {remaining_female_count} students unassigned.", "yellow"))

        if male_count > 0:
            male_rooms = [room for room in rooms if room["location"] not in ["Krishna (Girls)", "Sharavathi (Managers)", "Mess Rooms (Ladies Managers)", "Guest House (Managers)"]]
            male_rooms = sorted(male_rooms, key=lambda r: r["remaining"], reverse=True)
            remaining_male_count = male_count
            for room in male_rooms:
                if remaining_male_count <= 0:
                    break
                if room["remaining"] > 0:
                    allocate = min(room["remaining"], remaining_male_count)
                    room["allocations"].append((college, allocate, "Male"))
                    room["remaining"] -= allocate
                    remaining_male_count -= allocate
                    post_allocation(api_url, jwt_token, college, room["id"], "Male", allocate)
            if remaining_male_count > 0:
                print(f"Warning: Not enough room capacity to allocate all male students from {college}. {remaining_male_count} students unassigned.")

    return rooms

def read_college_students_from_csv(csv_file):
    college_students = {}
    with open(csv_file, mode='r') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            college_code = row[0]
            male_students = int(row[2])
            female_students = int(row[3])
            college_students[college_code] = (male_students, female_students)
    return college_students

if __name__ == '__main__':
    api_url = "http://127.0.0.1:5000/api/room/list"
    jwt_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc0MTY3NDYyNywianRpIjoiOTRiMzZlZmYtODZlNS00MzMzLTlmYTMtMGRjNTIzNDYxMWExIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjEiLCJuYmYiOjE3NDE2NzQ2MjcsImNzcmYiOiI4NjY5YjRlMi0yYjcxLTRjZDAtOTBlYi04MWIzN2Q3MDkzZDYiLCJleHAiOjE3NDE2NzU1Mjd9.peCEmwagNpmoqTLyHEs3icJelw5ehq20LIbZ5iXKpJ0"
    csv_file = "collegewise_participants.csv"
    post_api_url = "http://127.0.0.1:5000/api/student/checkin"
    
    try:
        rooms = get_rooms(api_url, jwt_token)
    except Exception as e:
        print("Error retrieving rooms:", e)
        exit(1)
    
    college_students = read_college_students_from_csv(csv_file)
    
    rooms = allot_rooms(college_students, rooms, post_api_url, jwt_token)
    
    for room in rooms:
        print(f"Location: {room['location']} || Room {room['number']} || (Capacity: {room['capacity']}) || Free space: {room['remaining']}")
        for allocation in room["allocations"]:
            college, allocated, gender = allocation
            print(f"  {college} ({gender}): {allocated} students")
        print()
