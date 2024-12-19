from typing import Any, Callable, Dict
from .instances_store import InstancesStore

class MW(metaclass=InstancesStore):
    """Base wrapper class for middleware that provides registration and access."""
    
    @classmethod
    def register(cls, func: Callable = None, name: str = None) -> 'MW':
        """Register a middleware function and return a wrapper instance."""
        if func is None:
            return lambda f: cls.register(f, name)
            
        name = name or func.__name__
        instance = cls(name, func)
        cls[name] = instance
        return instance

    def __init__(self, name: str, func: Callable):
        """Initialize with middleware name and callable."""
        self.name = name
        self._func = func

    def __call__(self, ctx: Dict[str, Any], conv: Any, *args: Any, **kwargs: Any) -> Any:
        """Execute the wrapped middleware function."""
        return self._func(ctx, conv, *args, **kwargs)

    def __repr__(self) -> str:
        """String representation of the wrapper."""
        return f"{self.__class__.__name__}['{self.name}']"

# Decorator for registering middleware
mw = MW.register
