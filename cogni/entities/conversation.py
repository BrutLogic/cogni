"""Conversation class for managing sequences of messages."""
from typing import List, Optional
from .message import Message

class Conversation:
    """Manages a sequence of messages between participants."""
    
    def __init__(self, messages: List[Message]):
        self.messages = messages
        
    def __getitem__(self, index):
        return self.messages[index]
        
    def __len__(self):
        return len(self.messages)
        
    def add_message(self, role: str, content: str) -> None:
        """Add a new message to the conversation."""
        self.messages.append(Message(role=role, content=content))
        
    def to_dict(self) -> List[dict]:
        """Convert conversation to list of message dictionaries."""
        return [msg.to_dict() for msg in self.messages]
