import sys
from itertools import product
from pathlib import Path
from typing import OrderedDict, cast

from PySide6.QtCore import QRect, Qt, Signal
from PySide6.QtGui import QAction, QColor, QPainter
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QPushButton,
    QSizePolicy,
    QTableWidget,
)
from utils import Config, Point, Solver, load_config, save_config

# INFO: This GUI relies on heavy use of Qt's dynamic properties to manage the state of the buttons.
# INFO: This may cause issues with reasons can be found in
# INFO: https://stackoverflow.com/questions/73265462/pyside6-qlabel-padding-not-applied-when-unpolish-polished
# INFO: But since the program only uses this for changing the color of the button, it should be fine


class Light(QPushButton):

    def __init__(
        self,
        row: int,
        col: int,
        parent=None,
        highlight: bool = False,
        # Edit mode boolean
        edit: bool = False,
    ):
        super().__init__(parent)
        self.row = row
        self.col = col
        self.highlight = highlight
        self.edit = edit
        self.setCheckable(True)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

    # INFO: Properties here only responsible for the visual aspect of the button
    @property
    def position(self):
        return Point(self.row, self.col)

    @property
    def highlight(self):
        return self.property("highlight")

    @highlight.setter
    def highlight(self, value: bool):
        if value != self.highlight:
            self.setProperty("highlight", value)
            self.update()

    @property
    def edit(self):
        return self.property("edit")

    @edit.setter
    def edit(self, value: bool):
        if value == self.edit:
            return None
        self.setProperty("edit", value)
        self.update()

    # NOTE: This property is only valid when in edit mode for storing the state of the button
    @property
    def _temp_state(self):
        return self.property("state")

    @_temp_state.setter
    def _temp_state(self, value: bool):
        self.setProperty("state", value)

    def paintEvent(self, event):
        super().paintEvent(event)  # Draw the button as usual
        self.style().unpolish(self)
        self.style().polish(self)
        if self.highlight:
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


# TODO: Add timeout for message
# TODO: Add hover for all QActions
# TODO: Add icon for status bar
class LightTable(QTableWidget):
    statusbarUpdate = Signal(str)

    def __init__(self, config: Config, parent=None) -> None:
        super().__init__(parent)
        # Avoid conflict with row/col method
        self.rows = config["row"]
        self.cols = config["col"]
        self.canvas: OrderedDict[Point, bool] = config["canvas"]
        self.solver = Solver(self.canvas.keys(), method=config["method"])
        self.draw_ui()
        self.is_idle: bool = config["is_idle"]
        self.highlight_active = config["highlight_active"]
        # Initialize is_edit_mode manually not with property
        self._is_edit_mode = config["is_edit_mode"]
        if self._is_edit_mode:
            self.enter_edit_mode()

    # properties
    @property
    def highlight_active(self) -> bool:
        return self._highlight_active

    # Allows for updating highlight status when highlight_active is set
    @highlight_active.setter
    def highlight_active(self, value: bool) -> None:
        self._highlight_active = value
        if value:
            self.update_solution_highlights()
        else:
            self.clear_solution_highlights()

    @property
    def is_edit_mode(self) -> bool:
        return self._is_edit_mode

    @is_edit_mode.setter
    def is_edit_mode(self, value: bool) -> None:
        self._is_edit_mode = value
        if value:
            self.enter_edit_mode()
        else:
            self.exit_edit_mode()

    def draw_ui(self):
        self.setRowCount(self.rows)
        self.setColumnCount(self.cols)
        self.horizontalHeader().hide()
        self.verticalHeader().hide()
        self.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        # TODO: Sweep to turn on and off
        self.setSelectionMode(QTableWidget.SelectionMode.NoSelection)
        for r, c in product(range(self.rows), range(self.cols)):
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

    def toggle_handler(self):
        light = cast(Light, self.sender())
        if self.is_edit_mode:
            self.edit_mode_handler(light)
            return None

        if self.is_idle:
            self.idle_mode_handler(light)
        else:
            self.game_mode_handler(light)

        return None

    def game_mode_handler(self, light: Light):
        nearby_lights = self._get_nearby_lights(light.position)
        self.canvas[light.position] = light.isChecked()
        for point in nearby_lights:
            near_light = self.get_light(point)
            near_light.setChecked(not near_light.isChecked())
            self.canvas[point] = near_light.isChecked()
        if self.highlight_active:
            self.update_solution_highlights()

    def idle_mode_handler(self, light: Light):
        self.canvas[light.position] = light.isChecked()
        if self.highlight_active:
            self.update_solution_highlights()

    def edit_mode_handler(self, light: Light):
        if light.isChecked():
            self.canvas[light.position] = False
        else:
            del self.canvas[light.position]

    def clear_solution_highlights(self):
        self.solution = []
        for point in self.canvas:
            light = self.get_light(point)
            light.highlight = False

    def update_solution_highlights(self):
        self.solution = self.solve()
        for point in self.canvas:
            light = self.get_light(point)
            light.highlight = True if point in self.solution else False

    def enter_edit_mode(self):
        for r, c in product(range(self.rows), range(self.cols)):
            light = self.get_light(Point(r, c))
            light.edit = True
            light.setEnabled(True)
            # store current state of the light
            light._temp_state = True if self.canvas.get(Point(r, c)) else False
            if Point(r, c) in self.canvas:
                light.setChecked(True)
            else:
                light.setChecked(False)
        self.statusbarUpdate.emit("Editing Canvas ...")

    def exit_edit_mode(self):
        # Sync Solver background with the current state
        self.solver.background = self.canvas
        for r, c in product(range(self.rows), range(self.cols)):
            light = self.get_light(Point(r, c))
            light.edit = False
            if Point(r, c) in self.canvas:
                light.setEnabled(True)
                light.setChecked(light._temp_state)
            else:
                light.setEnabled(False)
        if self.solver.is_empty:
            self.statusbarUpdate.emit("No lights on the canvas.")
        elif self.solver.is_full_rank:
            self.statusbarUpdate.emit("Every light status is reachable.")
        else:
            self.statusbarUpdate.emit(
                f"Current Matrix Rank: {self.solver.rank}, some status unreachable."
            )

    def solve(self) -> list[Point]:
        current = [point for point in self.canvas if self.canvas[point]]
        code, result = self.solver.solve(current, [])
        length = len(result)
        if code == Solver.Result.EMPTY_CANVAS:
            self.statusbarUpdate.emit("No solution for empty canvas.")
        elif code == Solver.Result.EMPTY_SOLUTION:
            self.statusbarUpdate.emit("Problem solved")
        elif code == Solver.Result.FULL_RANK_SOLVED:
            self.statusbarUpdate.emit(f"Unique solution found with {length} moves.")
        elif code == Solver.Result.INCOMPLETE_RANK_SOLVED:
            self.statusbarUpdate.emit(
                f"Multiple solutions found, best solution with {length} moves."
            )
        elif code == Solver.Result.INCOMPLETE_RANK_UNSOLVED:
            self.statusbarUpdate.emit("No solution found for non-full rank canvas")
        return result

    def _get_nearby_lights(self, point: Point) -> set[Point]:
        """Get the points around the clicked point"""
        neighbors = set(
            (
                Point(point.x - 1, point.y),
                Point(point.x + 1, point.y),
                Point(point.x, point.y - 1),
                Point(point.x, point.y + 1),
            )
        )
        return set.intersection(neighbors, self.canvas.keys())

    def get_light(self, point: Point) -> Light:
        light = self.cellWidget(point.x, point.y)
        assert isinstance(light, Light)
        return light

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

    def _clean_up(self):
        self.solver.close()


