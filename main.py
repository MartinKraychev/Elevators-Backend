from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

import schemas
from utils.config_utils import create_redis_config
from utils.request_utils import handle_floor_request, handle_elevators_request

import threading

app = FastAPI()
# Configure CORS
origins = ["http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create a mutex (lock)
db_mutex = threading.Lock()


@app.post("/config/")
async def create_config(config: schemas.Config):
    try:
        await create_redis_config(config.elevators)
        return HTMLResponse(status_code=201)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ----------------------------------------------------------------------------------------------------------------------
@app.post("/elevators/", response_model=schemas.ElevatorResponse)
def make_floor_request(request: schemas.Request):
    # We lock handling the request to avoid multiple users
    # attempting to update the same entry in the DB at the same time
    with db_mutex:
        elevator_number, elevator_direction = handle_floor_request(request)
    return {"elevator_number": elevator_number, "elevator_direction": elevator_direction}


# ----------------------------------------------------------------------------------------------------------------------
@app.get("/elevators/", response_model=schemas.ElevatorStatuses)
def check_elevators_status():
    elevators_info = handle_elevators_request()
    return {"elevators_info": elevators_info}

