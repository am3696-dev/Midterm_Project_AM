# main.py

import sys
from decimal import Decimal
import os
import pandas as pd

from app.calculator import Calculator
from app.calculation import ArithmeticCalculation
from app.input_validators import InputValidator
from app.exceptions import ValidationError, OperationError, InsufficientHistoryError
from app.operations import OperationFactory
from app.logger import setup_logging, app_logger, LoggingObserver
from app.calculator_config import CalculatorConfig
from app.history import AutoSaveObserver 

# 1. CRITICAL STEP: Call the logger setup first
setup_logging()

# 2. Initialize core services
CALCULATOR = Calculator()
LOGGING_OBSERVER = LoggingObserver()

AUTOSAVE_OBSERVER = None
if CalculatorConfig.AUTO_SAVE:
    AUTOSAVE_OBSERVER = AutoSaveObserver()
    app_logger.info("AutoSaveObserver initialized.")

class Cli:
    """Command-Line Interface (REPL) for the Advanced Calculator Application."""
    def __init__(self, calculator: Calculator):
        self.calculator = calculator
        self.commands = self._setup_commands()
        app_logger.info("CLI initialized.")

    def _setup_commands(self) -> dict:
        binary_ops = [
            'add', 'subtract', 'multiply', 'divide', 'power', 'root',
            'modulus', 'int_divide', 'percent', 'abs_diff'
        ]
        command_map = {cmd: self._handle_binary_operation for cmd in binary_ops}
        command_map.update({
            'history': self._handle_history, 'clear': self._handle_clear,
            'undo': self._handle_undo, 'redo': self._handle_redo,
            'save': self._handle_save, 'load': self._handle_load,
            'help': self._handle_help, 'exit': self._handle_exit, 'quit': self._handle_exit
        })
        return command_map

    def _handle_binary_operation(self, command: str, operands: list):
        if len(operands) != 2:
            print("Error: Arithmetic commands require exactly two operands (e.g., add 1 1).")
            return
        try:
            a = InputValidator.validate_operand(operands[0])
            b = InputValidator.validate_operand(operands[1])
            operation_func = OperationFactory.get_operation(command)
            calculation = ArithmeticCalculation(a, b, operation_func)
            
            calculation.attach(LOGGING_OBSERVER)
            if AUTOSAVE_OBSERVER:
                calculation.attach(AUTOSAVE_OBSERVER)
                
            self.calculator.execute_command(calculation)
            print(f"Result: {self.calculator.get_current_value()}")
        except (ValidationError, OperationError, Exception) as e:
            print(f"Error: {e}")
            app_logger.error(f"Failed to execute command '{command}': {e}", exc_info=False)

    def _handle_undo(self, *args):
        try:
            self.calculator.undo()
            print(f"Undo successful. Current value: {self.calculator.get_current_value()}")
        except InsufficientHistoryError as e:
            print(f"Error: {e}")

    def _handle_redo(self, *args):
        try:
            self.calculator.redo()
            print(f"Redo successful. Current value: {self.calculator.get_current_value()}")
        except InsufficientHistoryError as e:
            print(f"Error: {e}")

    def _handle_history(self, *args):
        history = self.calculator.get_history()
        if len(history) <= 1: 
            print("No calculations in history yet.")
            return

        print("\n--- Calculation History ---")
        for memento in history[1:]:
            calc = memento.get_last_command()
            print(f"{calc.operation.__name__.title()}({calc.a}, {calc.b}) = {calc.result}")
        print("--------------------------")

    def _handle_clear(self, *args):
        self.calculator.clear_history()
        print("In-memory history cleared. Calculator reset to 0.")
        
    def _handle_save(self, *args):
        print("Feature TBD: Manual history save.")

    def _handle_load(self, *args):
        print("Feature TBD: History load.")

    def _handle_help(self, *args):
        print("\n--- Available Commands ---")
        binary_ops = [k for k, v in self.commands.items() if v == self._handle_binary_operation]
        util_ops = [k for k, v in self.commands.items() if v != self._handle_binary_operation]
        print(f"\n[Arithmetic Commands (Usage: <command> <number1> <number2>)]\n  {', '.join(binary_ops)}")
        print(f"\n[Utility Commands (Usage: <command>)]\n  {', '.join(util_ops)}")
        print("\n--------------------------")

    def _handle_exit(self, *args):
        print("Exiting calculator. Goodbye!")
        sys.exit(0)

    def start(self):
        """Runs the main Read-Eval-Print Loop (REPL)."""
        print("\n==============================================")
        print("   Welcome to the Advanced Calculator REPL!")
        print(f"   Initial Value: {self.calculator.get_current_value()}")
        print("   Type 'help' for commands or 'exit' to quit.")
        print("==============================================\n")
        while True:
            try:
                user_input = input("Enter Command > ").strip().lower()
                
                if not user_input: continue
                parts = user_input.split()
                command, operands = parts[0], parts[1:]
                handler = self.commands.get(command)
                if handler:
                    if handler == self._handle_binary_operation: handler(command, operands)
                    else: handler(*operands)
                else:
                    print(f"Error: Unknown command '{command}'. Type 'help' for available commands.")
            except KeyboardInterrupt: self._handle_exit()
            except Exception as e:
                app_logger.critical(f"An unexpected error occurred in the REPL: {e}", exc_info=True)
                print(f"An unexpected error occurred. Please check the logs.")

if __name__ == '__main__':
    try:
        cli = Cli(CALCULATOR)
        cli.start()
    except Exception as e:
        app_logger.critical(f"Failed to start the application: {e}", exc_info=True)
        print(f"CRITICAL ERROR: Failed to initialize application. Check logs for details.")