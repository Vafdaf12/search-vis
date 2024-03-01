import pyglet

from picker import CellPicker
from grid import GridCell


CELL_SIZE = 30
OFFSET = (10, 10)
GRID_SIZE = (20, 10)

if __name__ == "__main__":
    window = pyglet.window.Window(caption="COS 314 - Search Algorithms")
    batch = pyglet.graphics.Batch()
    cells = [
        GridCell(
            size=CELL_SIZE,
            pos=(
                OFFSET[0] + CELL_SIZE * (i % GRID_SIZE[0]),
                OFFSET[1] + CELL_SIZE * (i // GRID_SIZE[0]),
            ),
            batch=batch
        )
        for i in range(GRID_SIZE[0] * GRID_SIZE[1])
    ]

    source_picker = CellPicker(CELL_SIZE, GRID_SIZE, OFFSET, (0, 0, 255))
    dest_picker = CellPicker(CELL_SIZE, GRID_SIZE, OFFSET, (0, 255, 0))

    @window.event
    def on_mouse_motion(x: int, y: int, dx: int, dy: int):
        if not source_picker.picked_position:
            source_picker.set_target_position(x, y)
        elif not dest_picker.picked_position:
            dest_picker.set_target_position(x, y)

    @window.event
    def on_mouse_press(x: int, y: int, button, modifiers):
        if not source_picker.picked_position:
            source_picker.pick()
        if not dest_picker.picked_position:
            dest_picker.pick()

    @window.event
    def on_draw():
        window.clear()
        batch.draw()
        source_picker.draw()
        if source_picker.picked_position:
            dest_picker.draw()

    pyglet.app.run()
