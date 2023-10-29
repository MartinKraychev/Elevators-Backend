# Elevators Controls Backend App with FastAPI and Redis

We're enhancing the REST service for our Elevator Controls app, which currently relies on a remote Redis instance for managing its queueing system.

In the current system, each elevator is represented as a list (or queue) within the Redis database. A background asynchronous script periodically dequeues the first item from this queue at 10-second intervals.

It's important to note that item dequeuing only occurs when there's more than one floor in the queue. To maintain data integrity, we've implemented a threading lock mechanism to ensure that only one user can manipulate the data stored in Redis at any given time.

This backend service works with the following client https://github.com/MartinKraychev/Elevators-Frontend and that needs to be set up as well.

## Configuration and start up

Clone the project

```bash
  git clone https://github.com/MartinKraychev/Elevators-Backend.git
```

Go to the project directory

```bash
  cd Elevators-Backend
```
Install Virtual env - for Windows
```bash
  pip install virtualenv
  python -m venv venv
  venv/Scripts/activate
```

```bash
  pip install -r requirements.txt
```

Start the server

```bash
  uvicorn main:app --reload
```
## API Reference

#### Set up elevators config

```http
  POST http://localhost:8000/config
```

The body is dictionary {"elevators": ${elevator_id}: [${starting_floor}, ${end_floor}]

Response is 201 Created

#### Press a floor and get an elevator coming

```http
  POST http://localhost:8000/elevators
```

The body is "current_floor": int -> from 1 to 9 which are the limits

Response is {"elevator_number": int, "elevator_direction": str}

#### Get the statuses of each elevator

```http
  Get http://localhost:8000/elevators
```

Response is {"elevators_info: []} containing the current floors and directions for each elevator




