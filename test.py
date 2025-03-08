def allot_rooms(college_students, room_capacities):
    """
    Allots rooms (with varying capacities) to college students using a heuristic
    that minimizes the number of rooms used overall while trying to keep each
    college's students together if possible.

    Parameters:
      college_students: dict mapping college name to number of students.
      room_capacities: list of integers representing capacity for each room.
      
    Returns:
      A list of room dictionaries with assignments.
      Each room dictionary contains:
         - "id": room index,
         - "capacity": the total capacity of the room,
         - "remaining": free space left in the room,
         - "allocations": a list of tuples (college_name, number_of_students)
           allocated to that room.
    """
    # Create a list of room objects.
    rooms = [{"id": i, "capacity": cap, "remaining": cap, "allocations": []} 
             for i, cap in enumerate(room_capacities)]
    
    # Process each college in descending order of student count.
    # This way, larger groups (which are more likely to require unsplit allocation)
    # are considered first.
    for college, count in sorted(college_students.items(), key=lambda item: item[1], reverse=True):
        # Try to find a room that can hold the entire college unsplit.
        # We choose the room with the smallest remaining capacity that still fits the group.
        best_fit = None
        min_remaining = None
        for room in rooms:
            if room["remaining"] >= count:
                if best_fit is None or room["remaining"] < min_remaining:
                    best_fit = room
                    min_remaining = room["remaining"]
                    
        if best_fit is not None:
            # Allocate the entire college to this room.
            best_fit["allocations"].append((college, count))
            best_fit["remaining"] -= count
        else:
            # If no single room can hold the entire group, split the college.
            remaining_count = count
            # Sort available rooms by descending remaining capacity
            # so that we try to use the largest available capacity first.
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


# Example usage:
if __name__ == '__main__':
    # Number of students from each college.
    college_students = {
        "College A": 35,
        "College B": 50,
        "College C": 20,
        "College D": 15,
        "College E": 80  # May require splitting since it is large.
    }
    # Each room has a different capacity.
    room_capacities = [40, 50, 30, 60]

    room_assignments = allot_rooms(college_students, room_capacities)
    
    # Print the assignments.
    for room in room_assignments:
        print(f"Room {room['id']} (Capacity: {room['capacity']}), Free space: {room['remaining']}")
        for college, allocated in room["allocations"]:
            print(f"  {college}: {allocated} students")
        print()
