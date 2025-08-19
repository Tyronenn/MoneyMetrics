"""Application bootstrap for MoneyMetrics."""

import sys
from PySide6.QtWidgets import QApplication

from money_metrics.ui.main_window import MainWindow


def main() -> None:
    """Launch the MoneyMetrics GUI."""
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

