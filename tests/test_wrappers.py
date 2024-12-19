import pytest
from cogni.wrappers import FuncWrapper, InstancesStore

# Test FuncWrapper
def test_func_wrapper_registration():
    """Test function registration and wrapper creation."""
    def sample_func(x: int) -> int:
        return x * 2
        
    wrapper = FuncWrapper.register(sample_func)
    assert wrapper.name == "sample_func"
    assert wrapper(5) == 10

def test_func_wrapper_custom_name():
    """Test registration with custom name."""
    def sample_func(x: int) -> int:
        return x * 2
        
    wrapper = FuncWrapper.register(sample_func, "custom_name")
    assert wrapper.name == "custom_name"
    assert wrapper(5) == 10

def test_func_wrapper_repr():
    """Test string representation."""
    def sample_func(): pass
    wrapper = FuncWrapper.register(sample_func)
    assert repr(wrapper) == "FuncWrapper['sample_func']"

# Test InstancesStore
def test_instances_store():
    """Test instance storage and retrieval."""
    class TestContainer(metaclass=InstancesStore):
        pass
        
    instance = TestContainer()
    TestContainer['test'] = instance
    
    assert TestContainer['test'] is instance
    assert 'test' in TestContainer

def test_instances_store_missing_key():
    """Test accessing non-existent instance."""
    class TestContainer(metaclass=InstancesStore):
        pass
        
    with pytest.raises(KeyError):
        _ = TestContainer['nonexistent']

def test_instances_store_multiple_classes():
    """Test isolation between different classes using InstancesStore."""
    class Container1(metaclass=InstancesStore):
        pass
        
    class Container2(metaclass=InstancesStore):
        pass
        
    Container1['test'] = 'value1'
    Container2['test'] = 'value2'
    
    assert Container1['test'] != Container2['test']
