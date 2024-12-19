import os
import json
import time
from datetime import datetime
from typing import Any, Dict, List, Union
from pathlib import Path

class _EventStore:
    def __init__(self):
        self._stores_dir = './.stores'
        os.makedirs(self._stores_dir, exist_ok=True)
        
    def _get_store_path(self, store_name: str) -> str:
        """Get the full path for a store directory"""
        return os.path.join(self._stores_dir, store_name)
        
    def _get_next_event_path(self, store_name: str) -> str:
        """Get the path for the next event file"""
        store_path = self._get_store_path(store_name)
        os.makedirs(store_path, exist_ok=True)
        
        existing_files = [f for f in os.listdir(store_path) if f.endswith('.json')]
        next_num = len(existing_files)
        return os.path.join(store_path, f"{next_num}.json")
    
    def _save_event(self, store_name: str, event: Dict) -> None:
        """Save an event with timestamp"""
        event['timestamp'] = int(time.time() * 1000)  # Millisecond timestamp
        path = self._get_next_event_path(store_name)
        
        with open(path, 'w') as f:
            json.dump(event, f, indent=2)
            
    def _load_events(self, store_name: str) -> List[Dict]:
        """Load all events from a store"""
        store_path = self._get_store_path(store_name)
        if not os.path.exists(store_path):
            return []
            
        events = []
        for file_name in sorted(os.listdir(store_path)):
            if file_name.endswith('.json'):
                with open(os.path.join(store_path, file_name), 'r') as f:
                    events.append(json.load(f))
        return events
    
    class _StoreProxy:
        def __init__(self, store_name: str, parent: '_EventStore'):
            self.store_name = store_name
            self.parent = parent
            
        def __iadd__(self, event: Dict) -> '_EventStore._StoreProxy':
            """Handle += operator for adding events"""
            self.parent._save_event(self.store_name, event)
            return self
            
        def all(self) -> List[Dict]:
            """Get all events in the store"""
            return self.parent._load_events(self.store_name)
            
        def after(self, threshold: Union[datetime, int]) -> List[Dict]:
            """Get events after a specific timestamp or datetime"""
            if isinstance(threshold, datetime):
                threshold_ts = int(threshold.timestamp() * 1000)
            else:
                threshold_ts = int(threshold)
                
            return [
                event for event in self.all()
                if event['timestamp'] > threshold_ts
            ]
            
    def __getitem__(self, store_name: str) -> _StoreProxy:
        """Get a store proxy for the given name"""
        return self._StoreProxy(store_name, self)

Store = _EventStore()
