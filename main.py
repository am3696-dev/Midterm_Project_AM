# app/calculator.py

from decimal import Decimal

from app.calculation import ArithmeticCalculation
from app.calculator_memento import CalculatorMemento
from app.history import HistoryManager
from app.exceptions import InsufficientHistoryError
from app.logger import app_logger

class Calculator:
    """
    The Originator in the Memento Pattern. It holds the current state
    and can create mementos of its state or restore its state from them.
    """
    def __init__(self):
        """Initializes the calculator with a starting value of 0."""
        self._current_value = Decimal('0')
        self._history_manager = HistoryManager()
        # Save the initial state so we can always undo back to the beginning.
        # We create a dummy calculation to represent the initial state.
        initial_command = ArithmeticCalculation(Decimal('0'), Decimal('0'), lambda a, b: a)
        self._save_initial_state(initial_command)

    def _save_initial_state(self, command: ArithmeticCalculation):
        """Saves the initial state of the calculator."""
        memento = CalculatorMemento(self._current_value, command)
        self._history_manager.save_state(memento)
        app_logger.info("Calculator initialized and initial state saved.")

    def execute_command(self, command: ArithmeticCalculation) -> Decimal:
        """
        Executes a calculation command, updates the current value,
        and saves the new state as a memento.
        """
        result = command.perform()
        self._current_value = result
        
        # Create and save a memento of the new state
        memento = CalculatorMemento(self._current_value, command)
        self._history_manager.save_state(memento)
        
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
        """Restores a previously undone state from the history manager."""
        memento = self._history_manager.redo()
        if memento is None:
            raise InsufficientHistoryError("Cannot redo: No more states to restore.")
            
        self._current_value = memento.get_state_value()
        app_logger.info(f"Redo successful. Restored value: {self._current_value}")

    def get_current_value(self) -> Decimal:
        """Returns the current value of the calculator."""
        return self._current_value

    def get_history(self) -> list[ArithmeticCalculation]:
        """Retrieves the list of executed commands from the history manager's mementos."""
        # This assumes the history manager's undo stack holds the mementos
        return [memento.get_last_command() for memento in self._history_manager._undo_mementos]

    def clear_history(self):
        """Resets the calculator to its initial state."""
        self._current_value = Decimal('0')
        self._history_manager = HistoryManager()
        initial_command = ArithmeticCalculation(Decimal('0'), Decimal('0'), lambda a, b: a)
        self._save_initial_state(initial_command)
        app_logger.info("Calculator history cleared and reset to initial state.")