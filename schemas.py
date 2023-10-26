from pydantic import BaseModel
from typing import List, Literal


class Config(BaseModel):
    elevators: dict

    class Config:
        arbitrary_types_allowed = True


# ----------------------------------------------------------------------------------------------------------------------
class Request(BaseModel):
    current_floor: int


# ----------------------------------------------------------------------------------------------------------------------
class ElevatorResponse(BaseModel):
    elevator_number: int
    elevator_direction: Literal['up', 'down', 'idle']


# ----------------------------------------------------------------------------------------------------------------------
class ElevatorStatuses(BaseModel):
    elevators_info: List
