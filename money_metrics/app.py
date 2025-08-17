"""Application bootstrap for MoneyMetrics."""

import sys
from PySide6.QtWidgets import QApplication, QFileDialog

from money_metrics.ui.main_window import MainWindow
from money_metrics.core.profile import AppProfile


def main() -> None:
    """Launch the MoneyMetrics GUI."""
    app = QApplication(sys.argv)
    path, _ = QFileDialog.getOpenFileName(
        None, "Open Profile", filter="MoneyMetrics Profile (*.json)"
    )
    profile = AppProfile.load_from_file(path) if path else None
    window = MainWindow(profile)
    if path:
        window.profile_path = path
    window.show()
    sys.exit(app.exec())

