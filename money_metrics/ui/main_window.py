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
    QFileDialog,
    QInputDialog,
    QMessageBox,
)
from PySide6.QtGui import QAction
from PySide6.QtCore import Qt

from money_metrics.core.data_manager import DataManager
from money_metrics.core.profile import AppProfile
from money_metrics.core.four_zero_one_k import FourZeroOneK
from .graph_screen import GraphScreen

class MainWindow(QMainWindow):
    def __init__(self, profile: AppProfile | None = None):
        super().__init__()
        self.setWindowTitle("MoneyMetrics")
        self.setGeometry(100, 100, 800, 600)

        # Data manager keeps datasets separate from the UI widgets
        self.data_manager = DataManager()

        # Placeholder central widget
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)
        layout.addWidget(QLabel("Welcome to MoneyMetrics!"))
        self.setCentralWidget(central_widget)

        # Keep track of graph screens
        self.graph_screens: list[GraphScreen] = []

        # Track profile path
        self.profile_path: str | None = None

        # Menu setup
        menu_bar = QMenuBar(self)
        self.setMenuBar(menu_bar)
        graphs_menu = menu_bar.addMenu("Graphs")
        add_graph_action = QAction("Add Graph", self)
        add_graph_action.triggered.connect(self.add_graph_screen)
        graphs_menu.addAction(add_graph_action)

        # Finance menu
        finance_menu = menu_bar.addMenu("Finance")
        add_401k_action = QAction("Add 401(k)", self)
        add_401k_action.triggered.connect(self._add_401k_dialog)
        finance_menu.addAction(add_401k_action)

        # Profile menu
        profile_menu = menu_bar.addMenu("Profile")
        load_action = QAction("Load Profile...", self)
        load_action.triggered.connect(self._load_profile_dialog)
        save_action = QAction("Save Profile", self)
        save_action.triggered.connect(self._save_profile)
        save_as_action = QAction("Save Profile As...", self)
        save_as_action.triggered.connect(self._save_profile_as)
        profile_menu.addAction(load_action)
        profile_menu.addAction(save_action)
        profile_menu.addAction(save_as_action)

        if profile is not None:
            self._apply_profile(profile)
        else:
            # Example dataset for demonstration purposes
            # `replace=True` ensures re-running won't raise if the dataset exists
            self.data_manager.add_dataset("Sample", [1, 2, 3, 4], replace=True)

    # ------------------------------------------------------------------
    def add_graph_screen(self):
        """Create and show a new graph screen."""
        graph = GraphScreen(self.data_manager, self)
        graph.destroyed.connect(self._remove_graph_screen)
        self.addDockWidget(Qt.RightDockWidgetArea, graph)
        self.graph_screens.append(graph)

    def _remove_graph_screen(self, screen):
        """Remove a graph screen once it has been destroyed."""
        if screen in self.graph_screens:
            self.graph_screens.remove(screen)

    # ------------------------------------------------------------------
    def _add_401k_dialog(self) -> None:
        """Prompt for 401(k) details and store the dataset."""
        contribution, ok = QInputDialog.getDouble(
            self,
            "401(k)",
            "Monthly contribution:",
            0.0,
            0.0,
            1_000_000.0,
            2,
        )
        if not ok:
            return
        growth, ok = QInputDialog.getDouble(
            self,
            "401(k)",
            "Monthly growth rate (e.g. 0.01 for 1%):",
            0.0,
            -1.0,
            1.0,
            4,
        )
        if not ok:
            return
        months, ok = QInputDialog.getInt(
            self,
            "401(k)",
            "Number of months:",
            12,
            1,
            600,
        )
        if not ok:
            return
        plan = FourZeroOneK()
        for _ in range(months):
            plan.add_month(contribution, growth)
        self.data_manager.add_dataset("401(k)", plan.to_dict(), replace=True)
        QMessageBox.information(self, "401(k)", "401(k) dataset added.")

    # ------------------------------------------------------------------
    def _apply_profile(self, profile: AppProfile) -> None:
        """Load datasets and graph screens from a profile."""
        self.data_manager = DataManager()
        for name, data in profile.datasets.items():
            self.data_manager.add_dataset(name, data, replace=True)

        # Remove existing screens
        for screen in list(self.graph_screens):
            screen.deleteLater()
        self.graph_screens.clear()

        for info in profile.screens:
            graph = GraphScreen(self.data_manager, self, title=info.get("title"))
            dataset_name = info.get("dataset")
            if dataset_name:
                data = self.data_manager.get_dataset(dataset_name)
                if data is not None:
                    graph.set_data(data, dataset_name)
            graph.destroyed.connect(self._remove_graph_screen)
            self.addDockWidget(Qt.RightDockWidgetArea, graph)
            self.graph_screens.append(graph)

    def _save_profile(self) -> None:
        if self.profile_path is None:
            self._save_profile_as()
            return
        profile = AppProfile.from_window(self)
        profile.save_to_file(self.profile_path)

    def _save_profile_as(self) -> None:
        path, _ = QFileDialog.getSaveFileName(
            self, "Save Profile", filter="MoneyMetrics Profile (*.json)"
        )
        if path:
            self.profile_path = path
            self._save_profile()

    def _load_profile_dialog(self) -> None:
        path, _ = QFileDialog.getOpenFileName(
            self, "Load Profile", filter="MoneyMetrics Profile (*.json)"
        )
        if path:
            profile = AppProfile.load_from_file(path)
            self.profile_path = path
            self._apply_profile(profile)
