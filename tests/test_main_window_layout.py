import pytest

pytest.importorskip("PySide6.QtWidgets")
from PySide6.QtWidgets import QApplication, QTabWidget

from money_metrics.ui.main_window import MainWindow
from money_metrics.core.profile import AppProfile


@pytest.fixture(scope="module")
def app():
    try:
        app = QApplication.instance() or QApplication([])
    except Exception:
        pytest.skip("Qt GUI not available")
    yield app


def test_default_home_layout_has_tabs(app):
    window = MainWindow()
    assert isinstance(window.centralWidget(), QTabWidget)
    assert window.centralWidget().tabPosition() == QTabWidget.North


def test_profile_load_replaces_home_layout(app):
    profile = AppProfile(
        datasets={"Sample": [1, 2, 3]},
        screens=[{"title": "Graph 1", "dataset": "Sample"}],
    )
    window = MainWindow()
    window._apply_profile(profile)
    assert not isinstance(window.centralWidget(), QTabWidget)
