from PySide6.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MoneyMetrics")
        self.setGeometry(100, 100, 800, 600)  # Set window size

        # Create a simple UI layout
        layout = QVBoxLayout()
        label = QLabel("Welcome to MoneyMetrics!")
        layout.addWidget(label)

        # Set central widget
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
