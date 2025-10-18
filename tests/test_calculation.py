# tests/test_calculation.py

import pytest
from decimal import Decimal
from app.calculation import ArithmeticCalculation
from app.operations import OperationFactory
from app.exceptions import DivisionByZeroError
from app.logger import Observer
import logging # <-- ADDED THIS IMPORT

# --- Imports for AutoSave Test ---
import os
import pandas as pd
from app.history import AutoSaveObserver
from app.calculator_config import CalculatorConfig
# ------------------------------------

class MockObserver(Observer):
    """A mock observer to test the update notification."""
    def __init__(self):
        self.updated = False
        self.subject_state = None

    def update(self, subject) -> None:
        self.updated = True
        self.subject_state = subject

@pytest.fixture
def mock_observer():
    """Provides a fresh instance of MockObserver."""
    return MockObserver()

@pytest.fixture
def basic_calc():
    """Provides a simple ArithmeticCalculation instance."""
    add_func = OperationFactory.get_operation('add')
    return ArithmeticCalculation(Decimal('10'), Decimal('5'), add_func)

# --- Tests ---

def test_calculation_perform(basic_calc):
    """Tests that the perform method returns the correct result."""
    result = basic_calc.perform()
    assert result == Decimal('15')
    assert basic_calc.result == Decimal('15')

def test_calculation_perform_error():
    """Tests that perform correctly re-raises calculation errors."""
    div_func = OperationFactory.get_operation('divide')
    calc = ArithmeticCalculation(Decimal('10'), Decimal('0'), div_func)
    
    with pytest.raises(DivisionByZeroError):
        calc.perform()

def test_calculation_repr(basic_calc):
    """Tests the __repr__ method for a clear string representation."""
    assert repr(basic_calc) == "Calculation(10, 5, Operation=Add)"

def test_observer_attach_and_notify(basic_calc, mock_observer):
    """Tests that an attached observer is notified when perform() is called."""
    basic_calc.attach(mock_observer)
    basic_calc.perform()
    assert mock_observer.updated is True
    assert mock_observer.subject_state == basic_calc

def test_observer_detach(basic_calc, mock_observer):
    """Tests that a detached observer is not notified."""
    basic_calc.attach(mock_observer)
    basic_calc.detach(mock_observer)
    basic_calc.perform()
    assert mock_observer.updated is False

# --- Test for AutoSave Observer ---

def test_auto_save_observer(basic_calc):
    """Tests that the AutoSaveObserver creates a CSV file."""
    if not CalculatorConfig.AUTO_SAVE:
        pytest.skip("AUTO_SAVE is false, skipping observer test.") # pragma: no cover
    
    observer = AutoSaveObserver()
    file_path = observer.history_file_path

    if os.path.exists(file_path):
        os.remove(file_path) # pragma: no cover

    basic_calc.attach(observer)
    basic_calc.perform()

    assert os.path.exists(file_path)
    df = pd.read_csv(file_path)
    assert len(df) == 1
    assert df.iloc[0]['operation'] == 'add'
    assert df.iloc[0]['result'] == 15
    os.remove(file_path)

# --- Test for AutoSave Observer Error Handling ---

def test_auto_save_observer_handles_exception(caplog):
    """Tests that the AutoSaveObserver logs an error if saving fails."""
    if not CalculatorConfig.AUTO_SAVE:
        pytest.skip("AUTO_SAVE is false, skipping observer test.") # pragma: no cover
        
    observer = AutoSaveObserver()
    bad_subject = object() 
    
    with caplog.at_level(logging.ERROR):
        observer.update(bad_subject)
    
    assert "Failed to auto-save history" in caplog.text