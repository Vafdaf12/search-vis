from enum import Enum
from pyglet import shapes

from render import GridRenderer


class PickState(Enum):
    PICKING = 0
    PICKED = 1
    INVALID = -1


class CellPicker:
    selected: tuple[int, int] | None = None

    def __init__(
        self,
        renderer: GridRenderer,
        tint: tuple[int, int, int] = (255, 255, 255),
    ):

        self.renderer = renderer
        self.rect = shapes.Rectangle(
            0, 0, self.renderer.cell_size, self.renderer.cell_size, (*tint, 255)
        )
        self.state = PickState.INVALID

    def set_target_position(self, targetx: int, targety: int):
        if self.state == PickState.PICKED:
            return

        cell = self.renderer.collide_cell(targetx, targety)
        if not cell:
            self.state = PickState.INVALID
            return

        self.state = PickState.PICKING
        self.__set_cell(*cell)

    def __set_cell(self, x: int, y: int):
        self.selected = x, y
        x, y = self.renderer.get_cell_position(x, y)
        self.rect.x = x
        self.rect.y = y

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
        return self.selected if self.state == PickState.PICKED else None
