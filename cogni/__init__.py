"""Cogni framework initialization."""
from functools import wraps
import os
from .entities import Message, Conversation
from .wrappers import tool, Tool, MW, mw, Agent, init_state
from .magicimport import dynamic_import

State = init_state(os.getcwd())


def use_tools(func):
    @wraps(func)
    def _use_tools(*a, **kw): raise Exception('TODO')

    return _use_tools


def parse_tools(*a, **kw): raise Exception('TODO')


for dir_name in [
    'tools',
    'agents',
    'middlewares',
]:
    dynamic_import(dir_name)

__all__ = [
    'Message',
    'Conversation',
    'tool',
    'Tool',
    'mw',
    'MW',
    'Agent',
    'State',
    'use_tools',
    'parse_tools',
]
