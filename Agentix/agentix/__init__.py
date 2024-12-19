import os
from .magicimport import dynamic_import

from .wrappers import (Tool,
                       Agent,
                       tool,
                       use_tools,
                       mw,
                       MW,
                       Func,
                       func,
                       Log,
                       log,
                       Event,
                       Endpoint,
                       endpoint,
                       Page,
                       page,
                       Component,
                       component,
                       get,
                       post,
                       Conf,
                       Services,
                       State,
                       Store,
                       SocketManager,
                       )


from .entities import Message, Conversation, ModuleInfo
from .utils import logger
from .utils.exec import Exec


class _Stuff:
    _instance = None


if not _Stuff._instance:
    _Stuff._instance = _Stuff()
Stuff = _Stuff._instance

# cwd = os.getcwd()
# os.chdir('/home/val/algotrade')


dynamic_import('middlewares')
dynamic_import('tools')
dynamic_import('loggers')
dynamic_import('funcs')
dynamic_import('agents')
dynamic_import('endpoints')
dynamic_import('utils')
# dynamic_import('nodes')
dynamic_import('code')

# os.chdir(cwd)

__all__ = [
    'Store'
]
