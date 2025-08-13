"""Main application window.

The window hosts the central dashboard and allows the user to create and
manage multiple graph screens. Each graph screen is implemented as a dockable
widget that can be freely rearranged, resized or detached. Graph screens are
kept separate from the underlying data and the user may choose which datasets
to display on a particular screen.
"""

from PySide6.QtWidgets import (
    QMainWindow,
    QLabel,
    QVBoxLayout,
    QWidget,
    QMenuBar,
    QAction,
)
from PySide6.QtCore import Qt

from core.data_manager import DataManager
from .graph_screen import GraphScreen

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MoneyMetrics")
        self.setGeometry(100, 100, 800, 600)

        # Data manager keeps datasets separate from the UI widgets
        self.data_manager = DataManager()
        # Example dataset for demonstration purposes
        self.data_manager.add_dataset("Sample", [1, 2, 3, 4])

        # Placeholder central widget
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)
        layout.addWidget(QLabel("Welcome to MoneyMetrics!"))
        self.setCentralWidget(central_widget)

        # Keep track of graph screens
        self.graph_screens = []

        # Menu setup
        menu_bar = QMenuBar(self)
        self.setMenuBar(menu_bar)
        graphs_menu = menu_bar.addMenu("Graphs")
        add_graph_action = QAction("Add Graph", self)
        add_graph_action.triggered.connect(self.add_graph_screen)
        graphs_menu.addAction(add_graph_action)

    # ------------------------------------------------------------------
    def add_graph_screen(self):
        """Create and show a new graph screen."""
        graph = GraphScreen(self.data_manager, self)
        self.addDockWidget(Qt.RightDockWidgetArea, graph)
        self.graph_screens.append(graph)
