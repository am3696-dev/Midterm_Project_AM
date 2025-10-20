# main.py

import sys
from decimal import Decimal
import os
import pandas as pd
import colorama # Import colorama
from colorama import Fore, Style # Import Fore and Style for colors

from app.calculator import Calculator
from app.calculation import ArithmeticCalculation
from app.input_validators import InputValidator
from app.exceptions import ValidationError, OperationError, InsufficientHistoryError
from app.operations import OperationFactory
from app.logger import setup_logging, app_logger, LoggingObserver
from app.calculator_config import CalculatorConfig
from app.history import AutoSaveObserver

# Initialize colorama
colorama.init(autoreset=True)

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
            # Print error in Red
            print(f"{Fore.RED}Error: Arithmetic commands require exactly two operands (e.g., add 1 1).{Style.RESET_ALL}")
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
            # Print result in Green
            print(f"{Fore.GREEN}Result: {self.calculator.get_current_value()}{Style.RESET_ALL}")
        except (ValidationError, OperationError, Exception) as e:
            # Print error in Red
            print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
            app_logger.error(f"Failed to execute command '{command}': {e}", exc_info=False)

    def _handle_undo(self, *args):
        try:
            self.calculator.undo()
            # Print success in Green
            print(f"{Fore.GREEN}Undo successful. Current value: {self.calculator.get_current_value()}{Style.RESET_ALL}")
        except InsufficientHistoryError as e:
            # Print error in Red
            print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")

    def _handle_redo(self, *args):
        try:
            self.calculator.redo()
            # Print success in Green
            print(f"{Fore.GREEN}Redo successful. Current value: {self.calculator.get_current_value()}{Style.RESET_ALL}")
        except InsufficientHistoryError as e:
            # Print error in Red
            print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")

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
        file_path = os.path.join(CalculatorConfig.HISTORY_DIR, 'calculations.csv')

        if not os.path.exists(file_path):
            # Print error in Red
            print(f"{Fore.RED}Error: History file not found at {file_path}{Style.RESET_ALL}")
            app_logger.warning(f"History file not found: {file_path}")
            return

        try:
            df = pd.read_csv(file_path)
            if df.empty:
                print("History file is empty.")
                app_logger.info("History file is empty. No history loaded.")
                return

            self.calculator.clear_history()

            print("Loading history...")
            for index, row in df.iterrows():
                op_func = OperationFactory.get_operation(row['operation'])
                a = Decimal(str(row['operand_a']))
                b = Decimal(str(row['operand_b']))
                result = Decimal(str(row['result']))

                calc = ArithmeticCalculation(a, b, op_func)
                calc.result = result

                self.calculator.load_calculation(calc)

            # Print success in Green
            print(f"{Fore.GREEN}History successfully loaded. Current value is {self.calculator.get_current_value()}{Style.RESET_ALL}")
            app_logger.info("Calculation history successfully loaded from CSV.")

        except pd.errors.EmptyDataError:
            print("History file is empty. No history to load.")
            app_logger.warning("History file is empty. No history loaded.")
        except Exception as e:
             # Print error in Red
            print(f"{Fore.RED}Error loading history: {e}{Style.RESET_ALL}")
            app_logger.error(f"Failed to load history from CSV: {e}", exc_info=True)

    def _handle_help(self, *args):
        print("\n--- Available Commands ---")
        binary_ops = [k for k, v in self.commands.items() if v == self._handle_binary_operation]
        util_ops = [k for k, v in self.commands.items() if v != self._handle_binary_operation]
        print(f"\n[Arithmetic Commands (Usage: <command> <number1> <number2>)]\n  {', '.join(binary_ops)}")
        print(f"\n[Utility Commands (Usage: <command>)]\n  {', '.join(util_ops)}")
        print("\n--------------------------")

    def _handle_exit(self, *args):
        print("Exiting Artan's calculator. Goodbye!")
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
                    # Print error in Red
                    print(f"{Fore.RED}Error: Unknown command '{command}'. Type 'help' for available commands.{Style.RESET_ALL}")
            except KeyboardInterrupt: self._handle_exit()
            except Exception as e:
                app_logger.critical(f"An unexpected error occurred in the REPL: {e}", exc_info=True)
                # Print error in Red
                print(f"{Fore.RED}An unexpected error occurred. Please check the logs.{Style.RESET_ALL}")

if __name__ == '__main__':
    try:
        cli = Cli(CALCULATOR)
        cli.start()
    except Exception as e:
        app_logger.critical(f"Failed to start the application: {e}", exc_info=True)
        # Print error in Red
        print(f"{Fore.RED}CRITICAL ERROR: Failed to initialize application. Check logs for details.{Style.RESET_ALL}")