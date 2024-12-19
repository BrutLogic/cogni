import pytest
from cogni import tool, Tool

def test_tool_decorator():
    """Test that the tool decorator properly registers functions"""
    @tool
    def sample_tool():
        return "sample result"
    
    assert "sample_tool" in Tool
    assert Tool["sample_tool"]() == "sample result"

def test_tool_access():
    """Test accessing tools through the Tool container"""
    @tool 
    def another_tool(x: int) -> int:
        return x * 2
        
    assert Tool["another_tool"](5) == 10

def test_tool_nonexistent():
    """Test accessing a non-existent tool raises KeyError"""
    with pytest.raises(KeyError):
        Tool["nonexistent_tool"]

def test_tool_multiple_registration():
    """Test registering multiple tools"""
    results = []
    
    @tool
    def tool1():
        results.append(1)
        
    @tool
    def tool2():
        results.append(2)
        
    Tool["tool1"]()
    Tool["tool2"]()
    
    assert results == [1, 2]

def test_tool_with_args_kwargs():
    """Test tool with various argument types"""
    @tool
    def complex_tool(a: int, b: str = "default") -> str:
        return f"{a}-{b}"
        
    assert Tool["complex_tool"](1) == "1-default"
    assert Tool["complex_tool"](2, "custom") == "2-custom"
