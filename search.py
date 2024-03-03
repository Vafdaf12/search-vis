from abc import ABC, abstractmethod
from dataclasses import dataclass, field
import random

from grid import CellState, Grid
from heuristic import HeuristicFunction

from heapq import heappop, heappush

class SearchAlgorithm(ABC):
    grid: Grid

    def __init__(self, grid: Grid):
        self.grid = grid

    @abstractmethod
    def next(self): ...

    @abstractmethod
    def dest_found(self) -> bool: ...

    @abstractmethod
    def start_search(self, src: tuple[int, int], dest: tuple[int, int]): ...

    def generate_neighbors(self, x: int, y: int, target: CellState):
        cell = self.grid.get_cell(x - 1, y)
        if cell and cell.state == target:
            yield cell.pos

        cell = self.grid.get_cell(x, y + 1)
        if cell and cell.state == target:
            yield cell.pos

        cell = self.grid.get_cell(x + 1, y)
        if cell and cell.state == target:
            yield cell.pos

        cell = self.grid.get_cell(x, y - 1)
        if cell and cell.state == target:
            yield cell.pos


class DepthFirstSearch(SearchAlgorithm):
    def __init__(self, grid: Grid):
        super().__init__(grid)
        self.found = False

    def start_search(self, src: tuple[int, int], dest: tuple[int, int]):
        self.open = [src]
        self.dest = dest
        self.found = False

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

    def __str__(self) -> str:
        return "Depth-First Search"


class BreadthFirstSearch(SearchAlgorithm):
    def __init__(self, grid: Grid):
        super().__init__(grid)
        self.found = False

    def start_search(self, src: tuple[int, int], dest: tuple[int, int]):
        self.open = [src]
        self.dest = dest
        self.found = False

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

    def __str__(self) -> str:
        return "Breadth-First Search"



@dataclass(order=True)
class HeuristicState:
    value: float
    state: tuple[int, int] = field(compare=False)



class BestFirstSearch(SearchAlgorithm):
    open: list[HeuristicState] = []
    found: bool = False

    def __init__(self, grid: Grid, heuristic: HeuristicFunction):
        super().__init__(grid)
        self.heuristic = heuristic

    def start_search(self, src: tuple[int, int], dest: tuple[int, int]):
        self.open = [HeuristicState(self.heuristic.calculate(src), src)]
        self.dest = dest
        self.found = False

    def next(self):
        if len(self.open) == 0:
            return

        x = heappop(self.open).state
        if x == self.dest:
            self.found = True
            return

        for pos in self.generate_neighbors(*x, CellState.NONE):
            if pos not in self.open:
                self.grid.want_to_visit(*pos)
                heappush(self.open, HeuristicState(self.heuristic.calculate(pos), pos))

        self.grid.visit(*x)

    def dest_found(self) -> bool:
        return self.found

    def __str__(self) -> str:
        return "Best-First Search"

class HillClimbSearch(SearchAlgorithm):
    open: list[HeuristicState] = []
    found: bool = False

    def __str__(self) -> str:
        return "Hill Climbing Search"

    def __init__(self, grid: Grid, heuristic: HeuristicFunction):
        super().__init__(grid)
        self.heuristic = heuristic

    def start_search(self, src: tuple[int, int], dest: tuple[int, int]):
        self.open = [HeuristicState(self.heuristic.calculate(src), src)]
        self.dest = dest
        self.found = False

    def next(self):
        if len(self.open) == 0:
            return

        x, *self.open = self.open
        if x.state == self.dest:
            self.found = True
            return

        children = []
        for pos in self.generate_neighbors(*x.state, CellState.NONE):
            if pos not in self.open:
                self.grid.want_to_visit(*pos)
                heappush(children, HeuristicState(self.heuristic.calculate(pos), pos))
        
        self.open = children + self.open
        self.grid.visit(*x.state)

    def dest_found(self) -> bool:
        return self.found

class GreedyHillClimbSearch(SearchAlgorithm):
    found: bool = False
    path: list[HeuristicState] = []

    def __init__(self, grid: Grid, heuristic: HeuristicFunction):
        super().__init__(grid)
        self.heuristic = heuristic

    def start_search(self, src: tuple[int, int], dest: tuple[int, int]):
        self.path = [HeuristicState(self.heuristic.calculate(src), src)]
        self.dest = dest
        self.found = False

    def next(self):
        if len(self.path) == 0:
            self.found = True
            return

        cur = self.path[len(self.path)-1]
        if cur.state == self.dest:
            self.found = True
            return

        self.grid.visit(*cur.state)

        for pos in self.generate_neighbors(*cur.state, CellState.NONE):
            h = HeuristicState(self.heuristic.calculate(pos), pos)
            if h < cur:
                self.grid.want_to_visit(*pos)
                self.path.append(h)
                return

        self.path.pop()

    def dest_found(self) -> bool:
        return self.found

    def __str__(self) -> str:
        return "Greedy Hill Climbing Search"

class TabuSearch(SearchAlgorithm):
    found: bool = False
    path: list[HeuristicState] = []

    def __init__(self, grid: Grid, heuristic: HeuristicFunction):
        super().__init__(grid)
        self.heuristic = heuristic

    def start_search(self, src: tuple[int, int], dest: tuple[int, int]):
        self.path = [HeuristicState(self.heuristic.calculate(src), src)]
        self.dest = dest
        self.found = False

    def next(self):
        if len(self.path) == 0:
            self.found = True
            return

        cur = self.path[len(self.path)-1]
        if cur.state == self.dest:
            self.found = True
            return

        self.grid.visit(*cur.state)

        children = list(self.generate_neighbors(*cur.state, CellState.NONE))
        for pos in children:
            h = HeuristicState(self.heuristic.calculate(pos), pos)
            if h < cur:
                self.grid.want_to_visit(*pos)
                self.path.append(h)
                return

        if len(children) == 0:
            self.path.pop()
        else:
            value = random.sample(children, 1)[0]

            h = HeuristicState(self.heuristic.calculate(value), value)
            self.grid.want_to_visit(*value)
            self.path.append(h)
            


    def dest_found(self) -> bool:
        return self.found

    def __str__(self) -> str:
        return "Tabu Search"