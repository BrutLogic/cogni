from .func_wrapper import FuncWrapper
from .instances_store import DefaultInstanceStore

class Log(FuncWrapper, metaclass=DefaultInstanceStore):
    ...
    
log = Log.register

@log
def _default(*a, **kw):...
