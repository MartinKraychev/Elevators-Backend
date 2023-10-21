from fastapi import FastAPI
from fastapi.responses import HTMLResponse

import redis
import json

import schemas

# Initialize Redis connection
r = redis.Redis(host='localhost', port=6379, db=0)

app = FastAPI()


@app.post("/config/")
def create_config(config: schemas.Config):
    # clear redis
    r.flushall()
    # set the limits
    r.set('elevator_limits', json.dumps(config.elevators))
    # init x amount of elevators having [min_limit,]

    # run scripts for each of those elevators that clear the front floor every x seconds and print msg

    return HTMLResponse(status_code=201)


@app.post("/elevators/", response_model=schemas.Response)
def make_request(request: schemas.Request):
    print(request)
    # get current floor and floor to go
    # get all elevators and see which one to is the best option
    # add the floor to the queue
    # return info
    return {"elevator_number": 3, "elevator_direction": 'down'}


@app.get("/elevators/")
def check_elevators_status():
    # access all elevators and return their current floor and their direction
    # get the direction by checking the next 2 floors in the queue
    return {"elevator1": 3, "elevator2": 4}

