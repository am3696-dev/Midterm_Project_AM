# tests/test_operations.py

import pytest
from decimal import Decimal
import math
from app.operations import Operations, OperationFactory
from app.exceptions import DivisionByZeroError, ValidationError

# Configure Decimal context for testing
# We use a higher precision here to ensure internal consistency, matching our config default (20)
from decimal import getcontext
getcontext().prec = 20

# --- Parameterized Tests for Binary Operations ---
# Format: (operation_name, a, b, expected_result)
test_data = [
    # Core Operations
    ('add', '10', '5', Decimal('15')),
    ('subtract', '10', '5', Decimal('5')),
    ('multiply', '10', '5', Decimal('50')),
    ('divide', '10', '4', Decimal('2.5')),
    # Additional Mandatory Operations
    ('power', '2', '3', Decimal('8')),
    ('power', '4', '0.5', Decimal('2')), # Square root via power
    ('root', '8', '3', Decimal(math.pow(8, 1/3))), # Cube root of 8
    ('root', '16', '4', Decimal(math.pow(16, 1/4))), # 4th root of 16
    ('modulus', '10', '3', Decimal('1')),
    ('integer_division', '10', '3', Decimal('3')),
    ('percentage', '25', '100', Decimal('25')), # 25 is 25% of 100
    ('absolute_difference', '5', '15', Decimal('10')),
    ('absolute_difference', '15', '5', Decimal('10')),
    # Floating point precision check
    ('divide', '1', '3', Decimal('0.33333333333333333333'))
]

@pytest.mark.parametrize("operation_name, a, b, expected_result", test_data)
def test_binary_operations_success(operation_name, a, b, expected_result):
    """Tests all standard and mandatory binary operations for correctness."""
    op_func = OperationFactory.get_operation(operation_name)
    result = op_func(Decimal(a), Decimal(b))
    
    # We use a small tolerance for the math.pow results due to float conversion
    if operation_name in ['root']:
        assert result == pytest.approx(expected_result)
    else:
        assert result == expected_result

# --- Edge Case Tests ---

def test_division_by_zero():
    """Tests that all division-related operations handle division by zero."""
    with pytest.raises(DivisionByZeroError):
        Operations.divide(Decimal('10'), Decimal('0'))
    with pytest.raises(DivisionByZeroError):
        Operations.modulus(Decimal('10'), Decimal('0'))
    with pytest.raises(DivisionByZeroError):
        Operations.integer_division(Decimal('10'), Decimal('0'))
    with pytest.raises(DivisionByZeroError):
        Operations.percentage(Decimal('10'), Decimal('0'))
    with pytest.raises(DivisionByZeroError):
        # Specific root test for b=0
        Operations.root(Decimal('8'), Decimal('0'))

def test_factory_invalid_operation():
    """Tests the OperationFactory raises ValidationError for unsupported commands."""
    with pytest.raises(ValidationError) as excinfo:
        OperationFactory.get_operation('invalid_command')
    assert "Invalid operation" in str(excinfo.value)

# --- Append these new tests to the end of tests/test_operations.py ---

from app.input_validators import InputValidator
from app.exceptions import InvalidInputError

# --- Tests for InputValidator ---

def test_validate_valid_operands():
    """Tests that valid string numbers are correctly converted to Decimal."""
    assert InputValidator.validate_operand("10") == Decimal("10")
    assert InputValidator.validate_operand("-5.5") == Decimal("-5.5")
    assert InputValidator.validate_operand("0") == Decimal("0")

def test_validate_invalid_operands_raises_error():
    """Tests that non-numeric strings raise InvalidInputError."""
    with pytest.raises(InvalidInputError, match="Invalid input: 'abc' is not a valid number."):
        InputValidator.validate_operand("abc")
    
    with pytest.raises(InvalidInputError, match="Invalid input: '' is not a valid number."):
        InputValidator.validate_operand("")
        
    with pytest.raises(InvalidInputError, match="Invalid input: '1 2' is not a valid number."):
        InputValidator.validate_operand("1 2")