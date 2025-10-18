# tests/test_calculator.py

import pytest
from decimal import Decimal
from app.calculator import Calculator
from app.calculation import ArithmeticCalculation
from app.operations import OperationFactory
from app.exceptions import InsufficientHistoryError

import pandas as pd
import os
from app.calculator_config import CalculatorConfig
from app.logger import Observer # For observer tests

# Helper function to create commands for tests
def create_command(op_name, a_val, b_val):
    """Creates an ArithmeticCalculation command for testing."""
    op_func = OperationFactory.get_operation(op_name)
    return ArithmeticCalculation(Decimal(a_val), Decimal(b_val), op_func)

@pytest.fixture
def clean_calculator():
    """Provides a fresh Calculator instance."""
    return Calculator()

def test_calculator_initial_state(clean_calculator):
    """Tests that the calculator initializes with a value of 0."""
    assert clean_calculator.get_current_value() == Decimal('0')

def test_calculator_execution(clean_calculator):
    """Tests basic execution of a command."""
    command = create_command('add', '10', '5')
    clean_calculator.execute_command(command)
    assert clean_calculator.get_current_value() == Decimal('15')

def test_undo_functionality(clean_calculator):
    """Tests the basic undo of the last successful operation."""
    clean_calculator.execute_command(create_command('add', '10', '0'))      # Value is 10
    clean_calculator.execute_command(create_command('subtract', '20', '5')) # Value is 15
    clean_calculator.undo() # Should revert to 10
    assert clean_calculator.get_current_value() == Decimal('10')

def test_redo_functionality(clean_calculator):
    """Tests the basic redo of the last undone operation."""
    clean_calculator.execute_command(create_command('add', '10', '0'))      # Value is 10
    clean_calculator.execute_command(create_command('subtract', '20', '5')) # Value is 15
    clean_calculator.undo() # Back to 10
    clean_calculator.redo() # Forward to 15
    assert clean_calculator.get_current_value() == Decimal('15')

def test_undo_limits(clean_calculator):
    """Tests that undoing beyond the start state raises an error."""
    clean_calculator.execute_command(create_command('add', '1', '1'))
    clean_calculator.undo() # Back to initial state (0)
    with pytest.raises(InsufficientHistoryError):
        clean_calculator.undo() # Should fail

def test_redo_without_undo(clean_calculator):
    """Tests that redo does nothing without a prior undo."""
    clean_calculator.execute_command(create_command('add', '10', '5'))
    with pytest.raises(InsufficientHistoryError):
        clean_calculator.redo()

def test_new_action_clears_redo_stack(clean_calculator):
    """Tests that performing a new calculation clears the redo stack."""
    clean_calculator.execute_command(create_command('add', '10', '0'))      # Value becomes 10
    clean_calculator.execute_command(create_command('add', '5', '0'))       # Value becomes 5
    clean_calculator.undo()                                                 # Value reverts to 10
    clean_calculator.execute_command(create_command('multiply', '4', '3'))  # New value is 12
    with pytest.raises(InsufficientHistoryError):
        clean_calculator.redo()
    assert clean_calculator.get_current_value() == Decimal('12')

# --- Tests for Calculation and Observer Pattern ---

def test_calculation_repr():
    """Tests the __repr__ method of ArithmeticCalculation for correct string representation."""
    command = create_command('add', '10', '5')
    assert repr(command) == "Calculation(10, 5, Operation=Add)"

def test_observer_detach():
    """Tests that an observer can be successfully detached from a calculation."""
    command = create_command('add', '1', '1')
    
    class MockObserver(Observer):
        def update(self, subject) -> None:
            pass # pragma: no cover
            
    observer = MockObserver()
    command.attach(observer)
    assert len(command._observers) == 1
    command.detach(observer)
    assert len(command._observers) == 0

def test_calculation_perform_error():
    """Tests that the perform method in a calculation correctly re-raises exceptions."""
    command = create_command('divide', '10', '0')
    with pytest.raises(Exception):
        command.perform()

# --- NEW TEST FOR LOAD COMMAND ---

def test_calculator_load_calculation(clean_calculator):
    """Tests that the load_calculation method correctly updates state and history."""
    
    # Create a sample calculation object as if it were loaded
    op_func = OperationFactory.get_operation('add')
    calc = ArithmeticCalculation(Decimal('100'), Decimal('50'), op_func)
    calc.result = Decimal('150') # Manually set the result
    
    # Load it into the calculator
    clean_calculator.load_calculation(calc)
    
    # Check that the current value is updated
    assert clean_calculator.get_current_value() == Decimal('150')
    
    # Check that it was added to the history
    history = clean_calculator.get_history()
    assert len(history) == 2 # (Initial '0' state + our loaded state)
    assert history[-1].get_last_command().result == Decimal('150')