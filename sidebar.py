from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QTextEdit,
    QDockWidget, QPushButton, QTreeWidget, QTreeWidgetItem
)
from PyQt6.QtCore import Qt, QPropertyAnimation


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Sidebar Animation Example")

        # Central widget
        self.editor = QTextEdit("Main editor area")
        self.setCentralWidget(self.editor)

        # Sidebar (dock) with a tree widget
        self.sidebar = QDockWidget("Sidebar", self)
        self.sidebar.setAllowedAreas(Qt.DockWidgetArea.LeftDockWidgetArea)

        tree = QTreeWidget()
        tree.setHeaderHidden(True)

        # Example tree items
        parent1 = QTreeWidgetItem(["Parent 1"])
        parent1.addChildren([QTreeWidgetItem(["Child 1.1"]),
                             QTreeWidgetItem(["Child 1.2"])])
        parent2 = QTreeWidgetItem(["Parent 2"])
        parent2.addChild(QTreeWidgetItem(["Child 2.1"]))

        tree.addTopLevelItems([parent1, parent2])

        self.sidebar.setWidget(tree)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.sidebar)

        # Toggle button
        toggle_btn = QPushButton("Toggle Sidebar")
        toggle_btn.clicked.connect(self.toggle_sidebar)
        self.editor.setCornerWidget(toggle_btn)

        # State
        self.sidebar_expanded = True
        self.sidebar_width = 200  # default width

    def toggle_sidebar(self):
        animation = QPropertyAnimation(self.sidebar, b"maximumWidth")
        animation.setDuration(300)  # ms
        if self.sidebar_expanded:
            animation.setStartValue(self.sidebar.width())
            animation.setEndValue(0)
        else:
            animation.setStartValue(self.sidebar.width())
            animation.setEndValue(self.sidebar_width)
        animation.start()

        self.sidebar_expanded = not self.sidebar_expanded


app = QApplication([])
w = MainWindow()
w.resize(600, 400)
w.show()
app.exec()
