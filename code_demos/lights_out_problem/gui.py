import sys
import numpy as np
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QPushButton,
    QTableWidget,
    QSizePolicy,
)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QPainter, QColor
from solver import Point, Solver


class Button(QPushButton):
    def __init__(self, row: int, col: int, parent=None):
        super().__init__(parent)
        self.row = row
        self.col = col
        self.setCheckable(True)
        self.setStyleSheet("background: #222;")
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

    def paintEvent(self, event):
        super().paintEvent(event)
        if self.isChecked():
            painter = QPainter(self)
            painter.setBrush(QColor(255, 255, 0))
            painter.drawRect(self.rect())

    # TODO: Button in total has 4 states: Disabled, Checked, Unchecked, Hovered
    # TODO: Use property and these states to avoid using paintEvent

    @property
    def position(self):
        return Point(self.row, self.col)


class LightsOutWidget(QTableWidget):
    def __init__(self, parent=None):
        super().__init__(3, 3, parent)
        self.grid: np.ndarray = np.array([[1, 1, 1], [1, 1, 1], [1, 1, 0]], dtype=bool)
        self.canvas: list[Point] = [Point(0, 0)]
        self.is_idle = False
        self.solver = Solver(self.grid)
        self.draw_ui()

    def draw_ui(self):
        self.horizontalHeader().hide()
        self.verticalHeader().hide()
        self.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        # TODO: Sweep to turn on and off
        self.setSelectionMode(QTableWidget.SelectionMode.NoSelection)
        for r in range(self.rowCount()):
            for c in range(self.columnCount()):
                btn = Button(r, c)
                btn.clicked.connect(self.toggle_handler)
                self.setCellWidget(r, c, btn)
                if not self.grid[r][c]:
                    btn.setEnabled(False)
                    btn.setStyleSheet("background: gray;")

        # Make all cells square and expanding
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.update_square_cells()

    def toggle_handler(self):
        assert isinstance(btn := self.sender(), Button)
        if btn.isChecked():
            btn.setStyleSheet("background: yellow;")
        else:
            btn.setStyleSheet("background: #222;")
        print("This is button with coordinates: ", btn.row, btn.col)

    # This may be eventually replaced with size change in the main window
    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.update_square_cells()

    def update_square_cells(self):
        # Make all cells square and fill the widget
        w = self.viewport().width()
        h = self.viewport().height()
        rows = self.rowCount()
        cols = self.columnCount()
        if rows == 0 or cols == 0:
            return None
        cell_size = min(w // cols, h // rows)
        for i in range(rows):
            self.setRowHeight(i, cell_size)
        for i in range(cols):
            self.setColumnWidth(i, cell_size)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Lights Out Solver")
        self.setGeometry(100, 100, 400, 400)

        # for testing purposes
        self.setCentralWidget(LightsOutWidget())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    app.exec()
