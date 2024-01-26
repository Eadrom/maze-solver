#!/usr/bin/env python

from tkinter import Tk, BOTH, Canvas, messagebox
import time, random


class Window:
    def __init__(self, width, height):
        # Initialize the main window
        self.__root = Tk()
        self.__root.title("Maze Solver")
        self.__root.protocol("WM_DELETE_WINDOW", self.close)
        self.__root.resizable(0, 0)
        # Create a canvas inside the window for drawing
        self.__canvas = Canvas(self.__root, width=width, height=height, bg="white")
        self.__canvas.pack(fill=BOTH, expand=1)
        # Set up event binding for mouse click
        self.__canvas.bind("<Button-1>", self.click_handler)
        # Show an informational popup on startup
        self.show_info_popup()
        self.maze = None

    def show_info_popup(self):
        # Display an informational popup on application startup
        instructions_title = "Welcome!"
        instructions_info = "Welcome to Maze Solver!\nClick inside the window to solve the maze.\nOnce the maze is solved, click again in the window to reset it."
        popup = messagebox.showinfo(instructions_title, instructions_info)

    def click_handler(self, event):
        # Function to execute when clicking inside the window
        if self.maze.is_solved is True:
            # Clear the canvas and generate a new maze if the current maze is solved
            self.__canvas.delete("all")
            self.maze = self.generate_new_maze(self.maze)
        else:
            # Solve the maze if it's not already solved
            self.maze.solve()

    def generate_new_maze(self, maze):
        # Generate a new maze with the same parameters
        return Maze(
            maze.x1,
            maze.y1,
            maze.num_rows,
            maze.num_cols,
            maze.cell_size_x,
            maze.cell_size_y,
            maze.win,
        )

    def redraw(self):
        # Update the main window
        self.__root.update_idletasks()
        self.__root.update()

    def draw_line(self, line, color=None):
        # Draw a line on the canvas
        line.draw(self.__canvas, color)

    def wait_for_close(self):
        # Start the event loop to keep the window open until closed
        self.__window_is_running = True
        while self.__window_is_running is True:
            self.redraw()

    def close(self):
        # Close the window when the close button is clicked
        self.__window_is_running = False


class Point:
    def __init__(self, x, y):
        # Represents a point in 2D space
        self.x = x
        self.y = y


class Line:
    def __init__(self, start_point, end_point, color="black"):
        # Represents a line between two points
        self.start_point = start_point
        self.end_point = end_point

    def draw(self, canvas, color="black"):
        # Draw the line on the canvas
        canvas.create_line(
            self.start_point.x,
            self.start_point.y,
            self.end_point.x,
            self.end_point.y,
            fill=color,
            width=2,
        )
        canvas.pack(fill=BOTH, expand=1)


class Cell:
    def __init__(self, tl_point, br_point, window=None):
        # Initialize a cell with top-left and bottom-right points, and an optional window
        self.top_left_point = tl_point
        self.bottom_right_point = br_point
        self.__window = window
        self.has_left_wall = True
        self.has_top_wall = True
        self.has_right_wall = True
        self.has_bottom_wall = True
        self.visited = False

    def draw(self):
        # Draw the walls of the cell using lines on the canvas
        line_color_left = "black" if self.has_left_wall else "white"
        line = Line(
            Point(self.top_left_point.x, self.top_left_point.y),
            Point(self.top_left_point.x, self.bottom_right_point.y),
            color=line_color_left,
        )
        self.__window.draw_line(line, color=line_color_left)

        line_color_top = "black" if self.has_top_wall else "white"
        line = Line(
            Point(self.top_left_point.x, self.top_left_point.y),
            Point(self.bottom_right_point.x, self.top_left_point.y),
            color=line_color_top,
        )
        self.__window.draw_line(line, color=line_color_top)

        line_color_right = "black" if self.has_right_wall else "white"
        line = Line(
            Point(self.bottom_right_point.x, self.top_left_point.y),
            Point(self.bottom_right_point.x, self.bottom_right_point.y),
            color=line_color_right,
        )
        self.__window.draw_line(line, color=line_color_right)

        line_color_bottom = "black" if self.has_bottom_wall else "white"
        line = Line(
            Point(self.top_left_point.x, self.bottom_right_point.y),
            Point(self.bottom_right_point.x, self.bottom_right_point.y),
            color=line_color_bottom,
        )
        self.__window.draw_line(line, color=line_color_bottom)

    def draw_move(self, target_cell, undo=False):
        # Draw a line between the center of the current cell and the center of the target cell
        if undo is False:
            line_color = "red"
        else:
            line_color = "white"

        # Find the center of the current cell
        self.center = Point(
            self.top_left_point.x
            + (self.bottom_right_point.x - self.top_left_point.x) / 2,
            self.top_left_point.y
            + (self.bottom_right_point.y - self.top_left_point.y) / 2,
        )

        # Find the center of the target cell
        target_cell_center = Point(
            target_cell.top_left_point.x
            + (target_cell.bottom_right_point.x - target_cell.top_left_point.x) / 2,
            target_cell.top_left_point.y
            + (target_cell.bottom_right_point.y - target_cell.top_left_point.y) / 2,
        )

        # Draw a line between the two centers on the canvas
        self.__window.draw_line(Line(self.center, target_cell_center), line_color)


