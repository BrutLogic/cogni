import glob
import os
from typing import Any, Dict, List, Optional
from .instances_store import InstancesStore
from .middleware import MW
from ..entities import Message, Conversation
from .tool import Tool


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

    @property
    def histo(self):
        try:
            return Conversation.from_file(self._histo_path)
        except:  # FIXME: have typed exception & exception handling, this can hide nasty bugs
            return Conversation([])

    def append_histo(self, msg):
        try:
            last = self.histo[-1]
            if last.content == msg.content and last.role == msg.role:
                return
        except:  # FIXME
            pass
        (self.histo + msg).to_file(self._histo_path)

    @property
    def base_prompt(self):
        grandparent_path = os.getcwd()
        pattern = grandparent_path + f"/**/prompts/{self.name}.conv"

        for file_path in glob.glob(pattern, recursive=True):
            self._histo_path = file_path.replace(
                '/prompts/', '/prompts/.histo/')
            histo_dir = os.path.dirname(self._histo_path)
            if not os.path.exists(histo_dir):
                os.makedirs(histo_dir, exist_ok=True)
            return Conversation.from_file(file_path)

        raise FileNotFoundError(f"Did not find {self.name}.conv")

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

        def infer(conv):
            ...

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
            while isinstance(conv, Conversation) and conv.should_infer:
                llm = conv.llm
                if llm == 'fake':
                    conv = conv.rehop(
                        "Fake llm message",
                        'assistant'
                    )
                else:
                    conv = conv.rehop(
                        Tool['llm'](conv),
                        'assistant'
                    )
                conv.should_infer = False
                self.append_histo(conv[-1])
                conv.hops += 1
                ctx['hops'] += 1
                conv = mw(ctx, conv)

        return conv

    def __repr__(self) -> str:
        """String representation showing agent name."""
        return f"Agent['{self.name}']"
