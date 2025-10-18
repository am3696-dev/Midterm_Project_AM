# tests/test_calculation.py

import pytest
from decimal import Decimal
from app.calculation import ArithmeticCalculation
from app.operations import OperationFactory
from app.exceptions import DivisionByZeroError
from app.logger import Observer

# --- Fixture for a simple mock observer ---

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

# --- Fixture for a basic calculation ---

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
    assert basic_calc.result == Decimal('15') # Check that the result is stored

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
    
    # Perform the calculation
    basic_calc.perform()
    
    # Check that the observer's update method was called
    assert mock_observer.updated is True
    # Check that the observer received the correct subject state
    assert mock_observer.subject_state == basic_calc
    assert mock_observer.subject_state.result == Decimal('15')

def test_observer_detach(basic_calc, mock_observer):
    """Tests that a detached observer is not notified."""
    basic_calc.attach(mock_observer)
    basic_calc.detach(mock_observer) # Detach immediately
    
    basic_calc.perform()
    
    # Check that the observer was NOT updated
    assert mock_observer.updated is False