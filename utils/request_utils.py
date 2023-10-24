import redis

r = redis.Redis(host='localhost', port=6379, db=0)


def handle_elevators_request():
    elevators, _ = extract_data()
    directions = []
    current_floors = []
    for el in elevators:
        directions.append(get_elevator_direction(el))
        current_floors.append(el[0])

    return current_floors, directions


def handle_floor_request(data):
    elevators, available_elevators = extract_data(data.current_floor)

    inserted_floors = {}

    for index in available_elevators:
        planned_floors = elevators[index]

        if data.current_floor in planned_floors:
            floor_index = planned_floors.index(data.current_floor)
        else:
            insert_user_floor(planned_floors, data.current_floor)
            floor_index = planned_floors.index(data.current_floor)
        inserted_floors[index+1] = (planned_floors, floor_index)

    sorted_inserted_floors = dict(sorted(inserted_floors.items(), key=lambda item: item[1][1]))
    elevator_to_go = next(iter(sorted_inserted_floors.items()))
    elevator_number = elevator_to_go[0]
    key = f'elevator_{elevator_number}'
    r.delete(key)
    r.rpush(key, *elevator_to_go[1][0])
    elevator_direction = get_elevator_direction(elevator_to_go[1][0])
    return elevator_number, elevator_direction


def extract_data(current_floor=None):
    elevators_count = decode_element(r.get("elevators_count"))
    elevators = []
    elevator_limits = []
    available_elevator_indexes = []
    for index in range(elevators_count):
        elevator = r.lrange(f'elevator_{index + 1}', 0, -1)
        elevators.append([decode_element(floor)for floor in elevator])
        elevator_limit = r.lrange(f'elevator_{index + 1}_limits', 0, -1)
        elevator_limits.append([decode_element(limit) for limit in elevator_limit])

    if current_floor:
        for index, elevator_limit in enumerate(elevator_limits):
            if current_floor in inclusive_range(*elevator_limit):
                available_elevator_indexes.append(index)

    return elevators, available_elevator_indexes


def decode_element(element):
    return int(element.decode("utf-8"))


def inclusive_range(start, end):
    return range(start, end+1)


def insert_user_floor(planned_floors, user_floor):
    if len(planned_floors) == 1:
        planned_floors.append(user_floor)
        return
    inserted = False
    for i in range(1, len(planned_floors)):
        smaller, bigger = min(planned_floors[i - 1], planned_floors[i]), max(planned_floors[i - 1], planned_floors[i])
        if user_floor in range(smaller, bigger):
            planned_floors.insert(i, user_floor)
            inserted = True
            break
    if not inserted:
        planned_floors.append(user_floor)


def get_elevator_direction(planned_floors):
    if len(planned_floors) == 1:
        return 'idle'
    elif planned_floors[0] > planned_floors[1]:
        return 'down'
    else:
        return 'up'
