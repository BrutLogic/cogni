import pytest
from cogni.wrappers import MW, InstancesStore

def test_mw_registration():
    """Test middleware registration and wrapper creation."""
    @MW.register
    def sample_mw(ctx, conv):
        return conv + "_processed"
        
    assert "sample_mw" in MW
    assert MW["sample_mw"]({"test": True}, "input") == "input_processed"

def test_mw_custom_name():
    """Test registration with custom name."""
    @MW.register
    def sample_mw(ctx, conv, extra=""):
        return conv + extra
        
    wrapper = MW.register(sample_mw, "custom_name")
    assert wrapper.name == "custom_name"
    assert wrapper({"test": True}, "input", "_modified") == "input_modified"

def test_mw_repr():
    """Test string representation."""
    @MW.register
    def sample_mw(ctx, conv): pass
    assert repr(MW["sample_mw"]) == "MW['sample_mw']"

def test_mw_multiple_registration():
    """Test registering multiple middleware."""
    results = []
    
    @MW.register
    def mw1(ctx, conv):
        results.append(1)
        return conv
        
    @MW.register 
    def mw2(ctx, conv):
        results.append(2)
        return conv
        
    MW["mw1"]({"test": True}, "input")
    MW["mw2"]({"test": True}, "input")
    
    assert results == [1, 2]

def test_mw_chaining():
    """Test chaining multiple middleware."""
    @MW.register
    def add_a(ctx, conv):
        return conv + "a"
        
    @MW.register
    def add_b(ctx, conv):
        return conv + "b"
        
    result = add_b({"test": True}, add_a({"test": True}, "input"))
    assert result == "inputab"