class MainWindow(QMainWindow):
    statusbarUpdate = Signal(str)

    def __init__(self, config: Config):
        super().__init__()
        self.setWindowTitle("Lights Out Solver")
        self.setGeometry(100, 100, 400, 400)

        toolbar = self.addToolBar("Toolbar")
        toolbar.setContextMenuPolicy(Qt.ContextMenuPolicy.PreventContextMenu)
        toolbar.setMovable(True)
        self.main = LightTable(config, self)

        statusbar = self.statusBar()
        self.main.statusbarUpdate.connect(statusbar.showMessage)

        idle_mode_action = QAction("Idle Mode", self)
        idle_mode_action.setCheckable(True)
        idle_mode_action.setShortcut("i")
        idle_mode_action.triggered.connect(self.toggle_idle_mode)
        idle_mode_action.setChecked(config["is_idle"])

        edit_mode_action = QAction("Edit Mode", self)
        edit_mode_action.setCheckable(True)
        edit_mode_action.setShortcut("e")
        edit_mode_action.triggered.connect(self.toggle_edit_mode)
        edit_mode_action.setChecked(config["is_edit_mode"])

        solution_highlight_action = QAction("Highlight Solution", self)  # Renamed text
        solution_highlight_action.setCheckable(True)
        solution_highlight_action.setShortcut("s")
        solution_highlight_action.setChecked(self.main.highlight_active)
        solution_highlight_action.triggered.connect(self.toggle_solution_highlight)
        solution_highlight_action.setChecked(config["highlight_active"])

        toolbar.addAction(idle_mode_action)
        toolbar.addAction(edit_mode_action)
        toolbar.addAction(solution_highlight_action)  # Renamed action
        # for testing purposes
        self.setCentralWidget(self.main)

    def toggle_idle_mode(self):
        action = cast(QAction, self.sender())
        self.main.is_idle = action.isChecked()

    def toggle_edit_mode(self):
        action = cast(QAction, self.sender())
        self.main.is_edit_mode = action.isChecked()

    def toggle_solution_highlight(self):
        action = cast(QAction, self.sender())
        self.main.highlight_active = action.isChecked()
        if self.main.highlight_active:
            self.main.update_solution_highlights()
        else:
            self.main.clear_solution_highlights()

    def closeEvent(self, event):
        self.main._clean_up()
        super().closeEvent(event)


if __name__ == "__main__":

    current_dir = Path(__file__).resolve().parent
    default_state = load_config(current_dir / "config.json")
    app = QApplication(sys.argv)
    stylesheet_path = current_dir / "style.qss"
    with open(stylesheet_path, "r") as f:
        stylesheet = f.read()
        app.setStyleSheet(stylesheet)  # Apply stylesheet to the entire application

    window = MainWindow(default_state)
    window.show()

    app.exec()
# TODO: Support Ctrl+Z to undo
