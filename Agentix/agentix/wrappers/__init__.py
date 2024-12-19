from .middleware import MW, mw
from .tool import Tool, tool, use_tools
from .agent import Agent
from .Func import Func, func
from .log import Log, log
from .event import Event
from .endpoint import Endpoint, get, post, endpoint
from .page import Page, page
from .component import Component, component
from .conf import Conf
from .state import State
from .event_store import Store
from .socket import SocketManager


class _Services:
    _instance = None
    _services = {}

    @classmethod
    def singleton(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def register(self, name, instance):
        self._services[name] = instance

    def __getitem__(self, item):
        return self._services.get(item)


Services = _Services.singleton()
