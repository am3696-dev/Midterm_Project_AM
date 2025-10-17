# app/operations.py

from decimal import Decimal, InvalidOperation
from app.exceptions import DivisionByZeroError, ValidationError

class Operations:
    """A static class to hold all arithmetic operations."""

    @staticmethod
    def add(a: Decimal, b: Decimal) -> Decimal:
        return a + b

    @staticmethod
    def subtract(a: Decimal, b: Decimal) -> Decimal:
        return a - b

    @staticmethod
    def multiply(a: Decimal, b: Decimal) -> Decimal:
        return a * b

    @staticmethod
    def divide(a: Decimal, b: Decimal) -> Decimal:
        if b == 0:
            raise DivisionByZeroError("Division by zero is not allowed.")
        return a / b

    @staticmethod
    def power(a: Decimal, b: Decimal) -> Decimal:
        return a ** b

    @staticmethod
    def root(a: Decimal, b: Decimal) -> Decimal:
        if a < 0 and b % 2 == 0:
            raise ValidationError("Cannot take an even root of a negative number.")
        # --- THIS IS THE FIX ---
        if b == 0:
            # Changed from ValidationError to DivisionByZeroError to match the test
            raise DivisionByZeroError("Root with an index of zero is undefined.")
        return a ** (Decimal('1.0') / b)

    @staticmethod
    def modulus(a: Decimal, b: Decimal) -> Decimal:
        if b == 0:
            raise DivisionByZeroError("Modulus by zero is not allowed.")
        return a % b

    @staticmethod
    def integer_division(a: Decimal, b: Decimal) -> Decimal:
        if b == 0:
            raise DivisionByZeroError("Integer division by zero is not allowed.")
        return a // b

    @staticmethod
    def percentage(a: Decimal, b: Decimal) -> Decimal:
        if b == 0:
            raise DivisionByZeroError("Percentage calculation with respect to zero is not allowed.")
        return (a / b) * 100

    @staticmethod
    def absolute_difference(a: Decimal, b: Decimal) -> Decimal:
        return abs(a - b)

class OperationFactory:
    """The Factory class to create operation instances."""

    OPERATION_MAP = {
        'add': Operations.add,
        'subtract': Operations.subtract,
        'multiply': Operations.multiply,
        'divide': Operations.divide,
        'power': Operations.power,
        'root': Operations.root,
        'modulus': Operations.modulus,
        'int_divide': Operations.integer_division,
        'integer_division': Operations.integer_division,
        'percent': Operations.percentage,
        'percentage': Operations.percentage,
        'abs_diff': Operations.absolute_difference,
        'absolute_difference': Operations.absolute_difference
    }

    @staticmethod
    def get_operation(operation_name: str):
        operation_name = operation_name.lower()
        op_func = OperationFactory.OPERATION_MAP.get(operation_name)
        if not op_func:
            raise ValidationError(f"Error: Invalid operation '{operation_name}'.")
        return op_func