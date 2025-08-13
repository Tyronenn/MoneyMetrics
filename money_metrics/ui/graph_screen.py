from PySide6.QtWidgets import QDockWidget, QWidget, QVBoxLayout, QLabel, QMenu, QInputDialog, QMessageBox
from PySide6.QtCore import Qt

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

        content = QWidget(self)
        layout = QVBoxLayout(content)
        self.label = QLabel("No data", content)
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)
        self.setWidget(content)

    # ------------------------ Data handling -------------------------
    def set_data(self, data):
        """Assign data to the graph screen.

        Parameters
        ----------
        data: Any
            Data to be visualised. For this stub implementation the data is
            simply converted to a string and displayed in the label.
        """
        self.data = data
        if data is None:
            self.label.setText("No data")
        else:
            self.label.setText(str(data))

    # ------------------------ UI actions ---------------------------
    def contextMenuEvent(self, event):
        menu = QMenu(self)
        rename_action = menu.addAction("Rename")
        data_action = menu.addAction("Set Data")
        detach_action = menu.addAction("Detach" if not self.isFloating() else "Attach")
        close_action = menu.addAction("Close")
        action = menu.exec(event.globalPos())
        if action == rename_action:
            self._rename()
        elif action == data_action:
            self._prompt_for_data()
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
        self.set_data(data)
