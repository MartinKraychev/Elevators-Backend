from fastapi import FastAPI
from fastapi.responses import HTMLResponse

import schemas

app = FastAPI()


@app.post("/config/")
def create_config(config: schemas.Config):
    print(config.elevators)
    return HTMLResponse(status_code=201)


@app.post("/elevators/", response_model=schemas.Response)
def make_request(request: schemas.Request):
    print(request)
    return {"elevator_number": 3, "elevator_direction": 'down'}


@app.get("/elevators/")
def check_elevators_status():
    return {"elevator1": 3, "elevator2": 4}

