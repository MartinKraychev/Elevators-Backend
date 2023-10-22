from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse

import schemas
import asyncio
import aioredis

app = FastAPI()


async def run_elevator_script(key):
    try:
        async with aioredis.from_url("redis://localhost") as r:
            while True:
                # Check if there's more than one floor in the elevator's queue
                if await r.llen(key) > 1:
                    # Pop the first floor from the queue
                    await r.lpop(key)
                await asyncio.sleep(5)  # Sleep for 5 seconds
    except Exception as e:
        print(f"Error running script for Elevator {key}: {e}")


@app.post("/config/")
async def create_config(config: schemas.Config):
    try:
        r = aioredis.from_url("redis://localhost")
        # Clear Redis
        await r.flushall()
        # Init the elevators with the current floor being the lower range of the floors
        for index, elevator_data in enumerate(config.elevators):
            key = f'elevator_{index + 1}'
            await r.rpush(key, *[elevator_data[0]])
            # Set the elevator limits
            await r.rpush(key + '_limits', *elevator_data)
            # Run scripts for each of those elevators asynchronously, so they don't block the API
            asyncio.create_task(run_elevator_script(key))
        return HTMLResponse(status_code=201)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/elevators/", response_model=schemas.Response)
def make_request(request: schemas.Request):
    print(request)
    # get current floor and floor to go
    # Algo
    # --- make sure only one client can access the algo at the same time
    # --- See elevator limits and select the elevators that match the criteria
    # --- For each elevator - extract floors and directions
    # --- For each elevator - place temporarily the new floor where it belongs and calculate time to reach that floor
    # --- Find the elevator that will get the quickest and insert that floor in the queue where it belongs
    # return the floor and the direction to the client
    # return info
    return {"elevator_number": 3, "elevator_direction": 'down'}


@app.get("/elevators/")
def check_elevators_status():
    # access all elevators and return their current floor and their direction
    # get the direction by checking the next 2 floors in the queue
    return {"elevator1": 3, "elevator2": 4}

