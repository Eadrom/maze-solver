#!/usr/bin/env python

from graphics import Window, Point, Line, Cell

def main():
    win = Window(800, 600)

    starting_point = Point(100, 100)
    ending_point = Point(500, 500)
    line_to_draw = Line(starting_point, ending_point)

    cell_1 = Cell(win, Point(200, 250), Point(300, 350))
    cell_1.has_bottom_wall =  False
    cell_1.draw()

    win.draw_line(line_to_draw, "blue")
    win.wait_for_close()

    exit()

if __name__ == "__main__":
    main()
