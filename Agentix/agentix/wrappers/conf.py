class _Conf:
    def __init__(self):
        self._data = {}

    def __getattr__(self, name):
        if name not in self._data:
            self._data[name] = _Conf()
        return self._data[name]

    def __setattr__(self, name, value):
        if name == '_data':
            super().__setattr__(name, value)
        else:
            if isinstance(value, dict):
                conf = _Conf()
                for k, v in value.items():
                    setattr(conf, k, v)
                self._data[name] = conf
            else:
                self._data[name] = value

    def __getitem__(self, key):
        # Handle nested access with dot notation
        if '.' in key:
            parts = key.split('.')
            obj = self
            for part in parts:
                obj = getattr(obj, part)
            return obj
        return self._data[key]

    def __setitem__(self, key, value):
        self._data[key] = value

    def __str__(self):
        return str(self._data)

    def __repr__(self):
        return repr(self._data)
    
    
Conf = _Conf()

__all__ = ['Conf']