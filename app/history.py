# app/history.py

import os
import pandas as pd
from datetime import datetime # Import the datetime module
from app.calculator_memento import CalculatorMemento
from app.logger import app_logger, Observer
from app.calculator_config import CalculatorConfig

class HistoryManager:
    """
    The Caretaker in the Memento Pattern. It manages undo/redo stacks.
    """
    def __init__(self):
        self._undo_mementos: list[CalculatorMemento] = []
        self._redo_mementos: list[CalculatorMemento] = []
        app_logger.info("HistoryManager initialized.")

    def save_state(self, memento: CalculatorMemento):
        """Saves a new state to the undo history and clears the redo history."""
        self._undo_mementos.append(memento)
        if self._redo_mementos:
            self._redo_mementos.clear()
            app_logger.info("Redo history cleared after new state saved.")
        app_logger.info(f"State saved. Undo stack size: {len(self._undo_mementos)}")

    def undo(self) -> CalculatorMemento | None:
        """Restores the previous state, moving the current state to the redo stack."""
        if len(self._undo_mementos) > 1:
            last_memento = self._undo_mementos.pop()
            self._redo_mementos.append(last_memento)
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
        
        memento_to_restore = self._redo_mementos.pop()
        self._undo_mementos.append(memento_to_restore)
        app_logger.info(f"Redo operation. Restoring state. Undo stack: {len(self._undo_mementos)}, Redo stack: {len(self._redo_mementos)}")
        return memento_to_restore

    def get_history(self) -> list[CalculatorMemento]:
        """Returns the current list of mementos in the undo stack."""
        return list(self._undo_mementos)
    
    def clear(self):
        """Clears the undo and redo stacks."""
        self._undo_mementos.clear()
        self._redo_mementos.clear()
        app_logger.info("HistoryManager cleared.")

# --- AutoSaveObserver Class ---

class AutoSaveObserver(Observer):
    """
    An observer that automatically saves the calculation history to a CSV file.
    """
    def __init__(self):
        self.history_file_path = os.path.join(CalculatorConfig.HISTORY_DIR, 'calculations.csv')
        self._ensure_directory_exists()

    def _ensure_directory_exists(self):
        """Creates the history directory if it doesn't exist."""
        directory = os.path.dirname(self.history_file_path)
        if not os.path.exists(directory):
            os.makedirs(directory)
            app_logger.info(f"Created history directory: {directory}")

    def update(self, subject) -> None:
        """
        Saves the latest calculation to the CSV file.
        'subject' is an instance of ArithmeticCalculation.
        """
        try:
            # Get the current time and format it as a string
            timestamp = datetime.now().isoformat()

            # Create a DataFrame for the new calculation
            new_data = {
                'timestamp': [timestamp], 
                'operation': [subject.operation.__name__],
                'operand_a': [subject.a],
                'operand_b': [subject.b],
                'result': [subject.result]
            }
            df = pd.DataFrame(new_data)
            
            # Re-order columns to match the rubric
            df = df[['timestamp', 'operation', 'operand_a', 'operand_b', 'result']]
            
            if os.path.exists(self.history_file_path):
                df.to_csv(self.history_file_path, mode='a', header=False, index=False)
            else:
                df.to_csv(self.history_file_path, mode='w', header=True, index=False)
                
            app_logger.info(f"Auto-saved calculation to {self.history_file_path}")
            
        except Exception as e:
            app_logger.error(f"Failed to auto-save history: {e}")