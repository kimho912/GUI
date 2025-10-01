import sys
import time
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget
from PyQt6.QtCore import QThread, pyqtSignal


# Worker thread
class Worker(QThread):
    progress = pyqtSignal(int)   # custom signal to send progress updates

    def run(self):
        for i in range(1, 6):   # simulate long task
            time.sleep(1)       # pretend this takes time
            self.progress.emit(i)  # send progress back


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("QThread Example")

        self.label = QLabel("Progress: 0")
        self.button = QPushButton("Start Task")
        self.button.clicked.connect(self.start_task)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def start_task(self):
        self.worker = Worker()             # create worker
        self.worker.progress.connect(self.update_label)  # connect signal
        self.worker.start()                # run in background

    def update_label(self, value):
        self.label.setText(f"Progress: {value}")


app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
