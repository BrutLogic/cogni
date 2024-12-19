from collections import defaultdict
import threading


def printou(w):
    return
    from rich import print
    print('[red]__EVENT__')
    print(f"{w=}")


class SocketManager:
    _handlers = {}
    instance = None

    def __init__(self, socketio):
        self.socketio = socketio
        # socketio.on('event', printou)
        if socketio is None:
            return
        for event_type, handler in self._handlers.items():
            socketio.on(event_type)(handler)

    @classmethod
    def handle(cls, json_data):
        def run_handler(hndlr, jd):
            hndlr(jd)
        event_type = json_data.get('eventType')

        handler = cls._handlers.get(event_type, False)
        if not handler:
            # print(f"No handler for {event_type}")
            return
        t = threading.Thread(target=run_handler, args=(handler, json_data))
        t.start()

    @classmethod
    def register(cls, event_type) -> callable:

        assert cls.instance is None, "You should register all handlers before init"

        def decorator(func):
            assert not hasattr(func, '_sockethandler')
            setattr(func, '_sockethandler', True)
            assert event_type not in cls._handlers, f"already a handler for {event_type}"

            cls._handlers[event_type] = func

            return func
        return decorator
    on = register

    @classmethod
    def init(cls, socketio):
        if cls.instance is None:
            cls.instance = cls(socketio)
        return cls.instance

    @classmethod
    def emit(cls, event_type, payload, broadcast=False):
        if cls.instance is None:
            cls.instance = cls(None)
        payload['eventType'] = event_type
        payload['_type'] = 'event'
        if not '_ttl' in payload:
            payload['_ttl'] = 5
        else:
            payload['_ttl'] -= 1

        if payload['_ttl'] > 0:
            cls.instance.handle(payload)
        if cls.instance.socketio:
            # , broadcast=broadcast)
            cls.instance.socketio.emit('event', payload)
