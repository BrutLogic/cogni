class FuncWrapper:
    @classmethod
    def register(cls, func:callable, name=None):
        name = name or func.__name__
        instance = cls(name, func)
        cls[name] = instance
        return instance 

    def __init__(self, name:str, func:callable):
        self.name  = name 
        self._func = func 
    def __repr__(self):
        return f"{type(self).__name__}['{self.name}']"
    def __call__(self, *args, **kwargs):
        return self._func(*args, **kwargs)
    def __getattr__(self, key):
        return getattr(self._func, key)
    
# FIXME: should be on its own file
import os
def file_property(filename):
    def getter(self):
        file_path = os.path.join(self.dir_path, filename)
        try:
            with open(file_path, 'r') as file:
                return file.read()
        except FileNotFoundError:
            return None

    def setter(self, value):
        file_path = os.path.join(self.dir_path, filename)
        with open(file_path, 'w') as file:
            file.write(value)
            
        if hasattr(self,'export'):
            self.export()

    return property(getter, setter)


