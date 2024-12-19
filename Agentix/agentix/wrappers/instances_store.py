class InstancesStore(type):
    """
    A metaclass for storing and retrieving Agent/MW instances.
    """
    def __new__(metacls, name, bases, dct):
        # Create a new class with a unique instance store
        cls = super().__new__(metacls, name, bases, dct)
        cls._store = {}  # Instance store specific to each class
        return cls

    def __getitem__(cls, item: str):
        if '/' in item:
            item = item.split('/')[-1]
        try:
            return cls._store[item]
        except KeyError:
            if 'Null' in cls._store:
                nullInstance = cls._store['Null']
                nullInstance.setinfo(item)
                return nullInstance
            raise KeyError(f"No {cls.__name__} with name '{item}' found.")

    def __setitem__(cls, key: str, value) -> None:
        # if key in cls._store:
        #    raise KeyError(f"{cls.__name__} with name '{key}' already exists.")
        cls._store[key] = value

    def __contains__(cls, item: str) -> bool:
        return item in cls._store

    def keys(cls):
        return cls._store.keys()

    def values(cls):
        return cls._store.values()

    def items(cls):
        return cls._store.items()

    def get(cls, item: str, default=None):
        return cls._store.get(item, default)


class DefaultInstanceStore(InstancesStore):
    def __getitem__(cls, item: str):

        val = super().get(item) or super().get('_default')
        if val is None:
            raise KeyError(
                f"No {cls.__name__} with name '{item}' found and no default instance available.")
        try:
            val._set_item(item)
        except:
            ...
        return val
