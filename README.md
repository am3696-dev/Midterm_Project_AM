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