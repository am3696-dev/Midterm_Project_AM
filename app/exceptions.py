# app/exceptions.py

class CalculatorError(Exception):
    """Base exception class for all calculator-related errors."""
    pass

class OperationError(CalculatorError):
    """Raised for errors related to invalid or unsupported operations."""
    pass

class DivisionByZeroError(OperationError):
    """Raised specifically for division by zero errors."""
    pass

class ValidationError(CalculatorError):
    """Base exception for input validation errors."""
    pass

class InvalidInputError(ValidationError):
    """Raised when user input is not a valid number or command."""
    pass

class InsufficientHistoryError(CalculatorError):
    """Raised when an undo or redo operation is attempted with no history."""
    pass