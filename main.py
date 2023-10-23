from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse

import schemas
from utils.config_utils import create_redis_config
from utils.request_utils import handle_request

app = FastAPI()


@app.post("/config/")
async def create_config(config: schemas.Config):
    try:
        await create_redis_config(config.elevators)
        return HTMLResponse(status_code=201)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/elevators/", response_model=schemas.Response)
def make_request(request: schemas.Request):
    handle_request(request)
    return {"elevator_number": 3, "elevator_direction": 'down'}


@app.get("/elevators/")
def check_elevators_status():
    # access all elevators and return their current floor and their direction
    # get the direction by checking the next 2 floors in the queue
    return {"elevator1": 3, "elevator2": 4}

