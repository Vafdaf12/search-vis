import pyglet

from picker import CellPicker
from grid import GridCell
from search import BreadthFirstSearch, DepthFirstSearch, SearchAlgorithm


CELL_SIZE = 30
OFFSET = (10, 10)
GRID_SIZE = (31, 17)

if __name__ == "__main__":
    window = pyglet.window.Window(caption="COS 314 - Search Algorithms")
    batch = pyglet.graphics.Batch()
    cells = [
        GridCell(
            size=CELL_SIZE,
            grid_pos=(
                i % GRID_SIZE[0],
                i // GRID_SIZE[0],
            ),
            pos=(
                OFFSET[0] + CELL_SIZE * (i % GRID_SIZE[0]),
                OFFSET[1] + CELL_SIZE * (i // GRID_SIZE[0]),
            ),
            batch=batch,
        )
        for i in range(GRID_SIZE[0] * GRID_SIZE[1])
    ]

    source_picker = CellPicker(CELL_SIZE, GRID_SIZE, OFFSET, (0, 0, 255))
    dest_picker = CellPicker(CELL_SIZE, GRID_SIZE, OFFSET, (0, 255, 0))

    algo: SearchAlgorithm | None = None

    @window.event
    def on_mouse_motion(x: int, y: int, dx: int, dy: int):
        if not source_picker.picked_position:
            source_picker.set_target_position(x, y)
        elif not dest_picker.picked_position:
            dest_picker.set_target_position(x, y)

    @window.event
    def on_mouse_press(x: int, y: int, button, modifiers):
        global algo
        if not source_picker.picked_position:
            source_picker.pick()
        elif not dest_picker.picked_position:
            dest_picker.pick()
            print("Picked:", source_picker.picked_position, "->", dest_picker.picked_position)
            algo = DepthFirstSearch(cells, GRID_SIZE[0], source_picker.picked_position, dest_picker.picked_position)  # type: ignore

    @window.event
    def on_draw():
        window.clear()
        batch.draw()
        source_picker.draw()
        if source_picker.picked_position:
            dest_picker.draw()

    def update_algo(dt: float):
        global algo
        if not algo:
            print("No algo")
            return
        if algo.dest_found():
            print("Dest found")
            return
        print("Update")
        algo.next()

    pyglet.clock.schedule_interval(update_algo, 1 / 20)
    pyglet.app.run()
