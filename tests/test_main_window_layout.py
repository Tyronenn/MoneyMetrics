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


def test_import_profile_hides_home_layout(app, tmp_path, monkeypatch):
    profile = AppProfile(
        datasets={"Sample": [{"balance": 1}, {"balance": 2}]},
        screens=[{"title": "Graph 1", "dataset": "Sample"}],
    )
    path = tmp_path / "profile.json"
    profile.save_to_file(path)
    monkeypatch.setattr(
        "money_metrics.ui.main_window.QFileDialog.getOpenFileName",
        lambda *args, **kwargs: (str(path), ""),
    )
    window = MainWindow()
    window._load_profile_dialog()
    assert not window.centralWidget().findChildren(QPushButton)
    assert window.graph_screens and window.graph_screens[0].view_mode == "table"


def test_create_data_hides_home_layout(app, monkeypatch):
    doubles = iter([(100.0, True), (0.01, True)])
    monkeypatch.setattr(
        "money_metrics.ui.main_window.QInputDialog.getDouble",
        lambda *args, **kwargs: next(doubles),
    )
    monkeypatch.setattr(
        "money_metrics.ui.main_window.QInputDialog.getInt",
        lambda *args, **kwargs: (2, True),
    )
    monkeypatch.setattr(
        "money_metrics.ui.main_window.QFileDialog.getSaveFileName",
        lambda *args, **kwargs: ("", ""),
    )
    window = MainWindow()
    window._add_401k_dialog()
    assert not window.centralWidget().findChildren(QPushButton)
    assert window.graph_screens and window.graph_screens[0].view_mode == "table"
