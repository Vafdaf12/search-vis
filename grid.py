from pyglet import shapes, graphics
from enum import Enum


class CellState(Enum):
    NONE = (18, 18, 18)
    TO_VISITED = (52, 174, 235)
    VISITED = (44, 120, 242)
    OBSTACLE = (255, 255, 255)


class GridCell:
    def __init__(
        self,
        size: int,
        pos: tuple[int, int],
        batch: graphics.Batch,
        state: CellState = CellState.NONE,
    ):

        self.state = state
        self.rect = shapes.Rectangle(
            x=pos[0],
            y=pos[1],
            width=size,
            height=size,
            color=(*state.value, 255),
            batch=batch,
        )

    def set_state(self, state: CellState):
        self.state = state
        self.rect.color = (*state.value, 255)
