import asyncio
import aioredis


async def create_redis_config(elevators_config):
    """
    Creates the initial redis config
    :param elevators_config: The initial elevator's config
    :return:
    """
    # Connect to Redis
    r = aioredis.from_url("redis://localhost")
    # Clear Redis
    await r.flushall()
    # Set the count, the initial state and the limits for each elevator
    await r.set('elevators_count', len(elevators_config))
    for index, elevator_data in enumerate(elevators_config):
        key = f'elevator_{index + 1}'
        await r.rpush(key, *[elevator_data[0]])
        await r.rpush(key + '_limits', *elevator_data)
        # Run scripts for each of those elevators asynchronously, so they don't block the API
        asyncio.create_task(move_elevator_script(key))


async def move_elevator_script(elevator):
    """
    Async Script running with each elevator. It removes the current floor from the front of the queue every 5 seconds
    :param elevator: The current elevator
    """
    try:
        async with aioredis.from_url("redis://localhost") as r:
            while True:
                # Check if there's more than one floor in the elevator's queue
                if await r.llen(elevator) > 1:
                    # Pop the first floor from the queue
                    await r.lpop(elevator)
                await asyncio.sleep(5)
    except Exception as e:
        print(f"Error running script for Elevator {elevator}: {e}")