from .func_wrapper import FuncWrapper
from .instances_store import InstancesStore

class MW(FuncWrapper, metaclass=InstancesStore):
    ...

mw = MW.register