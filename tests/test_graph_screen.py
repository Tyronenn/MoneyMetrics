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


def test_update_graph_reuses_axes(app):
    screen = GraphScreen(DataManager())
    data = sample_dataset()
    screen.set_data(data, name="401(k)")
    initial_axes = len(screen.canvas.figure.axes)
    # Repeated updates should not create additional axes
    screen._update_graph(data)
    screen._update_graph(data)
    assert len(screen.canvas.figure.axes) == initial_axes


def _col_index(table, name):
    for i in range(table.columnCount()):
        if table.horizontalHeaderItem(i).text() == name:
            return i
    raise ValueError(name)


def test_edit_and_rename_column_updates_dataset(app):
    dm = DataManager()
    screen = GraphScreen(dm)
    data = sample_dataset()
    screen.set_data(data, name="401(k)")

    # Edit contribution of first row
    c_idx = _col_index(screen.table, "contribution")
    item = screen.table.item(0, c_idx)
    item.setText("200")
    assert screen.data[0]["contribution"] == 200.0
    # balance should be recomputed
    assert screen.data[0]["balance"] == pytest.approx((0 + 200) * 1.01)
    assert dm.get_dataset("401(k)")[0]["contribution"] == 200.0

    # Rename column and ensure parameters update
    screen.handle_dropped_parameter("contribution")
    screen.rename_column(c_idx, "deposit")
    assert "deposit" in screen.data[0]
    assert "contribution" not in screen.data[0]
    assert "deposit" in screen._parameters and "contribution" not in screen._parameters


def test_drag_drop_toggle_parameter(app):
    screen = GraphScreen(DataManager())
    data = sample_dataset()
    screen.set_data(data, name="401(k)")
    screen.handle_dropped_parameter("contribution")
    assert "contribution" in screen._parameters
    screen.handle_dropped_parameter("contribution")
    assert "contribution" not in screen._parameters
