"""
Example: Using the WorkerThread independently

This example shows how to use the WorkerThread class
for background tasks in other PyQt6 applications.
"""

import sys
import time
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel
from PyQt6.QtCore import QThread, pyqtSignal


class SimpleWorker(QThread):
    """Simple worker thread that counts to 10."""
    update = pyqtSignal(str)
    
    def run(self):
        for i in range(1, 11):
            time.sleep(0.5)
            self.update.emit(f"Count: {i}")


class SimpleWindow(QMainWindow):
    """Minimal example window."""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Simple Threading Example")
        
        widget = QWidget()
        layout = QVBoxLayout(widget)
        self.setCentralWidget(widget)
        
        self.label = QLabel("Click button to start")
        layout.addWidget(self.label)
        
        btn = QPushButton("Start Counting")
        btn.clicked.connect(self.start_worker)
        layout.addWidget(btn)
    
    def start_worker(self):
        """Start the worker thread."""
        worker = SimpleWorker()
        worker.update.connect(self.label.setText)
        worker.finished.connect(lambda: self.label.setText("Finished!"))
        worker.start()
        
        # Keep reference to prevent garbage collection
        self.worker = worker


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SimpleWindow()
    window.show()
    sys.exit(app.exec())
