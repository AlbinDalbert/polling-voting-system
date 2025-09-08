from datetime import datetime, UTC
from utils import load_data, save_data, log_action

def close_expired_polls():
    """
    Checks all polls and closes any that are past their expiration date.
    """
    all_data = load_data()
    polls = all_data.get("polls", {})
    
    now_utc = datetime.now(UTC)
    
    polls_changed = False
    
    for poll_id, poll in list(polls.items()):
        if poll.get("status") == "open":
            expiration_date_str = poll['expiration_date'].rstrip("Z")
            expiration_date = datetime.fromisoformat(expiration_date_str).replace(tzinfo=UTC)

            if now_utc > expiration_date:
                poll['status'] = 'closed'
                polls_changed = True
                log_action("poll_closed", "Poll ID {poll_id} expired")

    if polls_changed:
        save_data(all_data)

if __name__ == "__main__":
    close_expired_polls()
