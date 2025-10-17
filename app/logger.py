# In app/logger.py

import logging
from abc import ABC, abstractmethod

# ADD THESE TWO CLASSES HERE
class Observer(ABC):
    """The Observer interface declares the update method, used by subjects."""
    @abstractmethod
    def update(self, subject) -> None:
        pass

class Subject(ABC):
    """The Subject interface declares a set of methods for managing subscribers."""
    @abstractmethod
    def attach(self, observer: Observer) -> None:
        pass

    @abstractmethod
    def detach(self, observer: Observer) -> None:
        pass

    @abstractmethod
    def notify(self) -> None:
        pass

# --- Your existing logger setup code ---
# ... (logging.basicConfig, etc.) ...
app_logger = logging.getLogger(__name__)

# --- Your existing LoggingObserver class ---
# It should now correctly inherit from the Observer class defined above
class LoggingObserver(Observer):
    def update(self, subject) -> None:
        # Your update logic here...
        op_name = subject.operation.__class__.__name__
        app_logger.info(f"New calculation: Operation={op_name}, Operands=({subject.a}, {subject.b})")