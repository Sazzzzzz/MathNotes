import sys
from typing import NamedTuple, OrderedDict, cast
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QPushButton,
    QTableWidget,
    QSizePolicy,
)
from PySide6.QtCore import Qt, QSize, QRect
from PySide6.QtGui import QPainter, QColor, QAction
from solver import Point, Solver
from pprint import pprint

stylesheet = """
    QPushButton {
        background: #222;
        border: 1px solid #444; /* Add a border for better definition */
        color: white; /* Ensure text is visible */
    }
    QPushButton:checked {
        background: yellow;
        border: 3px solid #660; /* Darker yellow border */
        color: black; /* Ensure text is visible */
    }
    QPushButton:disabled {
        background: #555;
        border: 1px solid #333; /* Darker gray border */
        color: #aaa; /* Lighter text for disabled */
    }
"""


class DefaultConfig(NamedTuple):
    row: int
    col: int
    is_idle: bool
    solution_highlight_active: bool  # Renamed from is_solution_hovered
    canvas: OrderedDict[Point, bool]


default_state = DefaultConfig(
    row=3,
    col=3,
    is_idle=False,
    solution_highlight_active=False,  # Renamed and set to False by default
    canvas=OrderedDict(
        {
            Point(0, 0): False,
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

# TODO: Why it uses a property in Qt?


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
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setProperty("solution_highlight", False)  # Initialize dynamic property

    @property
    def position(self):
        return Point(self.row, self.col)

    def setSolutionHighlight(self, highlight: bool) -> None:
        if self.property("solution_highlight") != highlight:
            self.setProperty("solution_highlight", highlight)
            self.update()  # Trigger a repaint

    def paintEvent(self, event):
        super().paintEvent(event)  # Draw the button as usual

        if self.property("solution_highlight"):
            painter = QPainter(self)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)

            # Semi-transparent red circle
            color = QColor(255, 0, 0, 128)  # Red with 50% alpha
            painter.setBrush(color)
            painter.setPen(Qt.PenStyle.NoPen)  # No outline for the circle

            # Calculate circle dimensions
            rect = self.rect()
            # Make the circle diameter 50% of the smaller dimension of the button
            diameter = min(rect.width(), rect.height()) * 0.5
            radius = diameter / 2

            # Center the circle
            center_x = rect.width() / 2
            center_y = rect.height() / 2

            # Define the bounding box for the ellipse
            circle_rect = QRect(
                int(center_x - radius),
                int(center_y - radius),
                int(diameter),
                int(diameter),
            )
            painter.drawEllipse(circle_rect)


class LightTable(QTableWidget):
    def __init__(self, parent=None) -> None:
        self._canvas: OrderedDict[Point, bool] = default_state.canvas
        self.solver = Solver(self.canvas.keys())
        self.is_idle: bool = default_state.is_idle
        self.solution_highlight_active: bool = (
            default_state.solution_highlight_active
        )  #
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
                light = Light(r, c, self)
                light.clicked.connect(self.toggle_handler)
                self.setCellWidget(r, c, light)
                if Point(r, c) in self.canvas:
                    light.setEnabled(True)
                    if self.canvas[Point(r, c)]:
                        light.setChecked(True)
                else:
                    light.setEnabled(False)

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
        assert isinstance(light := self.cellWidget(point.x, point.y), Light)
        return light

    def toggle_handler(self):
        assert isinstance(light := self.sender(), Light)
        # idle mode handler
        if self.is_idle:
            self.canvas[light.position] = light.isChecked()
            return None
        # Game mode handler
        nearby_lights = self._nearby_lights_on_canvas(light.position)
        self.canvas[light.position] = light.isChecked()
        for point in nearby_lights:
            near_light = self._get_light(point)
            near_light.setChecked(not near_light.isChecked())
            self.canvas[point] = near_light.isChecked()

        # Solution highlight handler
        if self.solution_highlight_active:
            self.show_solution_highlights()

        return None

    def solve(self):
        current = [point for point in self.canvas if self.canvas[point]]
        return self.solver.solve(current, [])

    def clear_solution_highlights(self):
        for point in self.canvas:
            light = self._get_light(point)
            light.setSolutionHighlight(False)

    def show_solution_highlights(self):
        self.clear_solution_highlights()
        if not self.solution_highlight_active:
            return None

        solution_steps = self.solve()

        for point in solution_steps:
            self._get_light(point).setSolutionHighlight(True)

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

        toolbar = self.addToolBar("Toolbar")
        toolbar.setMovable(False)
        self.main = LightTable()

        idle_mode_action = QAction("Idle Mode", self)
        idle_mode_action.setCheckable(True)
        idle_mode_action.setShortcut("i")
        idle_mode_action.triggered.connect(self.toggle_idle_mode)

        edit_mode_action = QAction("Edit Mode", self)
        edit_mode_action.setCheckable(True)
        edit_mode_action.setShortcut("e")
        edit_mode_action.triggered.connect(self.toggle_edit_mode)

        solution_highlight_action = QAction("Highlight Solution", self)  # Renamed text
        solution_highlight_action.setCheckable(True)
        solution_highlight_action.setShortcut("s")
        solution_highlight_action.setChecked(
            self.main.solution_highlight_active
        )  # Sync with initial state
        solution_highlight_action.triggered.connect(
            self.toggle_solution_highlight
        )  # Renamed method

        toolbar.addAction(idle_mode_action)
        toolbar.addAction(edit_mode_action)
        toolbar.addAction(solution_highlight_action)  # Renamed action
        # for testing purposes
        self.setCentralWidget(self.main)

    def toggle_idle_mode(self):
        action = cast(QAction, self.sender())
        self.main.is_idle = action.isChecked()
        # When exiting idle mode, if highlights are active, refresh them
        if not self.main.is_idle and self.main.solution_highlight_active:
            self.main.show_solution_highlights()

    def toggle_edit_mode(self):
        pass

    def toggle_solution_highlight(self):
        action = cast(QAction, self.sender())
        self.main.solution_highlight_active = action.isChecked()
        if self.main.solution_highlight_active:
            self.main.show_solution_highlights()
        else:
            self.main.clear_solution_highlights()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(stylesheet)  # Apply stylesheet to the entire application
    window = MainWindow()
    window.show()

    app.exec()
# TODO： Support Ctrl+Z to undo