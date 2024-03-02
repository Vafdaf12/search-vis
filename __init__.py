import pyglet
from pyglet.window import mouse, key

from picker import CellPicker
from grid import CellState, Grid
from search import (
    BestFirstSearch,
    DepthFirstSearch,
    GreedyHillClimbSearch,
    HillClimbSearch,
    SearchAlgorithm,
    BreadthFirstSearch,
)
from heuristic import DistanceHeuristic

FONT = "Fira Code"
CELL_SIZE = 30
OFFSET = (10, 10)
GRID_SIZE = (30, 16)


def calculate_efficiency(grid: Grid) -> float:
    total = grid.size[0] * grid.size[1]
    current = 0
    for cell in grid.cells:
        if cell.state == CellState.OBSTACLE:
            total -= 1
        if cell.state == CellState.NONE:
            current += 1
    return current / total


if __name__ == "__main__":
    window = pyglet.window.Window(caption="COS 314 - Search Algorithms")
    grid = Grid(CELL_SIZE, *GRID_SIZE, (OFFSET[0], OFFSET[1] + CELL_SIZE))
    grid.load_from_file("last_open.map")

    window.size = (
        grid.offset[0] + (grid.gap + grid.cell_size) * grid.size[0] + OFFSET[0],
        grid.offset[1] + (grid.gap + grid.cell_size) * grid.size[1] + OFFSET[1],
    )

    source_picker = CellPicker(grid, (0, 0, 255))
    dest_picker = CellPicker(grid, (0, 255, 0))

    heuristic = DistanceHeuristic()
    algos: list[SearchAlgorithm] = [
        BreadthFirstSearch(grid),
        DepthFirstSearch(grid),
        BestFirstSearch(grid, heuristic),
        HillClimbSearch(grid, heuristic),
        GreedyHillClimbSearch(grid, heuristic),
    ]


    labels = [
        pyglet.text.Label(
            a.__str__(), FONT, font_size=16, x=OFFSET[0], y=OFFSET[1]
        )
        for a in algos
    ]
    stats_label = pyglet.text.Label(
        "",
        "Iosevka Term",
        font_size=16,
        x=window.size[0] - OFFSET[0],
        y=OFFSET[1],
        anchor_x="right",
    )

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

        if not running:
            match code:
                case key.RIGHT:
                    active_algo = (active_algo + 1) % len(algos)
                    print(active_algo)
                case key.LEFT:
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
        global active_algo
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

                print(
                    "Picked:",
                    source_picker.picked_position,
                    "->",
                    dest_picker.picked_position,
                )
                heuristic.set_target(dest_picker.picked_position)
                algos[active_algo].start_search(
                    source_picker.picked_position, dest_picker.picked_position
                )
                stats_label.text = "Running"
                running = True

    @window.event
    def on_draw():
        global active_algo
        global labels
        global stats_label

        window.clear()
        grid.draw()
        source_picker.draw()
        if source_picker.picked_position:
            dest_picker.draw()

        labels[active_algo].draw()
        stats_label.draw()

    def update_algo(dt: float):
        global algos
        global active_algo
        global running
        global grid
        global stats_label

        if not running:
            return

        algo = algos[active_algo]
        if algo.dest_found():
            percentage = round(calculate_efficiency(grid) * 100, 1)
            stats_label.text = f"{percentage}% unexplored"
            running = False
            return
        algo.next()

    pyglet.clock.schedule_interval(update_algo, 1 / 60)
    pyglet.app.run()
    grid.save_to_file("last_open.map")
