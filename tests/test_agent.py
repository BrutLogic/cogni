import pytest
from cogni.wrappers import Agent, MW

def test_agent_registration():
    """Test agent registration and creation."""
    agent = Agent("test_agent", "mw1|mw2")
    assert "test_agent" in Agent
    assert agent.name == "test_agent"

def test_agent_middleware_chain():
    """Test middleware chain execution."""
    results = []
    
    @MW.register
    def mw1(ctx, conv):
        results.append(1)
        return conv + "_mw1"
        
    @MW.register
    def mw2(ctx, conv):
        results.append(2)
        return conv + "_mw2"
        
    agent = Agent("test_chain", "mw1|mw2")
    result = agent("input")
    
    assert results == [1, 2]
    assert result == "input_mw1_mw2"

def test_agent_context():
    """Test context passing through middleware chain."""
    @MW.register 
    def ctx_test(ctx, conv):
        assert ctx["agent"].name == "ctx_agent"
        assert ctx["args"] == ("test_input",)
        assert ctx["hops"] == 0
        return conv
        
    agent = Agent("ctx_agent", "ctx_test")
    agent("test_input")

def test_agent_repr():
    """Test string representation."""
    agent = Agent("repr_test", "mw1|mw2")
    assert repr(agent) == "Agent['repr_test']"
