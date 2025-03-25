import sys
from PyQt6.QtWidgets import QApplication, QLabel, QMainWindow
from PyQt6.QtCore import Qt  # Import Qt from PyQt6.QtCore

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyQt6 Minimal Example")
        label = QLabel("Hello, PyQt6!")
        #label.setAlignment(Qt.AlignCenter)  # Use Qt from the import above
        self.setCentralWidget(label)

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
