"""Message class representing a single message in a conversation."""
from dataclasses import dataclass
from typing import Optional

@dataclass
class Message:
    """A single message with role and content."""
    role: str
    content: str
    
    def to_dict(self) -> dict:
        """Convert message to dictionary format."""
        return {
            "role": self.role,
            "content": self.content
        }
