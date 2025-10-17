# app/calculation.py

from decimal import Decimal, InvalidOperation
from typing import Callable

# Import Subject and Observer from logger.py to break the circular dependency
from app.logger import Subject, Observer, app_logger

class ArithmeticCalculation(Subject):
    """
    A class to represent a single arithmetic calculation.
    It acts as a "Subject" in the Observer design pattern.
    """
    def __init__(self, a: Decimal, b: Decimal, operation: Callable[[Decimal, Decimal], Decimal]):
        """Initializes the calculation with two operands and an operation."""
        self._observers = []
        self.a = a
        self.b = b
        self.operation = operation
        self.result = None  # Store the result after performing the calculation

    # --- Observer Pattern Methods ---
    def attach(self, observer: Observer) -> None:
        """Attach an observer to the subject."""
        if observer not in self._observers:
            self._observers.append(observer)
            app_logger.info(f"Attached observer: {observer.__class__.__name__}")

    def detach(self, observer: Observer) -> None:
        """Detach an observer from the subject."""
        try:
            self._observers.remove(observer)
            app_logger.info(f"Detached observer: {observer.__class__.__name__}")
        except ValueError:
            app_logger.warning(f"Observer {observer.__class__.__name__} not found for detachment.")

    def notify(self) -> None:
        """Notify all observers about an event."""
        app_logger.info("Notifying observers...")
        for observer in self._observers:
            observer.update(self)

    # --- Calculation Logic ---
    @staticmethod
    def create(a: Decimal, b: Decimal, operation: Callable[[Decimal, Decimal], Decimal]):
        """Factory method to create a new calculation instance."""
        return ArithmeticCalculation(a, b, operation)

    def perform(self) -> Decimal:
        """
        Performs the calculation and notifies observers.
        Handles potential calculation errors.
        """
        try:
            self.result = self.operation(self.a, self.b)
            app_logger.info(f"Calculation successful: {self.a} {self.operation.__name__} {self.b} = {self.result}")
            self.notify()  # Notify observers after a successful calculation
            return self.result
        except (ValueError, InvalidOperation, ZeroDivisionError) as e:
            app_logger.error(f"Error performing calculation ({self.a}, {self.b}, {self.operation.__name__}): {e}")
            # Re-raise the exception to be handled by the caller (e.g., the REPL)
            raise

    def __repr__(self):
        """Return a string representation of the calculation."""
        op_name = self.operation.__name__.replace('_', ' ').title()
        return f"Calculation({self.a}, {self.b}, Operation={op_name})"