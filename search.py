from abc import ABC, abstractmethod
from grid import CellState, Grid


class SearchAlgorithm(ABC):
    grid: Grid

    def __init__(self, grid: Grid):
        self.grid = grid

    @abstractmethod
    def next(self): ...

    @abstractmethod
    def dest_found(self) -> bool: ...


    def generate_neighbors(self, x: int, y: int, target: CellState):
        cell = self.grid.get_cell(x-1, y)
        if cell and cell.state == target:
            yield cell.pos

        cell = self.grid.get_cell(x, y+1)
        if cell and cell.state == target:
            yield cell.pos

        cell = self.grid.get_cell(x+1, y)
        if cell and cell.state == target:
            yield cell.pos
            
        cell = self.grid.get_cell(x, y-1)
        if cell and cell.state == target:
            yield cell.pos

class DepthFirstSearch(SearchAlgorithm):
    def __init__(
        self,
        grid: Grid,
        start: tuple[int, int],
        dest: tuple[int, int],
    ):
        super().__init__(grid)

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
                self.grid.want_to_visit(*pos)
                self.open.insert(0, pos)

        self.grid.visit(*x)

    def dest_found(self) -> bool:
        return self.found


class BreadthFirstSearch(SearchAlgorithm):
    def __init__(
        self,
        grid: Grid,
        start: tuple[int, int],
        dest: tuple[int, int],
    ):
        super().__init__(grid)

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
                self.grid.want_to_visit(*pos)
                self.open.append(pos)

        self.grid.visit(*x)

    def dest_found(self) -> bool:
        return self.found
