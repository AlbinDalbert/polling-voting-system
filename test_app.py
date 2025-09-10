import pytest
import json
import os
from app import app
from utils import save_data, load_data, DATA_FILE


@pytest.fixture
def client():
    """Create a test client for the Flask app."""
    save_data({"polls": {}})
    with app.test_client() as client:
        yield client

    os.remove(DATA_FILE)

# --- Test Cases ---

def test_create_poll_success(client):
    """
    Test successful poll creation (POST /polls).
    """
    new_poll_data = {
        "title": "What is your favorite color?",
        "description": "A simple color poll.",
        "options": ["Red", "Green", "Blue"],
        "expiration": "2025-10-09"
    }

    response = client.post('/polls', json=new_poll_data)

    assert response.status_code == 201
    response_data = response.get_json()
    assert "message" in response_data
    assert "poll_id" in response_data

def test_get_all_polls_initially_empty(client):
    """
    Test that getting all polls returns an empty object initially (GET /polls).
    """
    response = client.get('/polls')
    
    assert response.status_code == 200
    assert response.get_json() == {}

def test_vote_on_nonexistent_poll(client):
    """
    Test voting on a poll that does not exist fails correctly (POST /polls/<poll_id>/vote).
    """
    vote_data = {"email": "test@example.com", "option": "Python"}
    
    response = client.post('/polls/nonexistent123/vote', json=vote_data)
    
    assert response.status_code == 404

def test_get_results_for_nonexistent_poll(client):
    """
    Test getting results for a poll that does not exist fails correctly (GET /polls/<poll_id>/results). [cite: 63]
    """
    response = client.get('/polls/nonexistent123/results')
    
    assert response.status_code == 404

def test_email_validation(client):
    """
    Test getting results for a poll that does not exist fails correctly (GET /polls/<poll_id>/results). [cite: 63]
    """
    response = client.get('/polls/nonexistent123/results')
    
    assert response.status_code == 404

def test_vote_casting_and_results_verification(client):
    """
    Test the full flow: create a poll, cast a valid vote, and verify the results.
    """
    # setup
    new_poll_data = {
        "title": "Favorite Cloud Provider?",
        "description": "Vote for the cloud you use most.",
        "options": ["AWS", "GCP", "Azure"],
        "expiration": "2025-10-09"
    }
    response = client.post('/polls', json=new_poll_data)
    assert response.status_code == 201
    poll_id = response.get_json()['poll_id']

    # test
    vote_data = {"email": "sandra@example.com", "option": "GCP"}
    response = client.post(f'/polls/{poll_id}/vote', json=vote_data)
    
    assert response.status_code == 200
    assert response.get_json()['message'] == "Vote submitted"

    response = client.get(f'/polls/{poll_id}/results')
    assert response.status_code == 200
    results = response.get_json()['results']
    
    assert results['GCP'] == 1
    assert results['AWS'] == 0
    assert results['Azure'] == 0

def test_vote_casting_on_closed_polls(client):
    """
    Test the full flow: create a poll, cast a valid vote, and verify the results.
    """
    # setup
    new_poll_data = {
        "title": "Favorite Cloud Provider?",
        "description": "Vote for the cloud you use most.",
        "options": ["AWS", "GCP", "Azure"],
        "expiration": "2025-08-09",
    }

    response = client.post('/polls', json=new_poll_data)
    assert response.status_code == 201
    poll_id = response.get_json()['poll_id']

    all_data = load_data()
    all_data['polls'][poll_id]['status'] = 'closed' # polls can't be initsialized as closed, so we update it here instead.
    save_data(all_data)

    # test
    vote_data = {"email": "sandra@example.com", "option": "GCP"}
    response = client.post(f'/polls/{poll_id}/vote', json=vote_data)
    
    assert response.status_code == 403
    assert response.get_json()['error'] == "Poll closed."

    response = client.get(f'/polls/{poll_id}/results')
    assert response.status_code == 200
    results = response.get_json()['results']
    
    assert results['GCP'] == 0
    assert results['AWS'] == 0
    assert results['Azure'] == 0

def test_email_validation_and_duplication(client):
    """
    Test the full flow: create a poll, cast a valid vote, and verify the results.
    """
    # setup
    new_poll_data = {
        "title": "Favorite Cloud Provider?",
        "description": "Vote for the cloud you use most.",
        "options": ["AWS", "GCP", "Azure"],
        "expiration": "2025-10-09"
    }
    response = client.post('/polls', json=new_poll_data)
    assert response.status_code == 201
    poll_id = response.get_json()['poll_id']

    # test
    vote_data = {"email": "sandra@example.com", "option": "GCP"}
    response = client.post(f'/polls/{poll_id}/vote', json=vote_data)

    assert response.status_code == 200
    assert response.get_json()['message'] == "Vote submitted"
    
    vote_data = {"email": "saNDra@EXAMPle.com", "option": "GCP"}
    response = client.post(f'/polls/{poll_id}/vote', json=vote_data)
    
    assert response.status_code == 409
    assert response.get_json()['error'] == "Email already casted a vote."

    response = client.get(f'/polls/{poll_id}/results')
    assert response.status_code == 200
    results = response.get_json()['results']
    
    assert results['GCP'] == 1
    assert results['AWS'] == 0
    assert results['Azure'] == 0
