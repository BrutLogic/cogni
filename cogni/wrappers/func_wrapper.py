from typing import Any, Callable
from .instances_store import InstancesStore

class FuncWrapper(metaclass=InstancesStore):
    """Base wrapper class for functions that provides registration and access."""
    
    @classmethod
    def register(cls, func: Callable, name: str = None) -> 'FuncWrapper':
        """Register a function and return a wrapper instance."""
        name = name or func.__name__
        instance = cls(name, func)
        cls[name] = instance
        return instance

    def __init__(self, name: str, func: Callable):
        """Initialize with function name and callable."""
        self.name = name
        self._func = func

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        """Execute the wrapped function."""
        return self._func(*args, **kwargs)

    def __repr__(self) -> str:
        """String representation of the wrapper."""
        return f"{self.__class__.__name__}['{self.name}']"
