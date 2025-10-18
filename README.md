# Advanced Calculator Application

## Project Description

This project is an advanced command-line calculator application built using Python. It supports standard arithmetic operations as well as additional functions like power, root, modulus, integer division, percentage calculation, and absolute difference.

The application features a Read-Eval-Print Loop (REPL) interface and utilizes several design patterns:
* **Factory Pattern:** To manage the creation of different arithmetic operations.
* **Memento Pattern:** To implement undo/redo functionality for calculations.
* **Observer Pattern:** To enable logging of calculations and automatic saving of history to a CSV file.

Configuration is managed through a `.env` file, and the application includes robust error handling and comprehensive unit tests with `pytest`. Continuous Integration (CI) is set up using GitHub Actions to ensure code quality and test coverage.

---

## Installation Instructions

1.  **Clone the repository:**
    ```bash
    git clone git@github.com:am3696-dev/Midterm_Project_AM.git
    cd Midterm_Project_AM
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
    *(On Windows, use `venv\Scripts\activate`)*

3.  **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
---

## Configuration Setup

The application uses a `.env` file in the project root directory to manage configuration settings. Create a file named `.env` and add the following variables:

```env
# .env

# --- Directory Settings ---
CALCULATOR_LOG_DIR=logs
# Directory for log files
CALCULATOR_HISTORY_DIR=history 
# Directory for history CSV file

# --- History Settings ---
CALCULATOR_MAX_HISTORY_SIZE=100
# Max history entries
CALCULATOR_AUTO_SAVE=true 
# Set to 'true' to auto-save history to CSV, 'false' to disable

# --- Calculation Settings ---
CALCULATOR_PRECISION=10        
#Decimal places for results
CALCULATOR_MAX_INPUT_VALUE=1000000000 
# Max allowed input
CALCULATOR_DEFAULT_ENCODING=utf-8 
# Default encoding for file operations

---

## Usage Guide

Run the application from the project root directory

```bash
python main.py
You will see the REPL prompt:

Enter Command >

### Arithmetic Operations  
**Usage:** `<command> <number1> <number2>`  

**Available Commands:**  
`add`, `subtract`, `multiply`, `divide`, `power`, `root`, `modulus`, `int_divide`, `percent`, `abs_diff`  

**Example:**  
```bash
add 10 5

---

## Testing Instructions

Unit tests are written using `pytest`. To run the tests and check coverage:

1.  Make sure your virtual environment is active.
2.  Run the following command from the project root directory:

    ```bash
    pytest --cov=app
    ```
    This will run all tests and display a coverage report.

    To enforce the 90% coverage requirement (as done in the CI pipeline), run:
    ```bash
    pytest --cov=app --cov-fail-under=90
    ```