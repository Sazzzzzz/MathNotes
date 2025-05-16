from __future__ import annotations
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

stylesheet = """
    QPushButton {
        background: #222;
    }
    QPushButton:checked {
        background: yellow;
    }
    QPushButton:disabled {
        background: #555;
    }
"""


class Light(QPushButton):

    def __init__(
        self,
        row: int,
        col: int,
        parent=None,
    ):
        super().__init__(parent)
        self.row = row
        self.col = col
        self.setCheckable(True)
        # No need to set stylesheet here
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

    @property
    def position(self):
        return Point(self.row, self.col)

    # INFO: Button status will be controlled entirely by `setChecked`, `setEnabled`, `setHovered`
    def setHovered(self):
        pass


class LightsOutWidget(QTableWidget):
    def __init__(self, parent=None):
        self.grid: np.ndarray = np.array([[1, 1, 1], [1, 1, 1], [1, 1, 0]], dtype=bool)
        self.canvas: list[Point] = [Point(0, 0)]
        self.is_idle = False
        self.solver = Solver(self.grid)
        super().__init__(parent)
        self.draw_ui()

    def draw_ui(self):
        self.setRowCount(self.grid.shape[0])
        self.setColumnCount(self.grid.shape[1])
        self.horizontalHeader().hide()
        self.verticalHeader().hide()
        self.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        # TODO: Sweep to turn on and off
        self.setSelectionMode(QTableWidget.SelectionMode.NoSelection)
        for r in range(self.rowCount()):
            for c in range(self.columnCount()):
                btn = Light(r, c)
                btn.clicked.connect(self.toggle_handler)
                self.setCellWidget(r, c, btn)
                if not self.grid[r][c]:
                    btn.setEnabled(False)
                if Point(r, c) in self.canvas:
                    btn.setChecked(True)

        # Make all cells square and expanding
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.update_square_cells()

    def toggle_handler(self):
        assert isinstance(btn := self.sender(), Light)
        if self.is_idle:
            return None
        # Change the state of the buttons around the clicked button
        print("This is button with coordinates: ", btn.row, btn.col)

    # Resize logic
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
    app.setStyleSheet(stylesheet)  # Apply stylesheet to the entire application
    window = MainWindow()
    window.show()

    app.exec()
