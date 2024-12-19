"""
Defines the Conversation class, which represents a sequence of messages between a user and a system.
"""
import os
import json
from copy import deepcopy
from typing import List
from .message import Message


SEP = '\n__-__\n'


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
        flags = {}
        # IF THE First message as a role `flags` then set flag_msg ,*msgs = msgs and flags = json.loads(flag_msg.content)
        if msgs[0].role == 'flags':
            flags_msg, *msgs = msgs
            flags = json.loads(flags_msg.content)
        return cls(msgs, flags)

    def to_str(self) -> str:
        flag_msg = Message(role='flags', content=json.dumps(self._flags))

        return SEP.join(f"{msg.role}:{msg.content}" for msg in [flag_msg] + self.msgs)

    def to_file(self, path: str) -> None:
        with open(path, 'w') as f:
            f.write(self.to_str())

    def openai(self) -> List[dict]:
        return [msg.to_dict(True) for msg in self.msgs]

    def to_dict(self) -> List[dict]:
        """
        Converts the conversation to a list of dictionaries, each representing a message.
        :return: A list of dictionaries with 'role' and 'content' keys.
        """
        return [{'role': msg.role, 'content': msg.content} for msg in self.msgs]

    def __init__(self, msgs: List[Message], flags: dict = None) -> None:

        def to_Message(msg: dict | Message) -> Message:
            if isinstance(msg, dict):
                return Message(**msg)
            return msg

        msgs = [to_Message(m) for m in msgs]

        flags = flags or {}
        self._msgs = msgs
        self._flags = {'should_infer': False, **flags}
        self._llm = os.getenv('AGENTIX_MODEL') or 'gpt-4o'

    @property
    def should_infer(self) -> bool:
        return self._flags.get('should_infer', False)

    @should_infer.setter
    def should_infer(self, value: bool):
        self._flags['should_infer'] = value

    @property
    def llm(self) -> str:
        return self._llm

    @llm.setter
    def llm(self, value: str):
        self._llm = value

    @property
    def msgs(self) -> List[Message]:
        return self._msgs

    @msgs.setter
    def msgs(self, msgs):
        self._msgs = msgs

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
        return Conversation(new_msgs, deepcopy(self._flags))

    def __repr__(self):
        return '\n\n______________\n\n'.join(f"{m.role}:{m.content}" for m in self.msgs)

    def __getitem__(self, key):
        if isinstance(key, int):
            # Return a single message if key is an integer
            return self._msgs[key]
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
