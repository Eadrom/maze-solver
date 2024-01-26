#!/usr/bin/env python

from graphics import Window, Point, Line, Cell, Maze


def main():
    # Create a window with dimensions 800x600
    win = Window(800, 600)

    # Define maze dimensions and properties
    maze_width = 800
    maze_height = 600
    cell_size = 20
    border_size = 20

    # Calculate the number of columns and rows based on cell and border size
    num_cols = (maze_width - 2 * border_size) // cell_size
    num_rows = (maze_height - 2 * border_size) // cell_size

    # Create a Maze object with specified properties
    maze = Maze(border_size, border_size, num_rows, num_cols, cell_size, cell_size, win)

    # Set the maze in the window to allow interaction
    win.maze = maze

    win.wait_for_close()

    exit()


if __name__ == "__main__":
    main()
