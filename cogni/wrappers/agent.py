from typing import Any, Dict, List, Optional
from .instances_store import InstancesStore
from .middleware import MW

class Agent(metaclass=InstancesStore):
    """Base class for agents that provides middleware chaining and execution."""

    def __init__(self, name: str, middlewares: str):
        """Initialize an agent with a name and middleware chain.
        
        Args:
            name: The agent's unique identifier
            middlewares: Pipe-separated list of middleware names
        """
        self.name = name
        self._middlewares_str = middlewares
        self._middlewares: Optional[List[MW]] = None
        Agent[name] = self

    def _init_middlewares(self):
        """Initialize middleware chain from string specification."""
        if self._middlewares is None:
            self._middlewares = [
                MW[name.strip()]
                for name in self._middlewares_str.split('|')
            ]

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        """Execute the middleware chain with the given inputs.
        
        The first middleware receives a context dict containing:
        - agent: Reference to this agent
        - args: The input arguments
        - hops: Number of inference steps (initially 0)
        - kwargs: Any keyword arguments
        
        Each middleware receives:
        - ctx: The context dict
        - conv: The current conversation/value
        """
        self._init_middlewares()
        
        ctx = {
            'agent': self,
            'args': args,
            'hops': 0,
            'kwargs': kwargs
        }

        conv = args
        for mw in self._middlewares:
            if isinstance(conv, tuple):
                conv = mw(ctx, *conv)
            else:
                conv = mw(ctx, conv)
                
        return conv

    def __repr__(self) -> str:
        """String representation showing agent name."""
        return f"Agent['{self.name}']"
