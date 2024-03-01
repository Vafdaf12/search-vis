import pyglet
from pyglet import shapes

from picker import CellPicker

window = pyglet.window.Window(caption="COS 314 - Search Algorithms")

CELL_SIZE = 30
OFFSET = (10, 10)
GRID_SIZE = (20, 10)

batch = pyglet.graphics.Batch()
grid = [
    shapes.Rectangle(
        x=OFFSET[0] + CELL_SIZE * (i % GRID_SIZE[0]),
        y=OFFSET[1] + CELL_SIZE * (i // GRID_SIZE[0]),
        width=CELL_SIZE,
        height=CELL_SIZE,
        batch=batch,
        color=(
            int((i % GRID_SIZE[0]) / GRID_SIZE[0] * 255),
            int((i // GRID_SIZE[0]) / GRID_SIZE[1] * 255),
            0,
            255,
        ),
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
