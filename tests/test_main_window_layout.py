import pytest

pytest.importorskip("PySide6.QtWidgets")
from PySide6.QtWidgets import QApplication, QPushButton

from money_metrics.ui.main_window import MainWindow
from money_metrics.core.profile import AppProfile


@pytest.fixture(scope="module")
def app():
    try:
        app = QApplication.instance() or QApplication([])
    except Exception:
        pytest.skip("Qt GUI not available")
    yield app


def test_default_home_layout_has_buttons(app):
    window = MainWindow()
    central = window.centralWidget()
    texts = sorted(btn.text() for btn in central.findChildren(QPushButton))
    assert texts == ["Create Data", "Import Profile"]


def test_profile_load_replaces_home_layout(app):
    profile = AppProfile(
        datasets={"Sample": [1, 2, 3]},
        screens=[{"title": "Graph 1", "dataset": "Sample"}],
    )
    window = MainWindow()
    window._apply_profile(profile)
    assert not window.centralWidget().findChildren(QPushButton)


def test_plot_hides_central_widget(app):
    window = MainWindow()
    window.add_plot_screen()
    assert not window.centralWidget().isVisible()
