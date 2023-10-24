import redis

r = redis.Redis(host='localhost', port=6379, db=0)


def handle_elevators_request():
    """
    Handles the elevator statuses requests
    :return: Elevator's current floors and their direction
    """
    elevators, _ = extract_data()
    directions = []
    current_floors = []
    for el in elevators:
        directions.append(get_elevator_direction(el))
        current_floors.append(el[0])

    return current_floors, directions


# ----------------------------------------------------------------------------------------------------------------------
def handle_floor_request(data):
    """
    Handles user interaction with the elevator
    :param data: The data from the request
    :return: Elevator number to take ,and it's direction
    """
    # Get the data from the database
    elevators, available_elevators_indexes = extract_data(data.current_floor)

    inserted_floors = {}
    # For each elevator insert the user floor where it belongs and create an index of proximity
    for index in available_elevators_indexes:
        planned_floors = elevators[index]

        if data.current_floor in planned_floors:
            floor_index = planned_floors.index(data.current_floor)
        else:
            insert_user_floor(planned_floors, data.current_floor)
            floor_index = planned_floors.index(data.current_floor)
        inserted_floors[index+1] = (planned_floors, floor_index)

    # Sort the inserted floors by the index of proximity and get the first one(the closest one)
    sorted_inserted_floors = dict(sorted(inserted_floors.items(), key=lambda item: item[1][1]))
    elevator_to_go = next(iter(sorted_inserted_floors.items()))
    # Replace the data for this elevator in the DB
    elevator_number = elevator_to_go[0]
    key = f'elevator_{elevator_number}'
    r.delete(key)
    r.rpush(key, *elevator_to_go[1][0])
    # Get the direction
    elevator_direction = get_elevator_direction(elevator_to_go[1][0])

    return elevator_number, elevator_direction


# ----------------------------------------------------------------------------------------------------------------------
def extract_data(current_floor=None):
    """
    Extracts the data from the database and if user floor is given, provide available elevator indexes
    :param current_floor: User selected floor
    :return: An list of all elevators and the indexes of the available ones
    """
    elevators_count = decode_int_element(r.get("elevators_count"))
    elevators = []
    elevator_limits = []
    available_elevator_indexes = []
    for index in range(elevators_count):
        elevator = r.lrange(f'elevator_{index + 1}', 0, -1)
        elevators.append([decode_int_element(floor) for floor in elevator])
        elevator_limit = r.lrange(f'elevator_{index + 1}_limits', 0, -1)
        elevator_limits.append([decode_int_element(limit) for limit in elevator_limit])

    if current_floor:
        for index, elevator_limit in enumerate(elevator_limits):
            if current_floor in inclusive_range(*elevator_limit):
                available_elevator_indexes.append(index)

    return elevators, available_elevator_indexes


# ----------------------------------------------------------------------------------------------------------------------
def decode_int_element(element):
    """
    Takes an element from the Redis DB and parses it to integer
    :param element: Element to decode
    :return: decoded element
    """
    return int(element.decode("utf-8"))


# ----------------------------------------------------------------------------------------------------------------------
def inclusive_range(start, end):
    """
    Utils functions to create a inclusive range
    :param start: start index
    :param end: end index
    :return: The range iterator
    """
    return range(start, end+1)


# ----------------------------------------------------------------------------------------------------------------------
def insert_user_floor(planned_floors, user_floor):
    """
    Inserts a user floor into the planned floors
    :param planned_floors: The planned floors
    :param user_floor: The user floor
    """
    # If only one floor is currently planned, just add append the user floor
    if len(planned_floors) == 1:
        planned_floors.append(user_floor)
        return
    inserted = False
    # Else, compare floors 2 by 2 and find the place to insert the floor accordingly
    for i in range(1, len(planned_floors)):
        smaller, bigger = min(planned_floors[i - 1], planned_floors[i]), max(planned_floors[i - 1], planned_floors[i])
        if user_floor in range(smaller, bigger):
            planned_floors.insert(i, user_floor)
            inserted = True
            break
    # Incase the floor can't be inserted anywhere just put it on the back of the queue
    if not inserted:
        planned_floors.append(user_floor)


# ----------------------------------------------------------------------------------------------------------------------
def get_elevator_direction(planned_floors):
    """
    Gets the elevator direction based on the first 2 floors in the queue
    :param planned_floors: The planned floors for the elevator
    :return: the direction
    """
    if len(planned_floors) == 1:
        return 'idle'
    elif planned_floors[0] > planned_floors[1]:
        return 'down'
    else:
        return 'up'
