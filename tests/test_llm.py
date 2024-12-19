import pytest
from cogni.tools.llm import llm
from cogni.entities import Conversation, Message
from cogni.middlewares.llm import mock_llm, llm_chain

def test_mock_llm_string():
    """Test mock LLM with string input."""
    result = llm("hello", model="mock_llm")
    assert result == "you told hello"

def test_mock_llm_conversation():
    """Test mock LLM with conversation input."""
    conv = Conversation([Message("user", "hello")])
    result = llm(conv, model="mock_llm")
    assert len(result) == 2
    assert result[-1].content == "you told hello"

def test_mock_llm_middleware():
    """Test mock LLM middleware."""
    ctx = {}
    result = mock_llm(ctx, "test")
    assert result == "you told test"

def test_llm_chain_middleware():
    """Test configurable LLM chain middleware."""
    ctx = {"model": "mock_llm"}
    result = llm_chain(ctx, "test")
    assert result == "you told test"

def test_invalid_model():
    """Test error on invalid model."""
    with pytest.raises(NotImplementedError):
        llm("test", model="invalid_model")
