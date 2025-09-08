# polling-voting-system

## Overview

A backend application for running polls where users can vote and view results. Built using Flask and data storage in a json file.

## Endpoints
### [POST] /polls
creat a new poll.
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
It's a simple flask add. so intsalling the dependencies in `requirements.txt` and running `flask run` is sufficiant.  

## CI/CD
Using GitHub Actions, the test suite is automatically executed and ran on push/pull request. The pipeline is defined in `/.github/workflows`

## Decisions
For data storage and persistance, json was picked because of the 'multiple choice' requirement in th:e polls. The flexibility of simply using a json file makes this easier to manage. Whiles other noSQL databases can do this aswell, it would be unnessecery complexity to the scope of this project.
