# MoneyMetrics

Simple PySide6 based application for experimenting with financial data.

## Features

* Modular graph and table screens that can be added, renamed, detached or
  removed.
* Data is stored separately from widgets allowing the user to choose
  which datasets to display.
* Blank landing screen with quick actions to import a profile or create
  data.
* Built-in 401(k) dataset support with editable monthly contributions and
  graph/table visualisation. 401(k) data is saved to a local JSON file and
  displayed immediately in an editable table. Columns can be renamed and
  rearranged, and parameters are added to the graph by dragging the column
  onto the plot. All edits are reflected in real time and persisted so the
  entire application state can be saved to a shareable profile. These
  behaviours form the basis for future datasets such as HSAs, brokerage
  accounts, home values, vehicles, savings accounts, bonds, stocks and
  cryptocurrencies.

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

The application can be launched directly as a module thanks to the
``money_metrics.__main__`` entry point:

```bash
python -m money_metrics
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

