# app/calculator_memento.py

from decimal import Decimal
from app.calculation import ArithmeticCalculation
from app.logger import app_logger

class CalculatorMemento:
    """
    Implements the Memento Design Pattern. 
    It stores the state of the Calculator (Originator) at a point in time.
    """
    # The type hint for last_command has been corrected to ArithmeticCalculation
    def __init__(self, state_value: Decimal, last_command: ArithmeticCalculation):
        self._state_value = state_value
        self._last_command = last_command
        app_logger.debug(f"Created Memento with value: {self._state_value}")

    def get_state_value(self) -> Decimal:
        """Returns the stored numerical state."""
        return self._state_value

    # The return type hint has also been corrected to ArithmeticCalculation
    def get_last_command(self) -> ArithmeticCalculation:
        """Returns the last command executed when this state was saved."""
        return self._last_command