# app/calculator_config.py

import os
from dotenv import load_dotenv
from decimal import getcontext, Decimal
import logging 

# Set up basic logging for config messages before the main app logger is configured
logging.basicConfig(level=logging.INFO)

# Load environment variables from .env file
load_dotenv()

class CalculatorConfig:
    """Class to manage and validate all application configuration settings."""
    
    # --- Default Values ---
    DEFAULTS = {
        'LOG_DIR': 'logs',
        'LOG_FILE': 'calculator_app.log',
        'HISTORY_DIR': 'history_data',
        'MAX_HISTORY_SIZE': 100,
        'AUTO_SAVE': 'true',
        'PRECISION': 20,
        'MAX_INPUT_VALUE': 1e20, # 1 followed by 20 zeros
        'DEFAULT_ENCODING': 'utf-8',
        'LOG_LEVEL': 'INFO'
    }

    @classmethod
    def load_config(cls):
        """Loads, validates, and sets all configuration parameters."""
        
        # --- Base Directories and Files ---
        cls.LOG_LEVEL = os.getenv('LOG_LEVEL', cls.DEFAULTS['LOG_LEVEL'])
        cls.LOG_DIR = os.getenv('CALCULATOR_LOG_DIR', cls.DEFAULTS['LOG_DIR'])
        cls.LOG_FILE = os.getenv('CALCULATOR_LOG_FILE', cls.DEFAULTS['LOG_FILE']) 
        cls.HISTORY_DIR = os.getenv('CALCULATOR_HISTORY_DIR', cls.DEFAULTS['HISTORY_DIR'])
        
        # --- History Settings ---
        try:
            # Load and validate MAX_HISTORY_SIZE
            cls.MAX_HISTORY_SIZE = int(os.getenv('CALCULATOR_MAX_HISTORY_SIZE', cls.DEFAULTS['MAX_HISTORY_SIZE']))
            if cls.MAX_HISTORY_SIZE < 0:
                raise ValueError
        except ValueError:
            logging.warning("Invalid CALCULATOR_MAX_HISTORY_SIZE. Using default: 100")
            cls.MAX_HISTORY_SIZE = cls.DEFAULTS['MAX_HISTORY_SIZE']

        # Boolean conversion (any case-insensitive variation of 'true' is True)
        auto_save_str = os.getenv('CALCULATOR_AUTO_SAVE', cls.DEFAULTS['AUTO_SAVE']).lower()
        cls.AUTO_SAVE = auto_save_str in ('true', '1', 't', 'y', 'yes')

        # --- Calculation Settings ---
        try:
            # Load, validate, and set global Decimal precision
            cls.PRECISION = int(os.getenv('CALCULATOR_PRECISION', cls.DEFAULTS['PRECISION']))
            if cls.PRECISION < 1:
                raise ValueError("Precision must be a positive integer.")
            getcontext().prec = cls.PRECISION
            logging.info(f"Decimal precision set to {cls.PRECISION}")
        except ValueError as e:
            logging.error(f"Invalid CALCULATOR_PRECISION: {e}. Using default: 20")
            cls.PRECISION = cls.DEFAULTS['PRECISION']
            getcontext().prec = cls.DEFAULTS['PRECISION']

        try:
            # Load and convert MAX_INPUT_VALUE to Decimal
            max_input_str = os.getenv('CALCULATOR_MAX_INPUT_VALUE', cls.DEFAULTS['MAX_INPUT_VALUE'])
            cls.MAX_INPUT_VALUE = Decimal(str(max_input_str))
        except Exception:
            logging.warning("Invalid CALCULATOR_MAX_INPUT_VALUE. Using default (1e20).")
            cls.MAX_INPUT_VALUE = Decimal(str(cls.DEFAULTS['MAX_INPUT_VALUE']))

        cls.DEFAULT_ENCODING = os.getenv('CALCULATOR_DEFAULT_ENCODING', cls.DEFAULTS['DEFAULT_ENCODING'])
        
        logging.info("Configuration successfully loaded and validated.")


# Load configuration immediately on import
CalculatorConfig.load_config()