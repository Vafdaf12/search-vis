from enum import Enum
from pyglet import shapes

from grid import Grid, GridCell

class PickState(Enum):
    PICKING = 0
    PICKED = 1
    INVALID = -1

class CellPicker:

    def __init__(
        self,
        grid: Grid,
        tint: tuple[int, int, int] = (255, 255, 255),
    ):
        self.grid = grid
        self.rect = shapes.Rectangle(0, 0, self.grid.cell_size, self.grid.cell_size, (*tint, 255))
        self.state = PickState.INVALID

    def set_target_position(self, targetx: int, targety: int):
        if self.state == PickState.PICKED:
            return
        
        cell = self.grid.get_target_cell(targetx, targety)
        if not cell:
            self.state = PickState.INVALID
            return

        self.state = PickState.PICKING
        self.__set_cell(cell)

    def __set_cell(self, cell: GridCell):
        self.grid_pos = cell.pos
        self.rect.x = cell.rect.x
        self.rect.y = cell.rect.y


    def pick(self):
        if self.state != PickState.PICKING:
            return
        self.state = PickState.PICKED

    def reset(self):
        if self.state != PickState.PICKED:
            return
        self.state = PickState.INVALID

    def draw(self):
        if self.state != PickState.INVALID:
            self.rect.draw()

    @property
    def picked_position(self) -> tuple[int, int] | None:
        return self.grid_pos if self.state == PickState.PICKED else None
