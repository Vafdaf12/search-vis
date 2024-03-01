import pyglet
from pyglet import shapes

window = pyglet.window.Window(caption="COS 314 - Search Algorithms")
label = pyglet.text.Label(
    "Hello, World!",
    font_name="Iosevka Term",
    font_size=36,
    x=window.width // 2,
    y=window.height // 2,
    anchor_x="center",
    anchor_y="center",
)

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


@window.event
def on_draw():
    window.clear()
    label.draw()
    batch.draw()


pyglet.app.run()
