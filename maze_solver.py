#!/usr/bin/env python

from graphics import Window, Point, Line

def main():
    win = Window(800, 600)
    
    starting_point = Point(100, 100)
    ending_point = Point(500, 500)
    line_to_draw = Line(starting_point, ending_point)

    win.draw_line(line_to_draw, "blue")
    win.wait_for_close()

    exit()

if __name__ == "__main__":
    main()
