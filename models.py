from datetime import datetime, timedelta
import uuid

def create_new_poll(title: str, description: str, options: list, expiration: str) -> dict:
    """
    Creates a dictionary for a new poll with a default structure.
    """
    now = datetime.utcnow()
    expiration_dt = datetime.strptime(expiration, '%Y-%m-%d')
    
    poll_id = str(uuid.uuid4())

    poll_structure = {
        "title": title,
        "description": description,
        "options": options,
        "created_at": now.isoformat() + "Z",
        "expiration_date": expiration_dt.isoformat() + "Z",
        "status": "open",
        "results": {option: 0 for option in options},
        "voters": []
    }
    
    return poll_id, poll_structure
