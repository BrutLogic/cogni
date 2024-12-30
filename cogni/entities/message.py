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
        self._original_content = content

    def to_dict(self) -> dict:
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

    def parse(self, parser):
        self.content = parser(self._original_content)

    def __repr__(self):
        import shutil
        import textwrap

        terminal_width = shutil.get_terminal_size().columns
        margin = 2
        effective_width = terminal_width - 2 * margin - 4

        emoji = {
            'system': '🖥️',
            'user': '🧑‍',
            'assistant': '🤖',
        }[self.role]

        pad = {
            'user': 1,
            'system': 2,
            'assistant': 0
        }

        role_display = f"  │ {emoji}  {self.role}:".ljust(
            effective_width + 4 + pad[self.role]) + "│"
        border_top = f"  {'╭' + '─' * (effective_width + 2) + '╮'}\n"
        border_bottom = f"  {'╰' + '─' * (effective_width + 2) + '╯'}\n"

        wrapped_lines = textwrap.wrap(self.content, width=effective_width)

        content_with_margin = "\n".join(
            f"  │ {line.ljust(effective_width)} │" for line in wrapped_lines
        )

        return f"{border_top}{role_display}\n{content_with_margin}\n{border_bottom}"
