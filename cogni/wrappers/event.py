from collections import defaultdict
import threading


class Event:
    _handlers = {}
    instance = None

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
            assert event_type not in cls._handlers, f"already a handler for {
                event_type}"

            cls._handlers[event_type] = func

            return func
        return decorator
    on = register

    @classmethod
    def init(cls):
        if cls.instance is None:
            cls.instance = cls()
        return cls.instance

    @classmethod
    def emit(cls, event_type, payload):
        if cls.instance is None:
            cls.instance = cls()
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
