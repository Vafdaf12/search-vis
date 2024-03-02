from pdb import run
import pyglet
from pyglet.window import mouse, key

from picker import CellPicker
from grid import Grid
from search import BestFirstSearch, DepthFirstSearch, DistanceHeuristic, HillClimbSearch, SearchAlgorithm, BreadthFirstSearch

CELL_SIZE = 30
OFFSET = (10, 10)
GRID_SIZE = (31, 17)

if __name__ == "__main__":
    window = pyglet.window.Window(caption="COS 314 - Search Algorithms")
    grid = Grid(CELL_SIZE, *GRID_SIZE, OFFSET)

    source_picker = CellPicker(grid, (0, 0, 255))
    dest_picker = CellPicker(grid, (0, 255, 0))

    heuristic = DistanceHeuristic()
    algos: list[SearchAlgorithm] = [
        BreadthFirstSearch(grid),
        DepthFirstSearch(grid),
        BestFirstSearch(grid, heuristic),
        HillClimbSearch(grid, heuristic)
    ]
    active_algo = 0
    running = False


    @window.event
    def on_mouse_motion(x: int, y: int, dx: int, dy: int):
        if not source_picker.picked_position:
            source_picker.set_target_position(x, y)
        elif not dest_picker.picked_position:
            dest_picker.set_target_position(x, y)

    @window.event
    def on_key_press(code: int, modifiers: int):
        global grid
        global source_picker
        global dest_picker
        global active_algo
        global running
        match code:
            case key.R:
                grid.reset()
                source_picker.reset()
                dest_picker.reset()
                running = False
            case key.RIGHT:
                active_algo = (active_algo + 1) % len(algos)
                print(active_algo)
            case key.RIGHT:
                if active_algo == 0:
                    active_algo = len(algos) - 1
                else:
                    active_algo -= 1
                print(active_algo)


    @window.event
    def on_mouse_press(x: int, y: int, button: int, modifiers):
        global algo
        global running
        global heuristic
        if button == mouse.RIGHT:
            cell = grid.get_target_cell(x, y)
            if cell:
                grid.toggle_obstacle(*cell.pos)

        if button == mouse.LEFT:
            if not source_picker.picked_position:
                source_picker.pick()
            elif not dest_picker.picked_position:
                dest_picker.pick()
                assert dest_picker.picked_position

                print("Picked:", source_picker.picked_position, "->", dest_picker.picked_position)
                heuristic.set_target(dest_picker.picked_position)
                algos[active_algo].start_search(source_picker.picked_position, dest_picker.picked_position)
                running = True

    @window.event
    def on_draw():
        window.clear()
        grid.draw()
        source_picker.draw()
        if source_picker.picked_position:
            dest_picker.draw()

    def update_algo(dt: float):
        global algos
        global active_algo
        global running

        if not running:
            return

        algo = algos[active_algo]
        if algo.dest_found():
            running = False
            return
        algo.next()

    pyglet.clock.schedule_interval(update_algo, 1 / 60)
    pyglet.app.run()
