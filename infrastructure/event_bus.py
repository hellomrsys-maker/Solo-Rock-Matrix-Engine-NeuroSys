import threading
from collections import defaultdict
import time

class EventBus:
    def __init__(self):
        self._lock = threading.Lock()
        self._subscribers = defaultdict(list)

    def subscribe(self, event_type: str, callback):
        with self._lock:
            if callback not in self._subscribers[event_type]:
                self._subscribers[event_type].append(callback)

    def unsubscribe(self, event_type: str, callback):
        with self._lock:
            if callback in self._subscribers[event_type]:
                self._subscribers[event_type].remove(callback)

    def publish(self, event_type: str) -> None:
        # Zero-Bridge: The EventBus no longer carries data. It is purely a wake-up signal.
        # Shallow copy the callback list to allow callbacks to mutate subscribers without deadlock
        with self._lock:
            callbacks = list(self._subscribers[event_type])
            
        for callback in callbacks:
            try:
                callback() # Wake up the nerve, no payload passed
            except Exception as e:
                print(f"[EventBus] Error dispatching event {event_type} to callback {callback}: {e}")

# Global event bus instance for the entire V4 matrix
event_bus = EventBus()
