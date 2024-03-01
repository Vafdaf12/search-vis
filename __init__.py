import pyglet
from pyglet.window import mouse

from picker import CellPicker
from grid import Grid
from search import SearchAlgorithm, BreadthFirstSearch

CELL_SIZE = 30
OFFSET = (10, 10)
GRID_SIZE = (31, 17)

if __name__ == "__main__":
    window = pyglet.window.Window(caption="COS 314 - Search Algorithms")
    grid = Grid(CELL_SIZE, *GRID_SIZE, OFFSET)

    source_picker = CellPicker(grid, (0, 0, 255))
    dest_picker = CellPicker(grid, (0, 255, 0))

    algo: SearchAlgorithm | None = None


    @window.event
    def on_mouse_motion(x: int, y: int, dx: int, dy: int):
        if not source_picker.picked_position:
            source_picker.set_target_position(x, y)
        elif not dest_picker.picked_position:
            dest_picker.set_target_position(x, y)

    @window.event
    def on_mouse_press(x: int, y: int, button: int, modifiers):
        global algo
        if button == mouse.RIGHT:
            cell = grid.get_target_cell(x, y)
            if cell:
                grid.toggle_obstacle(*cell.pos)

        if button == mouse.LEFT:
            if not source_picker.picked_position:
                source_picker.pick()
            elif not dest_picker.picked_position:
                dest_picker.pick()
                print("Picked:", source_picker.picked_position, "->", dest_picker.picked_position)
                algo = BreadthFirstSearch(grid, source_picker.picked_position, dest_picker.picked_position)  # type: ignore

    @window.event
    def on_draw():
        window.clear()
        grid.draw()
        source_picker.draw()
        if source_picker.picked_position:
            dest_picker.draw()

    def update_algo(dt: float):
        global algo
        if not algo:
            return
        if algo.dest_found():
            return
        algo.next()

    pyglet.clock.schedule_interval(update_algo, 1 / 20)
    pyglet.app.run()
