from uuid import uuid4


class InMemoryDatabase:

    def __init__(self):
        self.sessions = {}
        self.messages = {}

    def create_session(self):
        session_id = str(uuid4())

        self.sessions[session_id] = {
            "session_id": session_id
        }

        self.messages[session_id] = []

        return session_id

    def get_session(self, session_id):
        return self.sessions.get(session_id)

    def save_message(self, session_id, role, content):
        self.messages[session_id].append({
            "role": role,
            "content": content
        })

    def get_messages(self, session_id):
        return self.messages.get(session_id, [])


database = InMemoryDatabase()