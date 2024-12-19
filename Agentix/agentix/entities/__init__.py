from .conversation import Conversation
from .message import Message

from pydantic import BaseModel
from typing import Optional


class ModuleInfo(BaseModel):
    name: str
    author: str
    version: str
    description: str
    agent: bool
    endpoints: bool
    widget: bool
    widget_type: Optional[str] = None
    module_path: Optional[str] = None
