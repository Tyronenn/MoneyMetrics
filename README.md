# MoneyMetrics

Simple PySide6 based application for experimenting with financial data.

## Features

* Modular graph screens that can be added, renamed, detached or removed.
* Data is stored separately from graph widgets allowing the user to choose
  which datasets to display.

## Setup

### Prerequisites
- Python 3.10+

### Automatic setup

Create a virtual environment and install dependencies with the provided script:

```bash
python setup_env.py            # runtime dependencies only
python setup_env.py --dev      # include dev/test requirements (optional)
```

### Activate the environment

- **macOS/Linux**

  ```bash
  source venv/bin/activate
  ```

- **Windows**

  ```bash
  venv\Scripts\activate
  ```

## Run the app

The application's entry point is `money_metrics.main.main`, exposed via the
top-level `main.py` helper script. Launch the program with:

```bash
python main.py
```

## Run tests

For contributors who wish to run the test suite, install the additional
development requirements (if not already installed) with:

```bash
python setup_env.py --dev
```

### Pytest

Execute the tests with:

```bash
pytest
```

## Troubleshooting

### macOS

If installing Qt or PySide fails, install the Xcode command line tools:

```bash
xcode-select --install
```

### Windows

Some dependencies may require Microsoft's C++ build tools. If installation
fails, install the [Microsoft C++ Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/).

