import os
from enum import Enum

from .func_wrapper import FuncWrapper, file_property
from .instances_store import InstancesStore


class Func(FuncWrapper, metaclass=InstancesStore):
    
    code = file_property('code.py')
    
    def __init__(self, name: str, func: callable):
        super().__init__(name, func)
        cwd = os.getcwd()
        self.dir_path = os.path.join(cwd, "funcs", name)
        os.makedirs(self.dir_path, exist_ok=True)

 

func = Func.register