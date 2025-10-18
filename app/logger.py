# app/logger.py

import logging
import os
from logging.handlers import RotatingFileHandler
from abc import ABC, abstractmethod
from app.calculator_config import CalculatorConfig # Import the config

# --- Observer Pattern Base Classes ---
class Observer(ABC):
    @abstractmethod
    def update(self, subject) -> None:
        pass

class Subject(ABC):
    @abstractmethod
    def attach(self, observer: Observer) -> None:
        pass
    @abstractmethod
    def detach(self, observer: Observer) -> None:
        pass
    @abstractmethod
    def notify(self) -> None:
        pass

# --- Logger Setup Function ---
def setup_logging():
    """Initializes and configures the application logger."""
    log_dir = CalculatorConfig.LOG_DIR
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # Use the config to create the full log file path
    log_file_path = os.path.join(log_dir, 'app.log')

    # Configure root logger
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            RotatingFileHandler(log_file_path, maxBytes=1048576, backupCount=5), # File handler
            logging.StreamHandler() # Console handler
        ]
    )

app_logger = logging.getLogger(__name__)

# --- Observer Implementation for Logging ---
class LoggingObserver(Observer):
    def update(self, subject) -> None:
        """Logs the details of a new calculation."""
        # Check if subject.result exists to avoid error on first log
        result = getattr(subject, 'result', 'N/A')
        op_name = subject.operation.__name__.title()
        app_logger.info(f"New calculation: Operation={op_name}, Operands=({subject.a}, {subject.b}), Result={result}")