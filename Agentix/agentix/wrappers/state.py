import os
import json
from typing import Any, Dict, List, Union


class StateDict:
    """A wrapper for dictionaries that provides attribute-style access and automatic persistence"""

    def __init__(self, data: Dict, parent: '_State' = None, state_name: str = None, path: List[str] = None):
        self._data = {}
        self._parent = parent
        self._state_name = state_name
        self._path = path or []

        # Recursively wrap nested structures
        for k, v in data.items():
            if isinstance(v, dict):
                self._data[k] = StateDict(
                    v, parent, state_name, self._path + [k])
            elif isinstance(v, list):
                self._data[k] = StateList(
                    v, parent, state_name, self._path + [k])
            else:
                self._data[k] = v

    def __len__(self):
        return len(self._data)

    def _persist(self):
        """Trigger persistence up the chain"""
        if self._parent and self._state_name:
            self._parent._save_state(
                self._state_name, self._parent._cache[self._state_name])

    def __getattr__(self, name: str) -> Any:
        if name in self._data:
            return self._data[name]
        raise AttributeError(f"'StateDict' object has no attribute '{name}'")

    def __setattr__(self, name: str, value: Any) -> None:
        if name.startswith('_'):
            super().__setattr__(name, value)
            return

        if isinstance(value, dict):
            self._data[name] = StateDict(
                value, self._parent, self._state_name, self._path + [name])
        elif isinstance(value, list):
            self._data[name] = StateList(
                value, self._parent, self._state_name, self._path + [name])
        else:
            self._data[name] = value
        self._persist()

    def __getitem__(self, key: str) -> Any:
        if key not in self._data:
            self._data[key] = StateDict(
                {}, self._parent, self._state_name, self._path + [key])
            self._persist()
        return self._data[key]

    def __setitem__(self, key: str, value: Any) -> None:
        if isinstance(value, dict):
            self._data[key] = StateDict(
                value, self._parent, self._state_name, self._path + [key])
        elif isinstance(value, list):
            self._data[key] = StateList(
                value, self._parent, self._state_name, self._path + [key])
        else:
            self._data[key] = value
        self._persist()

    def __contains__(self, key: str) -> bool:
        return key in self._data

    def __delitem__(self, key: str) -> None:
        """Delete an item from the state dictionary"""
        if key in self._data:
            del self._data[key]
            self._persist()
        else:
            raise KeyError(key)

    def get(self, item, default=None):
        if item in self._data:
            return self._data[item]
        return default

    def to_dict(self) -> Dict:
        """Convert back to a regular dictionary"""
        result = {}
        for k, v in self._data.items():
            if isinstance(v, (StateDict, StateList)):
                result[k] = v.to_dict()
            else:
                result[k] = v
        return result

    def __str__(self) -> str:
        """String representation showing the wrapped dictionary"""
        return str(self.to_dict())

    def __repr__(self) -> str:
        """Detailed representation including class name"""
        return f"StateDict({self.to_dict()})"

    def items(self):
        """Return a view of the dictionary's items (key-value pairs)"""
        return self._data.items()

    def keys(self):
        """Return a view of the dictionary's keys"""
        return self._data.keys()


class StateList:
    """A wrapper for lists that provides automatic persistence"""

    def __init__(self, data: List, parent: '_State' = None, state_name: str = None, path: List[str] = None):
        self._data = []
        self._parent = parent
        self._state_name = state_name
        self._path = path or []

        # Recursively wrap nested structures
        for item in data:
            if isinstance(item, dict):
                self._data.append(
                    StateDict(item, parent, state_name, self._path + ['*']))
            elif isinstance(item, list):
                self._data.append(
                    StateList(item, parent, state_name, self._path + ['*']))
            else:
                self._data.append(item)

    def _persist(self):
        """Trigger persistence up the chain"""
        if self._parent and self._state_name:
            self._parent._save_state(
                self._state_name, self._parent._cache[self._state_name])

    def __getitem__(self, idx: int) -> Any:
        return self._data[idx]

    def __setitem__(self, idx: int, value: Any) -> None:
        if isinstance(value, dict):
            self._data[idx] = StateDict(
                value, self._parent, self._state_name, self._path + ['*'])
        elif isinstance(value, list):
            self._data[idx] = StateList(
                value, self._parent, self._state_name, self._path + ['*'])
        else:
            self._data[idx] = value
        self._persist()

    def __contains__(self, value: Any) -> bool:
        return value in self._data

    def __len__(self) -> int:
        return len(self._data)

    def append(self, value: Any) -> None:
        if isinstance(value, dict):
            self._data.append(StateDict(value, self._parent,
                              self._state_name, self._path + ['*']))
        elif isinstance(value, list):
            self._data.append(StateList(value, self._parent,
                              self._state_name, self._path + ['*']))
        else:
            self._data.append(value)
        self._persist()

    def to_dict(self) -> List:
        """Convert back to a regular list"""
        result = []
        for item in self._data:
            if isinstance(item, (StateDict, StateList)):
                result.append(item.to_dict())
            else:
                result.append(item)
        return result

    def __str__(self) -> str:
        """String representation showing the wrapped list"""
        return str(self.to_dict())

    def __repr__(self) -> str:
        """Detailed representation including class name"""
        return f"StateList({self.to_dict()})"


class _State:
    def __init__(self):
        self._states_dir = '/home/val/GoodAI/goodassistant/.states'
        self._cache = {}
        self._callbacks = []
        # Create states directory if it doesn't exist
        os.makedirs(self._states_dir, exist_ok=True)

    def reset_cache(self):
        self._cache = {}

    def onChange(self, callback):
        """Register a callback to be called when any state changes

        Args:
            callback: Function that takes (state_id:str, state:Any)
        """
        self._callbacks = [callback]

    def _get_state_path(self, state_name: str) -> str:
        """Get the full path for a state file"""
        return os.path.join(self._states_dir, f"{state_name}.json")

    def _load_state(self, state_name: str) -> Dict:
        """Load state from file or return empty dict if not exists"""
        path = self._get_state_path(state_name)
        if os.path.exists(path):
            # print(f"{path=}")
            # input('')
            with open(path, 'r') as f:
                try:
                    return json.load(f)
                except:
                    return {}
        return {}

    def _save_state(self, state_name: str, data: Union[StateDict, Dict]) -> None:
        """Save state to file"""
        if isinstance(data, StateDict):
            data = data.to_dict()
        path = self._get_state_path(state_name)
        with open(path, 'w') as f:
            json.dump(data, f, indent=2)

        # Trigger callbacks
        for callback in self._callbacks:
            callback(state_name, data)

    def __getitem__(self, state_name: str) -> StateDict:
        """Get a state, loading from file if not in cache"""
        if state_name not in self._cache:
            data = self._load_state(state_name)
            self._cache[state_name] = StateDict(data, self, state_name)
        return self._cache[state_name]

    def __contains__(self, key):
        return self[key] != {}

    def __setitem__(self, state_name: str, value: Dict) -> None:
        """Set a state and persist it"""
        self._cache[state_name] = StateDict(value, self, state_name)
        self._save_state(state_name, value)

    def __delitem__(self, state_name: str) -> None:
        """Delete a state and its file"""
        path = self._get_state_path(state_name)
        if os.path.exists(path):
            os.remove(path)
        self._cache.pop(state_name, None)


State = _State()
