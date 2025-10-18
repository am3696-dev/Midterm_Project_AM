# app/logger.py

import logging
import os
from logging.handlers import RotatingFileHandler
from abc import ABC, abstractmethod
from app.calculator_config import CalculatorConfig

# --- Observer Pattern Base Classes ---
class Observer(ABC):
    @abstractmethod
    def update(self, subject) -> None:
        pass # pragma: no cover

class Subject(ABC):
    @abstractmethod
    def attach(self, observer: Observer) -> None:
        pass # pragma: no cover
    @abstractmethod
    def detach(self, observer: Observer) -> None:
        pass # pragma: no cover
    @abstractmethod
    def notify(self) -> None:
        pass # pragma: no cover

# --- Logger Setup Function ---
def setup_logging():
    """Initializes and configures the application logger."""
    log_dir = CalculatorConfig.LOG_DIR
    if not os.path.exists(log_dir):
        os.makedirs(log_dir) # pragma: no cover

    log_file_path = os.path.join(log_dir, 'app.log')

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            RotatingFileHandler(log_file_path, maxBytes=1048576, backupCount=5),
            logging.StreamHandler()
        ]
    )

app_logger = logging.getLogger(__name__)

# --- Observer Implementation for Logging ---
class LoggingObserver(Observer):
    def update(self, subject) -> None:
        """Logs the details of a new calculation."""
        result = getattr(subject, 'result', 'N/A')
        op_name = subject.operation.__name__.title()
        app_logger.info(f"New calculation: Operation={op_name}, Operands=({subject.a}, {subject.b}), Result={result}")