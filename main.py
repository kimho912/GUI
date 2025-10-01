"""
Basic PyQt6 Application with Threading and Multiple Layouts

This application demonstrates:
- Multiple layout types (QVBoxLayout, QHBoxLayout, QGridLayout)
- Threading for background tasks
- Interactive GUI elements
"""

import sys
import time
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QGridLayout, QPushButton, QLabel, QProgressBar, QTextEdit, QLineEdit
)
from PyQt6.QtCore import QThread, pyqtSignal, Qt


class WorkerThread(QThread):
    """
    Worker thread for performing background tasks.
    Emits signals to update the main GUI without blocking it.
    """
    # Define signals
    progress = pyqtSignal(int)
    finished = pyqtSignal(str)
    status = pyqtSignal(str)
    
    def __init__(self, task_name="Task"):
        super().__init__()
        self.task_name = task_name
        self.is_running = True
    
    def run(self):
        """Execute the background task."""
        self.status.emit(f"Starting {self.task_name}...")
        
        # Simulate a long-running task
        for i in range(101):
            if not self.is_running:
                self.status.emit(f"{self.task_name} cancelled")
                return
            
            time.sleep(0.05)  # Simulate work
            self.progress.emit(i)
            self.status.emit(f"{self.task_name} progress: {i}%")
        
        self.finished.emit(f"{self.task_name} completed successfully!")
    
    def stop(self):
        """Stop the thread gracefully."""
        self.is_running = False


class MainWindow(QMainWindow):
    """
    Main application window demonstrating multiple layouts and threading.
    """
    
    def __init__(self):
        super().__init__()
        self.worker_thread = None
        self.init_ui()
    
    def init_ui(self):
        """Initialize the user interface."""
        self.setWindowTitle("PyQt6 Multi-Layout Threading App")
        self.setGeometry(100, 100, 800, 600)
        
        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # Add title
        title = QLabel("PyQt6 Application with Threading and Multiple Layouts")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 18px; font-weight: bold; padding: 10px;")
        main_layout.addWidget(title)
        
        # Add horizontal layout section
        main_layout.addWidget(self.create_horizontal_section())
        
        # Add grid layout section
        main_layout.addWidget(self.create_grid_section())
        
        # Add threading control section
        main_layout.addWidget(self.create_threading_section())
        
        # Add status section
        main_layout.addWidget(self.create_status_section())
    
    def create_horizontal_section(self):
        """Create a section with horizontal layout."""
        widget = QWidget()
        widget.setStyleSheet("background-color: #f0f0f0; padding: 10px; border-radius: 5px;")
        layout = QHBoxLayout(widget)
        
        # Add label
        label = QLabel("Horizontal Layout:")
        label.setStyleSheet("font-weight: bold;")
        layout.addWidget(label)
        
        # Add buttons
        for i in range(1, 4):
            btn = QPushButton(f"Button {i}")
            btn.clicked.connect(lambda checked, x=i: self.log_message(f"Horizontal Button {x} clicked"))
            layout.addWidget(btn)
        
        return widget
    
    def create_grid_section(self):
        """Create a section with grid layout."""
        widget = QWidget()
        widget.setStyleSheet("background-color: #e0e0e0; padding: 10px; border-radius: 5px;")
        layout = QVBoxLayout(widget)
        
        # Add title
        title = QLabel("Grid Layout:")
        title.setStyleSheet("font-weight: bold;")
        layout.addWidget(title)
        
        # Create grid
        grid_widget = QWidget()
        grid_layout = QGridLayout(grid_widget)
        
        # Add input field
        grid_layout.addWidget(QLabel("Input:"), 0, 0)
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Enter text here...")
        grid_layout.addWidget(self.input_field, 0, 1, 1, 2)
        
        # Add buttons in grid
        positions = [(1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)]
        for idx, (row, col) in enumerate(positions, 1):
            btn = QPushButton(f"Grid {idx}")
            btn.clicked.connect(lambda checked, x=idx: self.log_message(f"Grid Button {x} clicked"))
            grid_layout.addWidget(btn, row, col)
        
        layout.addWidget(grid_widget)
        return widget
    
    def create_threading_section(self):
        """Create a section for threading controls."""
        widget = QWidget()
        widget.setStyleSheet("background-color: #d0d0d0; padding: 10px; border-radius: 5px;")
        layout = QVBoxLayout(widget)
        
        # Add title
        title = QLabel("Threading Controls:")
        title.setStyleSheet("font-weight: bold;")
        layout.addWidget(title)
        
        # Create horizontal layout for buttons
        button_layout = QHBoxLayout()
        
        # Start button
        self.start_btn = QPushButton("Start Background Task")
        self.start_btn.clicked.connect(self.start_task)
        button_layout.addWidget(self.start_btn)
        
        # Stop button
        self.stop_btn = QPushButton("Stop Task")
        self.stop_btn.clicked.connect(self.stop_task)
        self.stop_btn.setEnabled(False)
        button_layout.addWidget(self.stop_btn)
        
        layout.addLayout(button_layout)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)
        layout.addWidget(self.progress_bar)
        
        return widget
    
    def create_status_section(self):
        """Create a section for status messages."""
        widget = QWidget()
        widget.setStyleSheet("background-color: #c0c0c0; padding: 10px; border-radius: 5px;")
        layout = QVBoxLayout(widget)
        
        # Add title
        title = QLabel("Status Log:")
        title.setStyleSheet("font-weight: bold;")
        layout.addWidget(title)
        
        # Text area for logs
        self.status_text = QTextEdit()
        self.status_text.setReadOnly(True)
        self.status_text.setMaximumHeight(150)
        layout.addWidget(self.status_text)
        
        return widget
    
    def start_task(self):
        """Start a background task in a separate thread."""
        if self.worker_thread is not None and self.worker_thread.isRunning():
            self.log_message("Task is already running!")
            return
        
        # Get task name from input field
        task_name = self.input_field.text() or "Background Task"
        
        # Create and configure worker thread
        self.worker_thread = WorkerThread(task_name)
        self.worker_thread.progress.connect(self.update_progress)
        self.worker_thread.status.connect(self.log_message)
        self.worker_thread.finished.connect(self.task_finished)
        
        # Update UI
        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        self.progress_bar.setValue(0)
        
        # Start thread
        self.worker_thread.start()
        self.log_message(f"Started thread for: {task_name}")
    
    def stop_task(self):
        """Stop the running background task."""
        if self.worker_thread is not None and self.worker_thread.isRunning():
            self.worker_thread.stop()
            self.log_message("Stopping task...")
            self.stop_btn.setEnabled(False)
    
    def update_progress(self, value):
        """Update the progress bar."""
        self.progress_bar.setValue(value)
    
    def task_finished(self, message):
        """Handle task completion."""
        self.log_message(message)
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
    
    def log_message(self, message):
        """Add a message to the status log."""
        self.status_text.append(f"[{time.strftime('%H:%M:%S')}] {message}")
    
    def closeEvent(self, event):
        """Handle window close event."""
        # Stop any running threads
        if self.worker_thread is not None and self.worker_thread.isRunning():
            self.worker_thread.stop()
            self.worker_thread.wait()
        event.accept()


def main():
    """Main entry point for the application."""
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
