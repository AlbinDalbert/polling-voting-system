from flask import Flask, request, jsonify
from datetime import datetime
import json
import os
import uuid
from email_validator import validate_email, EmailNotValidError

from utils import load_data, save_data, log_action
from models import create_new_poll

app = Flask(__name__)

@app.route('/polls', methods=['POST'])
def create_poll():
    """
    Creates a new poll.
    Required in JSON body: title, description, options (list of strings), expiration
    """
    poll_data = request.get_json()
    if not poll_data or 'title' not in poll_data or 'options' not in poll_data or 'expiration' not in poll_data:
        return jsonify({"error": "Missing required fields: title, options or expiration"}), 400

    title = poll_data['title']
    description = poll_data.get('description', '')
    options = poll_data['options']
    expiration = poll_data['expiration']

    poll_id, new_poll = create_new_poll(title, description, options, expiration)

    all_data = load_data()
    all_data['polls'][poll_id] = new_poll
    save_data(all_data)
    
    return jsonify({"message": "Poll created successfully!", "poll_id": poll_id}), 201


@app.route('/polls/<poll_id>/vote', methods=['POST'])
def vote(poll_id):
    """
    Submits a vote for a specific poll option.
    Required in JSON body: option, email
    """
    all_data = load_data()
    error, poll = get_poll_from_id(all_data, poll_id)
    if error:
        return error

    if poll['status'] == 'closed':
        return jsonify({"error": "Poll closed."}), 403

    vote_data = request.get_json()
    email = vote_data.get('email')
    option = vote_data.get('option')

    error, normalized_email = email_validation(email, poll)
    if error:
        return error

    if option in poll['results']:
        poll['results'][option] += 1

    poll['voters'].append(normalized_email)

    save_data(all_data)

    return jsonify({"message": "Vote submitted"})


@app.route('/polls/<poll_id>/results', methods=['GET'])
def get_results(poll_id):
    """
    Fetches the results for a specific poll with vote counts.
    """
    all_data = load_data()
    error, poll = get_poll_from_id(all_data, poll_id)
    if error:
        return error

    return jsonify({
        "title": poll['title'],
        "description": poll['description'],
        "results": poll['results'],
        "status": poll['status']
    })


@app.route('/polls', methods=['GET'])
def get_all_polls():
    """
    A convenience endpoint to list all available polls.
    """
    all_data = load_data()
    return jsonify(all_data.get("polls", {}))

def get_poll_from_id(all_data, poll_id):
    polls = all_data.get('polls', {})

    if poll_id not in polls:
        error = jsonify({"error": f"Poll with ID {poll_id} not found"}), 404
        return error, None

    return None, polls[poll_id]


def email_validation(email, poll):
    if not email:
        log_action("register_failed", "Missing email")
        error = jsonify({"error": "Email is required"}), 400
        return error, None

    try:
        valid = validate_email(email, check_deliverability=False) # disabled DNS check
        normalized_email = valid.normalized.lower()
    except EmailNotValidError as e:
        log_action("register_failed", f"Invalid email format: {email}")
        error = jsonify({"error": str(e)}), 400
        return error, None

    if normalized_email in poll['voters']:
        log_action("register_failed", f"Duplicate email: {email}")
        error = jsonify({"error": "Email already casted a vote."}), 409
        return error, None

    return None, normalized_email



if __name__ == '__main__':
    if not os.path.exists(DATA_FILE):
        save_data({"polls": {}})
        
    app.run(debug=True)
