# polling-voting-system

## Overview

A backend application for running polls where users can vote and view results. Built using Flask and data storage in a json file.

## Endpoints
### [POST] /polls
create a new poll.
Example:
```
curl -X POST http://127.0.0.1:5000/polls \
-H "Content-Type: application/json" \
-d '{
    "title": "Favorite Programming Language?",
    "description": "A poll for our dev team.",
    "options": ["Python", "JavaScript", "Rust"],
    "expiration": "2025-12-31"
}'
```

### [POST] /polls/<poll_id>/vote
casting a vote on a poll.
Example:
```
curl -X POST http://127.0.0.1:5000/polls/<poll_id>/vote \
-H "Content-Type: application/json" \
-d '{
    "email": "test@example.com",
    "option": "Python"
}'
```

### [GET] /polls/<poll_id>/result
get the result of a given poll
Example:
```
curl -X GET http://127.0.0.1:5000/polls/<poll_id>/results
```

### [GET] /polls
get all polls
Example:
```
curl -X GET http://127.0.0.1:5000/polls
```

## Build and Run 
*(these instructions are aimed for an linux environment)*

Prerequisites
- Python 3.12+
- pip

Clone the repository and enter the directory.
```
git clone https://github.com/AlbinDalbert/polling-voting-system.git
cd simple-expense-tracker
```

Create a virtual environment and intall the dependencies.
```
python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt
```

Run the application:
```
flask run
```
And it can now be reached at `http://127.0.0.1:5000`

For the closure of expired polls, a scheduled task has to be setup in the given deployment environtment (e.g. cron for linux). setting that up to run `scheduler.py` will make sure expired polls are getting closed.

## CI/CD
Using GitHub Actions, the test suite is automatically executed and ran on push/pull request. The pipeline is defined in `/.github/workflows`
It starts by running the `pytest` and after that, it packages the application into a .zip file.
## Decisions
For data storage and persistance, json was picked because of the 'multiple choice' requirement in the polls. The flexibility of simply using a json file makes this easier to manage. Whiles other noSQL databases can do this aswell, it would be unnessecery complexity to the scope of this project.
