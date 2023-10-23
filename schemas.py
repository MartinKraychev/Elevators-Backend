from pydantic import BaseModel
from typing import List, Literal


class Config(BaseModel):
    elevators: List

    class Config:
        arbitrary_types_allowed = True


class Request(BaseModel):
    current_floor: int


class Response(BaseModel):
    elevator_number: int
    elevator_direction: Literal['up', 'down', 'idle']
