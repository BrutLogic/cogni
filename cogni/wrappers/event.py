"""
Event system for handling asynchronous events and socket communications.

This module provides a standardized way to handle events across the application,
with support for WebSocket communication and thread-safe event handling.

Example usage:

    # Register an event handler
    @Event.on("user_connected")
    def handle_user_connection(event_data: EventPayload):
        print(f"User {event_data.user_id} connected")
        
    # Emit an event
    Event.emit("user_connected", {"user_id": "123"})
    
    # Initialize the event system
    event_system = Event.init()
"""

from collections import defaultdict
import threading
from typing import Any, Dict, Optional, Callable
from pydantic import BaseModel, Field


class EventPayload(BaseModel):
    """Standard structure for event payloads."""
    event_type: str = Field(..., description="Type of the event")
    data: Dict[str, Any] = Field(default_factory=dict, description="Event data")
    _type: str = Field(default="event", description="Internal event type marker")
    _ttl: int = Field(default=5, description="Time-to-live counter for event propagation")


class Event:
    """
    Event management system with thread-safe handlers and WebSocket support.
    
    Attributes:
        _handlers: Dictionary mapping event types to their handler functions
        instance: Singleton instance of the Event system
        socketio: Optional SocketIO instance for WebSocket communication
    """
    _handlers: Dict[str, Callable] = {}
    instance: Optional['Event'] = None
    socketio: Any = None

    @classmethod
    def handle(cls, event_data: Dict[str, Any]) -> None:
        """
        Handle an incoming event by dispatching it to the appropriate handler.
        
        Args:
            event_data: Dictionary containing event information
        """
        event_type = event_data.get('eventType')
        handler = cls._handlers.get(event_type)
        
        if not handler:
            return
            
        def run_handler(handler: Callable, data: Dict[str, Any]) -> None:
            handler(EventPayload(**data))
            
        thread = threading.Thread(
            target=run_handler, 
            args=(handler, event_data)
        )
        thread.start()

    @classmethod
    def register(cls, event_type: str) -> Callable:
        """
        Decorator to register an event handler.
        
        Args:
            event_type: The type of event this handler will process
            
        Returns:
            Decorator function for registering handlers
            
        Raises:
            AssertionError: If handlers are registered after initialization
        """
        assert cls.instance is None, "Register handlers before initialization"

        def decorator(func: Callable) -> Callable:
            assert not hasattr(func, '_sockethandler'), "Handler already registered"
            assert event_type not in cls._handlers, f"Handler exists for {event_type}"
            
            setattr(func, '_sockethandler', True)
            cls._handlers[event_type] = func
            return func
            
        return decorator
        
    # Alias for register to provide a more intuitive API
    on = register

    @classmethod
    def init(cls) -> 'Event':
        """
        Initialize the Event system singleton.
        
        Returns:
            The Event system instance
        """
        if cls.instance is None:
            cls.instance = cls()
        return cls.instance

    @classmethod
    def emit(cls, event_type: str, payload: Dict[str, Any]) -> None:
        """
        Emit an event to all registered handlers.
        
        Args:
            event_type: Type of event to emit
            payload: Event data to send
        """
        if cls.instance is None:
            cls.instance = cls()
            
        event_data = EventPayload(
            event_type=event_type,
            data=payload,
            _ttl=payload.get('_ttl', 5)
        )
        
        if event_data._ttl > 0:
            event_data._ttl -= 1
            cls.instance.handle(event_data.dict())
            
        if cls.instance.socketio:
            cls.instance.socketio.emit('event', event_data.dict())
