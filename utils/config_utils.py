import asyncio
import aioredis


TIME_TO_MOVE_BETWEEN_FLOORS = 10
TIME_TO_WAIT_BEFORE_NEXT_CHECK = 1


async def create_redis_config(elevators_config):
    """
    Creates the initial redis config
    :param elevators_config: The initial elevator's config
    :return:
    """
    # Connect to Redis
    r = aioredis.from_url("redis://:Pf5h6w5E4YqbIT0jj4Lk24tSH5nBNWDs@redis-15451.c242.eu-west-1-2.ec2.cloud.redislabs.com:15451")
    # Clear Redis
    await r.flushall()
    # Set the count, the initial state and the limits for each elevator
    await r.set('elevators_count', len(elevators_config))
    for index, elevator_data in elevators_config.items():
        key = f'elevator_{index}'
        await r.rpush(key, *[elevator_data[0]])
        await r.rpush(key + '_limits', *elevator_data)
        # Run scripts for each of those elevators asynchronously, so they don't block the API
        asyncio.create_task(move_elevator_script(key))


# ----------------------------------------------------------------------------------------------------------------------
async def move_elevator_script(elevator):
    """
    Async Script running with each elevator. It removes the current floor from the front of the queue every 5 seconds
    :param elevator: The current elevator
    """
    try:
        async with aioredis.from_url("redis://:Pf5h6w5E4YqbIT0jj4Lk24tSH5nBNWDs@redis-15451.c242.eu-west-1-2.ec2.cloud.redislabs.com:15451") as r:
            while True:
                # Check if there's more than one floor in the elevator's queue
                if await r.llen(elevator) > 1:
                    # wait for 10 seconds and pop the first floor from the queue
                    await asyncio.sleep(TIME_TO_MOVE_BETWEEN_FLOORS)
                    await r.lpop(elevator)
                else:
                    # Sleep for 1 second before checking again
                    await asyncio.sleep(TIME_TO_WAIT_BEFORE_NEXT_CHECK)

    except Exception as e:
        print(f"Error running script for Elevator {elevator}: {e}")