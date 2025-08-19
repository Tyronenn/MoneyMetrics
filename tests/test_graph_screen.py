import pytest

pytest.importorskip("PySide6.QtWidgets")
from PySide6.QtWidgets import QApplication

from money_metrics.ui.graph_screen import GraphScreen
from money_metrics.core.data_manager import DataManager


@pytest.fixture(scope="module")
def app():
    try:
        app = QApplication.instance() or QApplication([])
    except Exception:
        pytest.skip("Qt GUI not available")
    yield app


def sample_dataset():
    return [
        {"month": 1, "contribution": 100.0, "growth_rate": 0.01, "balance": 101.0},
        {"month": 2, "contribution": 100.0, "growth_rate": 0.01, "balance": 202.01},
    ]


def test_add_and_remove_parameters(app):
    screen = GraphScreen(DataManager())
    data = sample_dataset()
    screen.set_data(data, name="401(k)")

    # Balance graphed by default
    assert screen._parameters == ["balance"]

    # Add contribution line
    screen._parameters.append("contribution")
    screen._update_graph(data)
    labels = [line.get_label() for line in screen.canvas.figure.axes[0].get_lines()]
    assert "balance" in labels and "contribution" in labels

    # Remove balance line
    screen._parameters.remove("balance")
    screen._update_graph(data)
    labels = [line.get_label() for line in screen.canvas.figure.axes[0].get_lines()]
    assert "balance" not in labels and "contribution" in labels
