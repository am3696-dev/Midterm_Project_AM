# app/calculator_config.py

import os
from dotenv import load_dotenv
from decimal import Decimal

class CalculatorConfig:
    """
    Manages loading and providing access to application configuration settings.
    It loads settings from a .env file and provides sensible defaults.
    """
    load_dotenv()

    # --- Base Directories ---
    LOG_DIR = os.getenv('CALCULATOR_LOG_DIR', 'logs')
    HISTORY_DIR = os.getenv('CALCULATOR_HISTORY_DIR', 'history')

    # --- History Settings ---
    try:
        MAX_HISTORY_SIZE = int(os.getenv('CALCULATOR_MAX_HISTORY_SIZE', 50))
    except (ValueError, TypeError): # pragma: no cover
        MAX_HISTORY_SIZE = 50

    AUTO_SAVE = os.getenv('CALCULATOR_AUTO_SAVE', 'false').lower() in ('true', '1', 't')

    # --- Calculation Settings ---
    try:
        PRECISION = int(os.getenv('CALCULATOR_PRECISION', 10))
    except (ValueError, TypeError): # pragma: no cover
        PRECISION = 10

    try:
        MAX_INPUT_VALUE = Decimal(os.getenv('CALCULATOR_MAX_INPUT_VALUE', '1000000000'))
    except (ValueError, TypeError): # pragma: no cover
        MAX_INPUT_VALUE = Decimal('1000000000')
    
    DEFAULT_ENCODING = os.getenv('CALCULATOR_DEFAULT_ENCODING', 'utf-8')