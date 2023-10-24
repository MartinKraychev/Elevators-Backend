from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse

import schemas
from utils.config_utils import create_redis_config
from utils.request_utils import handle_floor_request, handle_elevators_request

app = FastAPI()


@app.post("/config/")
async def create_config(config: schemas.Config):
    try:
        await create_redis_config(config.elevators)
        return HTMLResponse(status_code=201)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/elevators/", response_model=schemas.ElevatorResponse)
def make_floor_request(request: schemas.Request):
    elevator_number, elevator_direction = handle_floor_request(request)
    return {"elevator_number": elevator_number, "elevator_direction": elevator_direction}


@app.get("/elevators/")
def check_elevators_status():
    elevator_floors, elevator_directions = handle_elevators_request()
    return {"elevator_floors": elevator_floors, "elevator_directions": elevator_directions}

