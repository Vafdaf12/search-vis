from pyglet import shapes, graphics
from enum import Enum


class CellState(Enum):
    NONE = (18, 18, 18)
    TO_VISITED = (19, 82, 128)
    VISITED = (7, 220, 227)
    OBSTACLE = (255, 255, 255)


class GridCell:
    def __init__(
        self,
        size: int,
        grid_pos: tuple[int, int],
        pos: tuple[int, int],
        batch: graphics.Batch,
        state: CellState = CellState.NONE,
    ):

        self.pos = grid_pos
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

    @property
    def is_empty(self):
        return self.state in [CellState.NONE, CellState.TO_VISITED, CellState.VISITED]


class Grid:
    def __init__(
        self, cell_size: int, width: int, height: int, offset: tuple[int, int] = (0, 0)
    ):
        self.gap = 1
        self.cell_size = cell_size
        self.offset = offset
        self.size = (width, height)
        self.batch = graphics.Batch()
        self.cells = [
            GridCell(
                size=cell_size,
                grid_pos=(
                    i % width,
                    i // width,
                ),
                pos=(
                    offset[0] + (cell_size+self.gap) * (i % width),
                    offset[1] + (cell_size+self.gap) * (i // width),
                ),
                batch=self.batch,
            )
            for i in range(width * height)
        ]

    def get_target_cell(self, x: int, y: int) -> GridCell | None:
        x = (x - self.offset[0]) // (self.cell_size + self.gap)
        y = (y - self.offset[1]) // (self.cell_size + self.gap)

        return self.get_cell(x, y)


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
        cell.set_state(CellState.TO_VISITED)
        return True

    def visit(self, x: int, y: int) -> bool:
        cell = self.get_cell(x, y)
        if not cell:
            return False
        if cell.state == CellState.OBSTACLE:
            return False
        cell.set_state(CellState.VISITED)
        return True

    def toggle_obstacle(self, x: int, y: int) -> bool:
        cell = self.get_cell(x, y)
        if not cell:
            return False

        if cell.state == CellState.OBSTACLE:
            cell.set_state(CellState.NONE)
        else:
            cell.set_state( CellState.OBSTACLE)

        return True

    def reset(self, reset_obstacles=False):
        for cell in self.cells:
            if cell.is_empty:
                cell.set_state(CellState.NONE)
            elif reset_obstacles:
                cell.set_state(CellState.NONE)

    def draw(self):
        self.batch.draw()
    
    def load_from_file(self, path: str): 
        lines = []
        with open(path, 'r+') as file:
            lines = file.readlines()
        
        w, h, *lines = lines
        w, h = int(w), int(h)

        self.size = (w, h)
        self.batch = graphics.Batch()
        self.cells = [
            GridCell(
                size=self.cell_size,
                grid_pos=(
                    i % w,
                    i // w,
                ),
                pos=(
                    self.offset[0] + (self.cell_size+self.gap) * (i % w),
                    self.offset[1] + (self.cell_size+self.gap) * (i // w),
                ),
                batch=self.batch,
            )
            for i in range(w * h)
        ]
        for y, line in enumerate(reversed(lines)):
            for x, c in enumerate(line):
                cell = self.get_cell(x, y)
                print(x, y)
                if not cell:
                    continue
                match c:
                    case ".":
                        cell.set_state(CellState.NONE)
                    case "#":
                        cell.set_state(CellState.OBSTACLE)


    def save_to_file(self, path: str): 
        lines = [
            str(self.size[0]) + "\n",
            str(self.size[1])
        ]
        for y in range(self.size[1]-1, -1, -1):
            line = "\n"
            for x in range(self.size[0]):
                cell = self.get_cell(x, y)
                assert cell
                if cell.state == CellState.OBSTACLE:
                    line += "#"
                else:
                    line += "."
            lines.append(line)

        with open(path, 'w+') as file:
            file.writelines(lines)