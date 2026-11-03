from uuid import uuid4

sessions = {}
messages = {}


def create_session():
    session_id = str(uuid4())
    sessions[session_id] = {"session_id": session_id}
    messages[session_id] = []
    return session_id


def get_session(session_id):
    return sessions.get(session_id)


def save_message(session_id, role, content):
    if session_id not in messages:
        messages[session_id] = []

    messages[session_id].append({
        "role": role,
        "content": content
    })


def get_messages(session_id):
    return messages.get(session_id, [])