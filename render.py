from grid import Grid

from pyglet import graphics, shapes


class GridRenderer:
    def __init__(
        self, g: Grid, cell_size: int, off: tuple[int, int] = (0, 0), gap: int = 0
    ):
        self.grid = g
        self.offset = off
        self.cell_size = cell_size
        self.gap = gap

        self.batch = graphics.Batch()
        self.cells = [
            shapes.Rectangle(
                x=off[0] + self.total_cell_size * cell.pos[0],
                y=off[1] + self.total_cell_size * cell.pos[1],
                width=cell_size,
                height=cell_size,
                color=(*cell.state.value, 255),
                batch=self.batch,
            )
            for cell in g.cells
        ]

    @property
    def bounding_box(self) -> tuple[int, int, int, int]:
        """Calculates the bounding box of the grid

        Returns:
            tuple[int, int, int, int]: The bottom left and size of the rectangle
        """

        return (
            *self.offset,
            self.total_cell_size * self.grid.size[0] - self.gap,
            self.total_cell_size * self.grid.size[1] - self.gap,
        )

    @property
    def total_cell_size(self) -> int:
        return self.cell_size + self.gap

    def update(self):
        for i, cell in enumerate(self.grid.cells):
            self.cells[i].color = (*cell.state.value, 255)

    def draw(self):
        self.batch.draw()

    def get_cell_position(self, x: int, y: int) -> tuple[int, int]:
        x = self.offset[0] + x * self.total_cell_size
        y = self.offset[1] + y * self.total_cell_size
        return x, y

    def collide_cell(self, x: int, y: int) -> tuple[int, int] | None:
        x, y = x - self.offset[0], y - self.offset[1]

        if x < 0 or y < 0:
            return None

        x //= self.total_cell_size
        y //= self.total_cell_size
        if x >= self.grid.size[0] or y >= self.grid.size[1]:
            return None

        return x, y
