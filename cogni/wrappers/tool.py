from functools import wraps
from .instances_store import InstancesStore
from .func_wrapper import FuncWrapper

class Tool(FuncWrapper, metaclass=InstancesStore):
    """A wrapper class for tool functions that provides registration and access via a global container."""
    ...

tool = Tool.register
