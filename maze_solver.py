#!/usr/bin/env python

from graphics import Window, Point, Line, Cell


def main():
    win = Window(800, 600)

    """
    starting_point = Point(100, 100)
    ending_point = Point(500, 500)
    line_to_draw = Line(starting_point, ending_point)
    win.draw_line(line_to_draw, "blue")
    """

    cell_size = 100

    cell_1 = Cell(win, Point(100, 100), Point(100 + cell_size, 100 + cell_size))
    cell_1.draw()

    cell_2 = Cell(
        win, Point(100 + cell_size, 100), Point(100 + 2 * cell_size, 100 + cell_size)
    )
    cell_2.draw()

    cell_3 = Cell(
        win, Point(100, 100 + cell_size), Point(100 + cell_size, 100 + 2 * cell_size)
    )
    cell_3.draw()

    cell_4 = Cell(
        win,
        Point(100 + cell_size, 100 + cell_size),
        Point(100 + 2 * cell_size, 100 + 2 * cell_size),
    )
    cell_4.draw()

    cell_1.draw_move(cell_2)
    cell_2.draw_move(cell_3)
    cell_3.draw_move(cell_4)
    cell_4.draw_move(cell_1)

    win.wait_for_close()

    exit()


if __name__ == "__main__":
    main()
