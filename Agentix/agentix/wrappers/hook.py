from .func_wrapper import FuncWrapper
from .instances_store import InstancesStore

class Tool(FuncWrapper, metaclass=InstancesStore):
    ...
    
tool = Tool.register
