import sys
import numpy as np
from PySide6.QtWidgets import (
    QApplication,
    QFrame,
    QMainWindow,
    QWidget,
    QPushButton,
    QGridLayout,
    QTableWidget,
    QHeaderView,
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter, QColor
from solver import Point, Solver

# reference: https://doc.qt.io/qtforpython-6/PySide6/QtWidgets/QTableWidget.html#more
# reference: https://doc.qt.io/qtforpython-6/PySide6/QtWidgets/QTableWidget.html#more
# reference: https://doc.qt.io/qtforpython-6/PySide6/QtWidgets/QTableView.html#more


class LightGrid(QTableWidget):
    def __init__(self, rows: int, cols: int):
        super().__init__(rows, cols)
        self.rows = rows
        self.cols = cols

        # Game board
        self.board_widget = QTableWidget()
        self.board_widget.setRowCount(self.rows)
        self.board_widget.setColumnCount(self.cols)
        self.board_widget.setStyleSheet(
            """
            QTableView::item { 
                border-radius: 0px;
                border: 1px solid #808080;
            }
        """
        )

        # Reduce spacing between cells
        self.setHorizontalScrollMode(QTableWidget.ScrollMode.ScrollPerPixel)
        self.setVerticalScrollMode(QTableWidget.ScrollMode.ScrollPerPixel)
        self.horizontalHeader().setMinimumSectionSize(20)  # Smaller minimum size
        self.verticalHeader().setMinimumSectionSize(20)  # Smaller minimum size

        self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        # self.horizontalHeader().hide()
        # self.verticalHeader().hide()
        self.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.cellClicked.connect(self.handle_left_click)
        # Right-click handler
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.handle_right_click)

    def handle_left_click(self, row: int, col: int):
        pass

    def handle_right_click(self, pos):
        pass


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Lights Out Solver")
        self.setGeometry(100, 100, 400, 400)

        # for testing purposes
        self.setCentralWidget(LightGrid(5, 5))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    app.exec()
