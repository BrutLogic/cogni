from typing import Dict, Any, Type, TypeVar

T = TypeVar('T')

class InstancesStore(type):
    """Metaclass for storing and retrieving instances by name."""
    
    def __new__(mcs, name: str, bases: tuple, namespace: dict) -> Type:
        """Create a new class with instance storage."""
        cls = super().__new__(mcs, name, bases, namespace)
        cls._instances: Dict[str, Any] = {}
        return cls
        
    def __getitem__(cls, key: str) -> Any:
        """Get an instance by name."""
        try:
            return cls._instances[key]
        except KeyError:
            raise KeyError(f"No {cls.__name__} instance named '{key}' found")
            
    def __setitem__(cls, key: str, value: Any) -> None:
        """Store an instance by name."""
        cls._instances[key] = value
        
    def __contains__(cls, key: str) -> bool:
        """Check if an instance name exists."""
        return key in cls._instances
