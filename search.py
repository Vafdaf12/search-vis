from abc import ABC, abstractmethod
from grid import CellState, GridCell




class SearchAlgorithm(ABC):
    grid: list[GridCell]
    grid_width: int

    def __init__(self, grid: list[GridCell], w: int):
        self.grid = grid
        self.grid_width = w

    @abstractmethod
    def next(self): ...

    @abstractmethod
    def dest_found(self) -> bool: ...

    def reset(self):
        for cell in self.grid:
            if cell.is_empty:
                cell.set_state(CellState.NONE)

    def visit(self, x: int, y: int):
        cell = self.grid[self.index(x, y)]
        if not cell.is_empty:
            return

        cell.set_state(CellState.VISITED)

    def to_visit(self, x: int, y: int):
        cell = self.grid[self.index(x, y)]
        if not cell.is_empty:
            return

        cell.set_state(CellState.TO_VISITED)

    def generate_neighbors(self, x: int, y: int, target: CellState):
        if x > 0 and self.grid[self.index(x-1, y)].state == target:
            yield (x - 1, y)
        if y < (len(self.grid) // self.grid_width) - 1 and self.grid[self.index(x, y+1)].state == target:
            yield (x, y + 1)
        if x < self.grid_width - 1 and self.grid[self.index(x+1, y)].state == target:
            yield (x + 1, y)

        if y > 0 and self.grid[self.index(x, y-1)].state == target:
            yield (x, y - 1)

    def index(self, x: int, y: int) -> int:
        return y * self.grid_width + x


class DepthFirstSearch(SearchAlgorithm):
    def __init__(
        self,
        grid: list[GridCell],
        w: int,
        start: tuple[int, int],
        dest: tuple[int, int],
    ):
        super().__init__(grid, w)

        self.found = False
        self.open = [start]
        self.dest = dest

    def next(self):
        if len(self.open) == 0:
            return

        x, *self.open = self.open
        if x == self.dest:
            self.found = True
            return

        for pos in self.generate_neighbors(*x, CellState.NONE):
            if pos not in self.open:
                self.to_visit(*pos)
                self.open.insert(0, pos)

        self.visit(*x)

    def dest_found(self) -> bool:
        return self.found

class BreadthFirstSearch(SearchAlgorithm):
    def __init__(
        self,
        grid: list[GridCell],
        w: int,
        start: tuple[int, int],
        dest: tuple[int, int],
    ):
        super().__init__(grid, w)

        self.found = False
        self.open = [start]
        self.dest = dest

    def next(self):
        if len(self.open) == 0:
            return

        x, *self.open = self.open
        if x == self.dest:
            self.found = True
            return

        for pos in self.generate_neighbors(*x, CellState.NONE):
            if pos not in self.open:
                self.to_visit(*pos)
                self.open.append(pos)

        self.visit(*x)

    def dest_found(self) -> bool:
        return self.found
