from ast import Name
from dataclasses import dataclass, field
import sys
from types import SimpleNamespace
from typing import NamedTuple, OrderedDict
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


class DefaultConfig(NamedTuple):
    row: int
    col: int
    is_idle: bool
    canvas: OrderedDict[Point, bool]


default_state = DefaultConfig(
    row=3,
    col=3,
    is_idle=False,
    canvas=OrderedDict(
        {
            # Point(0, 0): False,
            Point(0, 1): False,
            Point(0, 2): False,
            Point(1, 0): False,
            Point(1, 1): False,
            Point(1, 2): False,
            Point(2, 0): False,
            Point(2, 1): False,
            Point(2, 2): True,
        }
    ),
)


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
    def __init__(self, parent=None) -> None:
        self._canvas: OrderedDict[Point, bool] = default_state.canvas
        self.solver = Solver(self.canvas.keys())
        self.is_idle: bool = default_state.is_idle
        # Avoid conflict with row/col method
        self.rows = default_state.row
        self.cols = default_state.col

        super().__init__(parent)
        self.draw_ui()

    @property
    def canvas(self) -> OrderedDict[Point, bool]:
        return self._canvas

    @canvas.setter
    def canvas(self, value: OrderedDict[Point, bool]) -> None:
        self._canvas = value
        self.solver.background = self._canvas.keys()
        print(f"Set canvas to {value}")

    def draw_ui(self):
        self.setRowCount(self.rows)
        self.setColumnCount(self.cols)
        self.horizontalHeader().hide()
        self.verticalHeader().hide()
        self.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        # TODO: Sweep to turn on and off
        self.setSelectionMode(QTableWidget.SelectionMode.NoSelection)
        for r in range(self.rows):
            for c in range(self.cols):
                btn = Light(r, c, self)
                btn.clicked.connect(self.toggle_handler)
                self.setCellWidget(r, c, btn)
                if Point(r, c) in self.canvas:
                    btn.setEnabled(True)
                    if self.canvas[Point(r, c)]:
                        btn.setChecked(True)
                else:
                    btn.setEnabled(False)

        # Make all cells square and expanding
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.update_square_cells()

    def _nearby_lights_on_canvas(self, point: Point) -> list[Point]:
        """Get the points around the clicked point"""
        l = [
            Point(point.x - 1, point.y),
            Point(point.x + 1, point.y),
            Point(point.x, point.y - 1),
            Point(point.x, point.y + 1),
        ]
        return [point for point in l if point in self.canvas.keys()]

    def _get_light(self, point: Point) -> Light:
        return self.cellWidget(point.x, point.y)  # type: ignore

    def toggle_handler(self):
        assert isinstance(btn := self.sender(), Light)
        if self.is_idle:
            self.canvas[btn.position] = btn.isChecked()
            return None
        # Change the state of the buttons around the clicked button
        nearby_lights = self._nearby_lights_on_canvas(btn.position)
        for point in nearby_lights:
            if point in self.canvas:
                near_btn = self._get_light(point)
                near_btn.setChecked(not near_btn.isChecked())
                self.canvas[point] = not self.canvas[point]
        return None

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
