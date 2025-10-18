# app/calculator.py

from decimal import Decimal
from app.calculation import ArithmeticCalculation
from app.calculator_memento import CalculatorMemento
from app.history import HistoryManager
from app.exceptions import InsufficientHistoryError
from app.logger import app_logger

class Calculator:
    """
    The Originator. It holds the current state and can create or restore mementos.
    """
    def __init__(self):
        self._current_value = Decimal('0')
        self._history_manager = HistoryManager()
        initial_command = ArithmeticCalculation(Decimal('0'), Decimal('0'), lambda a, b: a)
        self._save_state(initial_command)
        app_logger.info("Calculator initialized and initial state saved.")

    def _save_state(self, command: ArithmeticCalculation):
        """Creates a memento of the current state and saves it."""
        memento = CalculatorMemento(self._current_value, command)
        self._history_manager.save_state(memento)

    def execute_command(self, command: ArithmeticCalculation) -> Decimal:
        """Executes a command, updates the value, and saves the new state."""
        result = command.perform() 
        self._current_value = result
        self._save_state(command)
        app_logger.info(f"Command executed. New value: {self._current_value}")
        return self._current_value

    def undo(self):
        """Restores the previous state from the history manager."""
        memento = self._history_manager.undo()
        if memento is None:
            raise InsufficientHistoryError("Cannot undo: No more history available.")
        self._current_value = memento.get_state_value()
        app_logger.info(f"Undo successful. Restored value: {self._current_value}")

    def redo(self):
        """Restores a previously undone state."""
        memento = self._history_manager.redo()
        if memento is None:
            raise InsufficientHistoryError("Cannot redo: No more states to restore.")
        self._current_value = memento.get_state_value()
        app_logger.info(f"Redo successful. Restored value: {self._current_value}")

    def get_current_value(self) -> Decimal:
        """Returns the current value of the calculator."""
        return self._current_value
    
    def get_history(self) -> list[CalculatorMemento]:
        """Retrieves the calculation history from the history manager."""
        return self._history_manager.get_history()

    def clear_history(self):
        """Resets the calculator and clears the history manager."""
        self._current_value = Decimal('0')
        self._history_manager.clear()
        initial_command = ArithmeticCalculation(Decimal('0'), Decimal('0'), lambda a, b: a)
        self._save_state(initial_command)
        app_logger.info("Calculator history cleared and reset to initial state.")

    
    def load_calculation(self, calculation: ArithmeticCalculation):
        """
        Loads a single, pre-computed calculation into the calculator's
        state and history. This is used when loading from a file.
        """
        # Set the current value to the result of this loaded calculation
        self._current_value = calculation.result
        # Save this state in the history manager
        self._save_state(calculation)
        app_logger.info(f"Loaded calculation from history: {calculation.result}")