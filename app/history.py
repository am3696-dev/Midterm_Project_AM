# app/history.py

from app.calculator_memento import CalculatorMemento
from app.logger import app_logger

class HistoryManager:
    """
    The Caretaker in the Memento Pattern. It is responsible for managing
    the history of states (mementos) for undo and redo operations.
    """
    def __init__(self):
        self._undo_mementos: list[CalculatorMemento] = []
        self._redo_mementos: list[CalculatorMemento] = []
        app_logger.info("HistoryManager initialized.")

    def save_state(self, memento: CalculatorMemento):
        """Saves a new state to the undo history and clears the redo history."""
        self._undo_mementos.append(memento)
        # When a new state is saved, any previous "redo" path is invalidated.
        if self._redo_mementos:
            self._redo_mementos.clear()
            app_logger.info("Redo history cleared after new state saved.")
        app_logger.info(f"State saved. Undo stack size: {len(self._undo_mementos)}")

    def undo(self) -> CalculatorMemento | None:
        """
        Moves the most recent state from the undo stack to the redo stack
        and returns the new current state (the top of the undo stack).
        """
        if len(self._undo_mementos) > 1:
            # Move the current state to the redo stack
            last_memento = self._undo_mementos.pop()
            self._redo_mementos.append(last_memento)
            
            # The new current state is now the last one in the undo list
            current_memento = self._undo_mementos[-1]
            
            app_logger.info(f"Undo operation. Restoring state. Undo stack: {len(self._undo_mementos)}, Redo stack: {len(self._redo_mementos)}")
            return current_memento
        
        app_logger.warning("Undo operation failed: No more states in undo history.")
        return None

    def redo(self) -> CalculatorMemento | None:
        """Moves a state from the redo stack back to the undo stack."""
        if not self._redo_mementos:
            app_logger.warning("Redo operation failed: No states in redo history.")
            return None
        
        # Move the state from redo back to undo
        memento_to_restore = self._redo_mementos.pop()
        self._undo_mementos.append(memento_to_restore)
        
        app_logger.info(f"Redo operation. Restoring state. Undo stack: {len(self._undo_mementos)}, Redo stack: {len(self._redo_mementos)}")
        return memento_to_restore