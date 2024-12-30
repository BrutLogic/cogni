"""
Defines the Conversation class, which represents a sequence of messages between a user and a system.
"""
import os
import json
from copy import deepcopy
from typing import List
from .message import Message


SEP = '\n__-__\n'


def repr_flags(**flags):

    effective_width = 30
    margin = 10

    border_top = f"{' ' * margin}╭{'─' * effective_width}╮\n"
    border_bottom = f"{' ' * margin}╰{'─' * effective_width}╯\n"

    formatted_flags = "\n".join(
        f"{' ' * margin}│ {key.ljust(8)
                           } {str(value).ljust(effective_width - 11)} │"
        for key, value in flags.items()
    )

    return f"{border_top}{' ' * margin}│ 🏳️ flags:{' ' * (effective_width - 10)} │\n{formatted_flags}\n{border_bottom}"


repr_flags


class Conversation:
    """
    Represents a conversation, which is a sequence of messages.
    Conversations can be created from strings or files and manipulated programmatically.
    """
    @classmethod
    def from_file(cls, path: str):
        assert os.path.isfile(path), f"No conversation found at {path}"
        with open(path) as f:
            return cls.from_str(f.read())

    @classmethod
    def from_str(cls, conv_str: str) -> 'Conversation':
        msgs = [Message(role=role, content=content)
                for msg_str in conv_str.split(SEP)
                for role, content in [msg_str.strip().split(':', 1)]]
        return cls(msgs)

    def to_str(self) -> str:
        padded_SEP = '\n\n' + SEP + '\n\n'
        return f"{padded_SEP}".join(f"{msg.role}:{msg.content}" for msg in self.msgs)

    def to_file(self, path: str) -> None:
        with open(path, 'w') as f:
            f.write(self.to_str())

    def openai(self) -> List[dict]:
        return [msg.to_dict() for msg in self.msgs]

    def to_dict(self) -> List[dict]:
        """
        Converts the conversation to a list of dictionaries, each representing a message.
        :return: A list of dictionaries with 'role' and 'content' keys.
        """
        return [{'role': msg.role, 'content': msg.content} for msg in self.msgs]

    def __init__(self, msgs: List[Message]) -> None:

        def to_Message(msg: dict | Message) -> Message:
            if isinstance(msg, dict):
                return Message(**msg)
            return msg

        self.msgs = [to_Message(m) for m in msgs]
        self.llm = None
        self.should_infer = False
        self.hops = 0

    def __add__(self, other) -> 'Conversation':
        """Returns a new Conversation instance with the given message or conversation added."""
        if isinstance(other, Message):
            new_msgs = deepcopy(self.msgs) + [deepcopy(other)]
        elif isinstance(other, Conversation):
            new_msgs = deepcopy(self.msgs) + deepcopy(other.msgs)
        else:
            raise TypeError(
                "Operand must be an instance of Message or Conversation.")
        new_conv = deepcopy(self)
        new_conv.msgs = new_msgs

        return new_conv

    def __repr__(self):

        flags = repr_flags(llm=self.llm,
                           rehop=self.should_infer,
                           hops=self.hops)

        msgs = ''.join([str(m) for m in self.msgs])

        return flags + '\n' + msgs

    def __getitem__(self, key):
        if isinstance(key, int):
            # Return a single message if key is an integer
            return self.msgs[key]
            return deepcopy(self.msgs[key])
        elif isinstance(key, slice):
            # Return a new Conversation instance with a slice of messages if key is a slice
            new_msgs = deepcopy(self.msgs[key])
            new_conv = deepcopy(self)
            new_conv.msgs = new_msgs
            return new_conv
            return Conversation(new_msgs)
        else:
            raise TypeError(
                "Invalid key type. Key must be an integer or a slice.")

    def rehop(self, message_str=None, role='system'):
        new_conv = deepcopy(self)

        if message_str is not None:
            new_conv = new_conv + Message(role, message_str)
        new_conv.should_infer = True

        return new_conv