class Maze:
    def __init__(
        self,
        x1,
        y1,
        num_rows,
        num_cols,
        cell_size_x,
        cell_size_y,
        win=None,
    ):
        # Initialize a maze with parameters and create cells
        self.x1 = x1
        self.y1 = y1
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self.win = win
        self.cells = []
        self.__create_cells()
        self.is_solved = False

    def __create_cells(self):
        # Create a grid of cells based on the specified parameters
        for l in range(0, self.num_cols):
            self.cells.append([])
            for w in range(0, self.num_rows):
                self.cells[l].append(
                    Cell(
                        Point(
                            self.x1 + l * self.cell_size_x,
                            self.y1 + w * self.cell_size_y,
                        ),
                        Point(
                            self.x1 + l * self.cell_size_x + self.cell_size_x,
                            self.y1 + w * self.cell_size_y + self.cell_size_y,
                        ),
                        self.win,
                    )
                )
        if self.win is not None:
            self.__draw_cells()

    def __draw_cells(self):
        # Draw the cells on the canvas
        for l in range(0, self.num_cols):
            for w in range(0, self.num_rows):
                self.cells[l][w].draw()
                self.__animate()
        self.__break_entrance_and_exit()
        self.__animate()
        self.__break_walls_r(0, 0)
        self.__reset_visited_state()

    def __animate(self):
        # Animate the drawing if a window is provided
        if self.win is not None:
            self.win.redraw()
            time.sleep(0.01)

    def __break_entrance_and_exit(self):
        # Break the entrance and exit walls of the maze
        self.cells[0][0].has_top_wall = False
        self.cells[self.num_cols - 1][self.num_rows - 1].has_bottom_wall = False

        if self.win is not None:
            self.cells[0][0].draw()
            self.cells[self.num_cols - 1][self.num_rows - 1].draw()

    def __break_walls_r(self, x, y):
        # Recursively break walls to create the maze
        self.cells[x][y].visited = True

        while True:
            non_visited_cells = []
            if x - 1 >= 0 and not self.cells[x - 1][y].visited:
                non_visited_cells.append([x - 1, y])
            if x + 1 < self.num_cols and not self.cells[x + 1][y].visited:
                non_visited_cells.append([x + 1, y])
            if y - 1 >= 0 and not self.cells[x][y - 1].visited:
                non_visited_cells.append([x, y - 1])
            if y + 1 < self.num_rows and not self.cells[x][y + 1].visited:
                non_visited_cells.append([x, y + 1])
            if len(non_visited_cells) == 0:
                self.cells[x][y].draw()
                return
            else:
                next_cell = random.choice(non_visited_cells)
                non_visited_cells.remove(next_cell)

                # Break walls facing each other in the current cell and the next cell
                if x - 1 == next_cell[0]:
                    self.cells[x][y].has_left_wall = False
                    self.cells[next_cell[0]][next_cell[1]].has_right_wall = False
                elif x + 1 == next_cell[0]:
                    self.cells[x][y].has_right_wall = False
                    self.cells[next_cell[0]][next_cell[1]].has_left_wall = False
                elif y - 1 == next_cell[1]:
                    self.cells[x][y].has_top_wall = False
                    self.cells[next_cell[0]][next_cell[1]].has_bottom_wall = False
                elif y + 1 == next_cell[1]:
                    self.cells[x][y].has_bottom_wall = False
                    self.cells[next_cell[0]][next_cell[1]].has_top_wall = False

                self.cells[x][y].draw()
                self.cells[next_cell[0]][next_cell[1]].draw()

                self.__break_walls_r(next_cell[0], next_cell[1])

    def __reset_visited_state(self):
        # Reset the visited state of all cells in the maze
        for x in range(0, self.num_cols):
            for y in range(0, self.num_rows):
                self.cells[x][y].visited = False

    def solve(self):
        # Solve the maze using recursive backtracking
        self.__solve_r(0, 0)

    def __solve_r(self, x, y):
        # Recursive function to solve the maze
        self.__animate()
        # mark the current cell as visited
        self.cells[x][y].visited = True
        # check if we're at the end of the maze
        if x == self.num_cols - 1 and y == self.num_rows - 1:
            self.is_solved = True
            return True
        # check if neighbors exist, are unvisited, and can be moved to (no wall facing that neighbor and that neighbor has no wall facing current cell)
        if (
            x - 1 >= 0
            and not self.cells[x - 1][y].visited
            and not self.cells[x][y].has_left_wall
            and not self.cells[x - 1][y].has_right_wall
        ):
            self.cells[x][y].draw_move(self.cells[x - 1][y])
            if self.__solve_r(x - 1, y):
                return True
            else:
                self.cells[x][y].draw_move(self.cells[x - 1][y], True)
        if (
            x + 1 < self.num_cols
            and not self.cells[x + 1][y].visited
            and not self.cells[x][y].has_right_wall
            and not self.cells[x + 1][y].has_left_wall
        ):
            self.cells[x][y].draw_move(self.cells[x + 1][y])
            if self.__solve_r(x + 1, y):
                return True
            else:
                self.cells[x][y].draw_move(self.cells[x + 1][y], True)
        if (
            y - 1 >= 0
            and not self.cells[x][y - 1].visited
            and not self.cells[x][y].has_top_wall
            and not self.cells[x][y - 1].has_bottom_wall
        ):
            self.cells[x][y].draw_move(self.cells[x][y - 1])
            if self.__solve_r(x, y - 1):
                return True
            else:
                self.cells[x][y].draw_move(self.cells[x][y - 1], True)
        if (
            y + 1 < self.num_rows
            and not self.cells[x][y + 1].visited
            and not self.cells[x][y].has_bottom_wall
            and not self.cells[x][y + 1].has_top_wall
        ):
            self.cells[x][y].draw_move(self.cells[x][y + 1])
            if self.__solve_r(x, y + 1):
                return True
            else:
                self.cells[x][y].draw_move(self.cells[x][y + 1], True)
        return False


if __name__ == "__main__":
    pass
