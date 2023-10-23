import redis


def handle_request(data):
    elevators, available_elevators = extract_data(data)

    inserted_floors = {}

    for index in available_elevators:
        planned_floors = elevators[index]

        if data.current_floor in planned_floors:
            index = planned_floors.index(data.current_floor)
        else:
            insert_user_floor(planned_floors, data.current_floor)
            index = planned_floors.index(data.current_floor)
        inserted_floors[elevators[index]] = (planned_floors, index)

    print(inserted_floors)


def extract_data(data):
    r = redis.Redis(host='localhost', port=6379, db=0)
    elevators_count = decode_element(r.get("elevators_count"))
    elevators = []
    elevator_limits = []
    available_elevator_indexes = []
    for index in range(elevators_count):
        elevator = r.lrange(f'elevator_{index + 1}', 0, -1)
        elevators.append([decode_element(floor)for floor in elevator])
        elevator_limit = r.lrange(f'elevator_{index + 1}_limits', 0, -1)
        elevator_limits.append([decode_element(limit) for limit in elevator_limit])
    for index, elevator_limit in enumerate(elevator_limits):
        if data.current_floor in inclusive_range(*elevator_limit):
            available_elevator_indexes.append(index + 1)

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




# for elevator, (planned_floors, index) in inserted_floors.items():
#     print(f"{elevator}: {planned_floors}, Inserted at index: {index}")
