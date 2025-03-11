import requests

def get_rooms(api_url, jwt_token):
    """
    Retrieves the list of rooms from the API using JWT authentication.
    Expects a JSON response of the form:
      {"rooms": [{"id": 1, "max_occupancy": 2}, ...]}
    
    Returns a list of room dictionaries, each augmented with:
      - capacity: the max occupancy (from API)
      - remaining: initially equal to capacity
      - allocations: an empty list to later store allocations
    """
    headers = {
        "Authorization": f"Bearer {jwt_token}",
        "Content-Type": "application/json"
    }
    response = requests.get(api_url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        # Transform the room list from API to our internal representation.
        rooms = [{
            "id": room["id"],
            "capacity": room["max_occupancy"],
            "remaining": room["max_occupancy"],
            "allocations": []
        } for room in data.get("rooms", [])]
        return rooms
    else:
        raise Exception("Failed to retrieve rooms: " + response.text)

def allot_rooms(college_students, rooms):
    """
    Allots rooms (with varying capacities) to college students.
    
    For each college, the function first tries to find a room that can fit
    all students unsplit. If none exists, it splits the allocation across
    multiple rooms using a greedy approach.
    
    Parameters:
      college_students: dict mapping college name to number of students.
      rooms: list of room dictionaries with keys "id", "capacity", "remaining", and "allocations".
    
    Returns:
      The rooms list with allocations added.
    """
    # Process each college in descending order of student count.
    for college, count in sorted(college_students.items(), key=lambda x: x[1], reverse=True):
        # Attempt unsplit allocation: find a room that can fit the whole college.
        best_fit = None
        min_remaining = None
        for room in rooms:
            if room["remaining"] >= count:
                if best_fit is None or room["remaining"] < min_remaining:
                    best_fit = room
                    min_remaining = room["remaining"]
                    
        if best_fit is not None:
            # Allocate entire college in one room.
            best_fit["allocations"].append((college, count))
            best_fit["remaining"] -= count
        else:
            # No single room can hold the whole group, so split allocation.
            remaining_count = count
            # Sort rooms by descending available space.
            available_rooms = sorted(
                [room for room in rooms if room["remaining"] > 0],
                key=lambda r: r["remaining"],
                reverse=True
            )
            for room in available_rooms:
                if remaining_count <= 0:
                    break
                if room["remaining"] > 0:
                    allocate = min(room["remaining"], remaining_count)
                    room["allocations"].append((college, allocate))
                    room["remaining"] -= allocate
                    remaining_count -= allocate
            if remaining_count > 0:
                print(f"Warning: Not enough room capacity to allocate all students from {college}. {remaining_count} students unassigned.")
    return rooms

if __name__ == '__main__':
    # Replace with your actual API endpoint and JWT token.
    api_url = "https://example.com/api/rooms"
    jwt_token = "your_jwt_token_here"
    
    try:
        rooms = get_rooms(api_url, jwt_token)
    except Exception as e:
        print("Error retrieving rooms:", e)
        exit(1)
    
    # Example dictionary of college students.
    college_students = {
        "College A": 35,
        "College B": 50,
        "College C": 20,
        "College D": 15,
        "College E": 80  # This may need splitting.
    }
    
    # Allocate students to the retrieved rooms.
    rooms = allot_rooms(college_students, rooms)
    
    # Print out room assignments.
    for room in rooms:
        print(f"Room {room['id']} (Capacity: {room['capacity']}), Free space: {room['remaining']}")
        for allocation in room["allocations"]:
            college, allocated = allocation
            print(f"  {college}: {allocated} students")
        print()
