elevator_data = {
    "elevator1": [1, 5, 7],
    "elevator2": [3, 4, 5],
    "elevator3": [7, 5, 4],
    "elevator4": [4, 3, 1],
    "elevator5": [2, 4, 6],
    "elevator6": [8, 9, 10],
    "elevator7": [3],  # An elevator with only one floor
}

user_floor = 3

inserted_floors = {}

# def insert_user_floor(planned_floors, user_floor):
#     if len(planned_floors) == 1:
#         planned_floors.append(user_floor)
#         return
#     inserted = False
#     for i in range(1, len(planned_floors)):
#         smaller, bigger = min(planned_floors[i - 1], planned_floors[i]), max(planned_floors[i - 1], planned_floors[i])
#         if user_floor in range(smaller, bigger):
#             planned_floors.insert(i, user_floor)
#             inserted = True
#             break
#     if not inserted:
#         planned_floors.append(user_floor)
#
# for elevator, planned_floors in elevator_data.items():
#     if user_floor in planned_floors:
#         index = planned_floors.index(user_floor)
#     else:
#         insert_user_floor(planned_floors, user_floor)
#         index = planned_floors.index(user_floor)
#     inserted_floors[elevator] = (planned_floors, index)
#
# for elevator, (planned_floors, index) in inserted_floors.items():
#     print(f"{elevator}: {planned_floors}, Inserted at index: {index}")