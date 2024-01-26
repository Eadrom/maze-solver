#!/usr/bin/env python

from graphics import Window, Point, Line, Cell, Maze


def main():
    win = Window(800, 600)

    maze_width = 800
    maze_height = 600
    cell_size = 20
    border_size = 20

    num_cols = (maze_width - 2 * border_size) // cell_size
    num_rows = (maze_height - 2 * border_size) // cell_size

    maze = Maze(border_size, border_size, num_rows, num_cols, cell_size, cell_size, win)

    win.wait_for_close()

    exit()


if __name__ == "__main__":
    main()
