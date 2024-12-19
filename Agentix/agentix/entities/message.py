"""
Defines the Message class, which represents a single message in a conversation.
Each message has a role (e.g., 'user' or 'system') and content (the text of the message).
"""
from copy import deepcopy


class Message:
    """
    Represents a single message in a conversation.
    """

    def __init__(self, role: str, content: str):
        """
        Initializes a new Message instance.
        :param role: The role of the message sender (e.g., 'user', 'system').
        :param content: The text content of the message.
        """
        if role.strip() == "A":
            role = "assistant"
        self.role = role
        self.content = content

    def to_dict(self, openai=False) -> dict:
        """
        Converts the message to a dictionary format, optionally in a format suitable for OpenAI API.

        :param openai: If True, formats the dictionary for OpenAI API consumption.
        :return: A dictionary representation of the message.
        """
        """Converts the message to a dictionary."""
        return {
            'role': self.role,
            'content': self.content,
        }

    def __repr__(self):
        emoji = {
            'system': '🖥️',
            'user': '👤',
            'assistant': '🤖',
        }[self.role]

        return f"Message({emoji}:{self.content})\n"
