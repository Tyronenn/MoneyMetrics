# MoneyMetrics

Simple PySide6 based application for experimenting with financial data.

## Features

* Modular graph screens that can be added, renamed, detached or removed.
* Data is stored separately from graph widgets allowing the user to choose
  which datasets to display.

## Setup

### Prerequisites
- Python 3.10+

### macOS/Linux
```bash
python3 -m venv venv
source venv/bin/activate
```

### Windows
```bash
python -m venv venv
venv\\Scripts\\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Run the app

The application's entry point is `money_metrics.main.main`, exposed via the
top-level `main.py` helper script. Launch the program with:

```bash
python main.py
```

## Run tests

For contributors who wish to run the test suite, first install the optional
development requirements:

```bash
pip install -r requirements-dev.txt
```

### Pytest

Execute the tests with:

```bash
pytest
```

