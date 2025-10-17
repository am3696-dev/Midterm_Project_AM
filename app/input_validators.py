# app/input_validators.py

from decimal import Decimal, InvalidOperation
from app.exceptions import InvalidInputError
from app.logger import app_logger
from app.calculator_config import CalculatorConfig

class InputValidator:
    """A static class for validating user inputs."""

    @staticmethod
    def validate_operand(value: str) -> Decimal:
        """
        Validates a string to ensure it is a valid number.

        Args:
            value: The string input from the user.

        Returns:
            The input converted to a Decimal object.

        Raises:
            InvalidInputError: If the input is not a valid number.
        """
        try:
            # Convert to Decimal, which handles floats, integers, and scientific notation
            decimal_value = Decimal(value)
            
            # Optional: Check against a max value from config if it exists
            max_val = CalculatorConfig.MAX_INPUT_VALUE
            if max_val is not None and abs(decimal_value) > max_val:
                raise InvalidInputError(f"Input {decimal_value} exceeds maximum allowed value of {max_val}.")

            return decimal_value
        except InvalidOperation:
            # This is the fix: Raise the specific error with the expected message
            app_logger.warning(f"Validation Failed: '{value}' is not a valid number.")
            raise InvalidInputError(f"Invalid input: '{value}' is not a valid number.")