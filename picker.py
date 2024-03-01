from enum import Enum
from pyglet import shapes

class PickState(Enum):
    PICKING = 0
    PICKED = 1
    INVALID = -1

class CellPicker:
    grid_pos: tuple[int, int]

    def __init__(
        self,
        cell_size: int,
        grid_size: tuple[int, int],
        grid_offset: tuple[int, int] = (0, 0),
        tint: tuple[int, int, int] = (255, 255, 255),
    ):
        self.cell_size = cell_size
        self.grid_size = grid_size
        self.grid_offset = grid_offset

        self.rect = shapes.Rectangle(0, 0, cell_size, cell_size, (*tint, 255))
        self.state = PickState.INVALID

    def set_target_position(self, targetx: int, targety: int):
        if self.state == PickState.PICKED:
            return

        if targetx < self.grid_offset[0] or targety < self.grid_offset[1]:
            self.state = PickState.INVALID
            return
        
        grid_x = (targetx - self.grid_offset[0]) // self.cell_size
        grid_y = (targety - self.grid_offset[1]) // self.cell_size

        if grid_x >= self.grid_size[0] or grid_y > self.grid_size[1]:
            self.state = PickState.INVALID
            return
        
        self.state = PickState.PICKING
        self.grid_pos = (grid_x, grid_y)

        self.__update_graphic()

    def __update_graphic(self):
        self.rect.x = self.grid_offset[0] + self.grid_pos[0]*self.cell_size
        self.rect.y = self.grid_offset[1] + self.grid_pos[1]*self.cell_size

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
