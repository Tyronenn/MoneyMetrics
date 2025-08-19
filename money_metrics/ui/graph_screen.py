from PySide6.QtWidgets import (
    QDockWidget,
    QWidget,
    QVBoxLayout,
    QLabel,
    QMenu,
    QInputDialog,
    QMessageBox,
    QTableWidget,
    QTableWidgetItem,
)
from PySide6.QtCore import Qt

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class GraphScreen(QDockWidget):
    """A dockable widget representing a graph screen.

    The screen does not automatically load any data. Data can be assigned
    later via :meth:`set_data`. The widget can be renamed, detached/attached
    and closed through a context menu.
    """

    _counter = 1

    def __init__(self, data_manager, parent=None, title=None):
        if title is None:
            title = f"Graph {GraphScreen._counter}"
            GraphScreen._counter += 1
        super().__init__(title, parent)
        self.data_manager = data_manager
        self.data = None
        self.dataset_name = None
        # Track which parameters from the dataset are currently graphed
        self._parameters: list[str] = []

        content = QWidget(self)
        self._layout = QVBoxLayout(content)
        self.label = QLabel("No data", content)
        self.label.setAlignment(Qt.AlignCenter)
        self.table = QTableWidget(content)
        self.canvas = FigureCanvas(Figure(figsize=(5, 3)))
        self.view_mode = "graph"

        self._layout.addWidget(self.label)
        self._current_widget = self.label
        self.setWidget(content)

    # ------------------------ Data handling -------------------------
    def set_data(self, data, name=None):
        """Assign data to the graph screen.

        Parameters
        ----------
        data: Any
            Data to be visualised. For this stub implementation the data is
            simply converted to a string and displayed in the label.
        name: str, optional
            Name of the dataset, stored so the screen can be recreated when a
            profile is loaded.
        """
        self.data = data
        self.dataset_name = name

        if isinstance(data, list) and data and isinstance(data[0], dict):
            # When new tabular data is assigned default to graphing the
            # calculated balance if present. The user can add/remove
            # additional parameters via the context menu.
            self._parameters = []
            if "balance" in data[0]:
                self._parameters.append("balance")
            self._update_table(data)
            self._update_graph(data)
            widget = self.canvas if self.view_mode == "graph" else self.table
            self._set_widget(widget)
        else:
            text = "No data" if data is None else str(data)
            self.label.setText(text)
            self._set_widget(self.label)

    # ------------------------ UI actions ---------------------------
    def contextMenuEvent(self, event):
        menu = QMenu(self)
        rename_action = menu.addAction("Rename")
        data_action = menu.addAction("Set Data")
        add_param = remove_param = toggle_action = None
        if isinstance(self.data, list) and self.data and isinstance(self.data[0], dict):
            add_param = menu.addAction("Add Parameter")
            remove_param = menu.addAction("Remove Parameter")
            toggle_action = menu.addAction(
                "Show Table" if self.view_mode == "graph" else "Show Graph"
            )
        detach_action = menu.addAction(
            "Detach" if not self.isFloating() else "Attach"
        )
        close_action = menu.addAction("Close")
        action = menu.exec(event.globalPos())
        if action == rename_action:
            self._rename()
        elif action == data_action:
            self._prompt_for_data()
        elif add_param and action == add_param:
            self._add_parameter()
        elif remove_param and action == remove_param:
            self._remove_parameter()
        elif toggle_action and action == toggle_action:
            self._toggle_view()
        elif action == detach_action:
            self.setFloating(not self.isFloating())
        elif action == close_action:
            self.close()

    def _rename(self):
        text, ok = QInputDialog.getText(self, "Rename Graph", "Graph name:", text=self.windowTitle())
        if ok and text:
            self.setWindowTitle(text)

    def _prompt_for_data(self):
        name, ok = QInputDialog.getText(self, "Set Data", "Dataset name:")
        if not ok or not name:
            return
        data = self.data_manager.get_dataset(name)
        if data is None:
            QMessageBox.warning(self, "Data not found", f"Dataset '{name}' not found.")
            return
        self.set_data(data, name)

    # ------------------------ Helpers ---------------------------
    def _set_widget(self, widget: QWidget) -> None:
        if widget is self._current_widget:
            return
        self._layout.removeWidget(self._current_widget)
        self._current_widget.setParent(None)
        self._layout.addWidget(widget)
        self._current_widget = widget

    def _update_table(self, data):
        keys = list(data[0].keys())
        self.table.setColumnCount(len(keys))
        self.table.setHorizontalHeaderLabels(keys)
        self.table.setRowCount(len(data))
        for row, entry in enumerate(data):
            for col, key in enumerate(keys):
                item = QTableWidgetItem(str(entry.get(key, "")))
                self.table.setItem(row, col, item)

    def _update_graph(self, data):
        """Render the selected parameters against months."""

        ax = self.canvas.figure.subplots()
        ax.clear()
        if not (isinstance(data, list) and data and isinstance(data[0], dict)):
            self.canvas.draw_idle()
            return

        months = [d.get("month", i + 1) for i, d in enumerate(data)]
        for param in self._parameters:
            values = [d.get(param, 0) for d in data]
            ax.plot(months, values, marker="o", label=param)
        ax.set_xlabel("Month")
        ax.set_ylabel("Value")
        if self._parameters:
            ax.legend()
        self.canvas.draw_idle()

    def _toggle_view(self):
        self.view_mode = "table" if self.view_mode == "graph" else "graph"
        widget = self.canvas if self.view_mode == "graph" else self.table
        self._set_widget(widget)

    # --------------------- Parameter management ---------------------
    def _available_parameters(self) -> list[str]:
        if not (isinstance(self.data, list) and self.data and isinstance(self.data[0], dict)):
            return []
        keys = list(self.data[0].keys())
        if "month" in keys:
            keys.remove("month")
        return [k for k in keys if k not in self._parameters]

    def _add_parameter(self) -> None:
        options = self._available_parameters()
        if not options:
            QMessageBox.information(self, "Add Parameter", "No additional parameters available.")
            return
        param, ok = QInputDialog.getItem(
            self, "Add Parameter", "Parameter:", options, 0, False
        )
        if ok and param:
            self._parameters.append(param)
            self._update_graph(self.data)

    def _remove_parameter(self) -> None:
        if not self._parameters:
            QMessageBox.information(self, "Remove Parameter", "No parameters to remove.")
            return
        param, ok = QInputDialog.getItem(
            self, "Remove Parameter", "Parameter:", self._parameters, 0, False
        )
        if ok and param in self._parameters:
            self._parameters.remove(param)
            self._update_graph(self.data)
