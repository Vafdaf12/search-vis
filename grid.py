from dataclasses import dataclass
from enum import Enum


class CellState(Enum):
    NONE = (18, 18, 18)
    TO_VISITED = (19, 82, 128)
    VISITED = (7, 220, 227)
    OBSTACLE = (255, 255, 255)


@dataclass
class GridCell:
    pos: tuple[int, int]
    state: CellState = CellState.NONE

    @property
    def is_empty(self):
        return self.state in [CellState.NONE, CellState.TO_VISITED, CellState.VISITED]


class Grid:
    def __init__(self, width: int, height: int):
        self.size = (width, height)
        self.cells = [GridCell((i % width, i // width)) for i in range(width * height)]

    def get_cell(self, x: int, y: int) -> GridCell | None:
        if x < 0 or x >= self.size[0]:
            return None
        if y < 0 or y >= self.size[1]:
            return None

        return self.cells[y * self.size[0] + x]

    def want_to_visit(self, x: int, y: int) -> bool:
        cell = self.get_cell(x, y)
        if not cell:
            return False
        if cell.state == CellState.OBSTACLE:
            return False
        cell.state = CellState.TO_VISITED
        return True

    def visit(self, x: int, y: int) -> bool:
        cell = self.get_cell(x, y)
        if not cell:
            return False
        if cell.state == CellState.OBSTACLE:
            return False
        cell.state = CellState.VISITED
        return True

    def toggle_obstacle(self, x: int, y: int) -> bool:
        cell = self.get_cell(x, y)
        if not cell:
            return False

        if cell.state == CellState.OBSTACLE:
            cell.state = CellState.NONE
        else:
            cell.state = CellState.OBSTACLE

        return True

    def reset(self, reset_obstacles=False):
        for cell in self.cells:
            if cell.is_empty:
                cell.state = CellState.NONE
            elif reset_obstacles:
                cell.state = CellState.NONE

    def load_from_file(self, path: str):
        lines = []
        with open(path, "r+") as file:
            lines = file.readlines()

        w, h, *lines = lines
        w, h = int(w), int(h)

        self.size = (w, h)
        self.cells = [GridCell((i % w, i // w)) for i in range(w * h)]
        for y, line in enumerate(reversed(lines)):
            for x, c in enumerate(line):
                cell = self.get_cell(x, y)
                print(x, y)
                if not cell:
                    continue
                match c:
                    case ".":
                        cell.state = CellState.NONE
                    case "#":
                        cell.state = CellState.OBSTACLE

    def save_to_file(self, path: str):
        lines = [str(self.size[0]) + "\n", str(self.size[1])]
        for y in range(self.size[1] - 1, -1, -1):
            line = "\n"
            for x in range(self.size[0]):
                cell = self.get_cell(x, y)
                assert cell
                if cell.state == CellState.OBSTACLE:
                    line += "#"
                else:
                    line += "."
            lines.append(line)

        with open(path, "w+") as file:
            file.writelines(lines)
