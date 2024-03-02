from abc import ABC, abstractmethod
from math import sqrt

class HeuristicFunction(ABC):

    @abstractmethod
    def calculate(self, state: tuple[int, int]) -> float: ...

    @abstractmethod
    def set_target(self, target: tuple[int, int]): ...


class DistanceHeuristic(HeuristicFunction):
    dest: tuple[int, int]

    def calculate(self, state: tuple[int, int]) -> float: 
        dx = state[0] - self.dest[0]
        dy = state[1] - self.dest[1]
        return sqrt(dx * dx + dy * dy)

    def set_target(self, target: tuple[int, int]):
        self.dest = target

class ReverseHeuristic(HeuristicFunction):
    dest: tuple[int, int]

    def calculate(self, state: tuple[int, int]) -> float: 
        dx = state[0] - self.dest[0]
        dy = state[1] - self.dest[1]
        return -sqrt(dx * dx + dy * dy)

    def set_target(self, target: tuple[int, int]):
        self.dest = target