import dataclasses
import json
import os
import time
from typing import List, Optional
from toolz import reduce

@dataclasses.dataclass
class Event:
    """Represents an execution event, either entering or exiting a named state."""
    event_type: str  # 'enter' or 'exit'
    target: str

class Exec:
    """Handles execution states using event sourcing, with events persisted as files."""
    

    _instance = None
    @classmethod
    def get_instance(cls):
        cls._instance = cls._instance or cls()
        
        return cls._instance
    
    
    def __init__(self, events_dir: str = 'events') -> None:
        """Initializes the executor with a directory to store events."""
        self.events_dir = events_dir
        os.makedirs(self.events_dir, exist_ok=True)

    def _write_event(self, event: Event) -> None:
        """Writes a single event to a uniquely named file."""
        timestamp = str(int(time.time() * 1000000))  # Microsecond precision for filenames
        filename = os.path.join(self.events_dir, f"{timestamp}.json")
        with open(filename, 'w') as f:
            f.write(json.dumps(dataclasses.asdict(event)))

    def enter(self, target: str) -> None:
        """Records an 'enter' event for a given target."""
        self._write_event(Event('enter', target))

    def exit(self) -> None:
        """Records an 'exit' event for the most recent 'enter' target, if any."""
        current_cursor = self.current_cursor
        if current_cursor:
            self._write_event(Event('exit', current_cursor))

    def _load_events(self) -> List[Event]:
        """Loads all events from the file system, sorted by their filenames (timestamps)."""
        files = sorted(os.listdir(self.events_dir))
        return [Event(**json.loads(open(os.path.join(self.events_dir, file), 'r').read())) for file in files]

    @property
    def current_cursor(self) -> Optional[str]:
        """Returns the current cursor, i.e., the target of the most recent 'enter' event not yet exited."""
        return self.execution_path[-1] if self.execution_path else None

    @property
    def execution_path(self) -> List[str]:
        """Returns the list of active 'enter' targets leading to the current cursor."""
        events = self._load_events()
        active_nodes = reduce(lambda acc, e: acc + [e.target] if e.event_type == 'enter' else acc[:-1], events, [])
        return active_nodes

    def generate_mermaid_flowchart(self) -> str:
        """Generates a Mermaid flowchart representation of the execution flow."""
        mermaid = "graph TD\n"
        stack = []
        for event in self._load_events():
            if event.event_type == 'enter':
                if stack:
                    mermaid += f"{stack[-1]} --> {event.target}\n"
                stack.append(event.target)
            elif stack:
                stack.pop()
        return mermaid
