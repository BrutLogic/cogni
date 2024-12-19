import pytest
from cogni.entities import Conversation, Message

def test_conversation_creation():
    """Test creating a conversation with messages."""
    msgs = [
        Message("user", "hello"),
        Message("assistant", "hi")
    ]
    conv = Conversation(msgs)
    assert len(conv) == 2
    assert conv[0].role == "user"
    assert conv[1].content == "hi"

def test_conversation_add_message():
    """Test adding messages to conversation."""
    conv = Conversation([])
    conv.add_message("user", "test")
    assert len(conv) == 1
    assert conv[0].content == "test"

def test_conversation_to_dict():
    """Test converting conversation to dictionary format."""
    conv = Conversation([
        Message("user", "hello"),
        Message("assistant", "hi")
    ])
    dict_conv = conv.to_dict()
    assert len(dict_conv) == 2
    assert dict_conv[0]["role"] == "user"
    assert dict_conv[1]["content"] == "hi"
