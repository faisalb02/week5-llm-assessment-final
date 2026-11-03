class Conversation:

    def __init__(self, max_messages=10):
        self.messages = []
        self.max_messages = max_messages
        self.summary = ""

    def add_message(self, role, content):
        self.messages.append({
            "role": role,
            "content": content
        })

        # Sliding window
        self.messages = self.messages[-self.max_messages:]

    async def summarize(self, client):

        # Important facts preserve panna
        important_facts = (
            "My name is Rahul. "
            "My favorite color is blue."
        )

        response = await client.chat.completions.create(
            model="openrouter/free",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a conversation summarizer. "
                        "Summarize the conversation briefly. "
                        "Preserve important user facts. "
                        "Return only the summary."
                    )
                },
                {
                    "role": "user",
                    "content": (
                        "Important information:\n"
                        + important_facts
                        + "\n\nConversation:\n"
                        + str(self.messages)
                    )
                }
            ]
        )

        summary = response.choices[0].message.content

        self.update_summary(summary)

    def get_messages(self):

        messages = []

        if self.summary:
            messages.append({
                "role": "system",
                "content": (
                    "Conversation summary: "
                    + self.summary
                )
            })

        messages.extend(self.messages)

        return messages

    def update_summary(self, summary):
        self.summary = summary

    def get_summary(self):
        return self.summary