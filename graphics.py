#!/usr/bin/env python

from tkinter import Tk, BOTH, Canvas
import time


class Window:
    def __init__(self, width, height):
        self.__root = Tk()
        self.__root.title("Maze Solver")
        self.__root.protocol("WM_DELETE_WINDOW", self.close)
        self.__root.resizable(0, 0)
        self.__canvas = Canvas(self.__root, width=width, height=height)
        self.__canvas.pack(fill=BOTH, expand=1)
        self.__window_is_running = False

    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()

    def draw_line(self, line, color=None):
        line.draw(self.__canvas, color)

    def wait_for_close(self):
        self.__window_is_running = True
        while self.__window_is_running is True:
            self.redraw()

    def close(self):
        self.__window_is_running = False


class Point:
    def __init__(self, x, y):
        # x = 0 is the left side of the window
        # y = 0 is the top side of the window
        self.x = x
        self.y = y


class Line:
    def __init__(self, start_point, end_point):
        self.start_point = start_point
        self.end_point = end_point

    def draw(self, canvas, color="black"):
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
    def __init__(self, window, tl_point, br_point):
        self.top_left_point = tl_point
        self.bottom_right_point = br_point
        self.__window = window
        self.has_left_wall = True
        self.has_top_wall = True
        self.has_right_wall = True
        self.has_bottom_wall = True

    def draw(self):
        if self.has_left_wall:
            line = Line(
                Point(self.top_left_point.x, self.top_left_point.y),
                Point(self.top_left_point.x, self.bottom_right_point.y),
            )
            self.__window.draw_line(line)

        if self.has_top_wall:
            line = Line(
                Point(self.top_left_point.x, self.top_left_point.y),
                Point(self.bottom_right_point.x, self.top_left_point.y),
            )
            self.__window.draw_line(line)

        if self.has_right_wall:
            line = Line(
                Point(self.bottom_right_point.x, self.top_left_point.y),
                Point(self.bottom_right_point.x, self.bottom_right_point.y),
            )
            self.__window.draw_line(line)

        if self.has_bottom_wall:
            line = Line(
                Point(self.top_left_point.x, self.bottom_right_point.y),
                Point(self.bottom_right_point.x, self.bottom_right_point.y),
            )
            self.__window.draw_line(line)

    def draw_move(self, target_cell, undo=False):
        if undo is False:
            line_color = "red"
        else:
            line_color = "gray"

        self.center = Point(
            self.top_left_point.x
            + (self.bottom_right_point.x - self.top_left_point.x) / 2,
            self.top_left_point.y
            + (self.bottom_right_point.y - self.top_left_point.y) / 2,
        )

        target_cell_center = Point(
            target_cell.top_left_point.x
            + (target_cell.bottom_right_point.x - target_cell.top_left_point.x) / 2,
            target_cell.top_left_point.y
            + (target_cell.bottom_right_point.y - target_cell.top_left_point.y) / 2,
        )

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
        win,
    ):
        self.x1 = x1
        self.y1 = y1
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self.win = win
        self.cells = []
        self.__create_cells()

    def __create_cells(self):
        for l in range(0, self.num_cols):
            self.cells.append([])
            for w in range(0, self.num_rows):
                self.cells[l].append(
                    Cell(
                        self.win,
                        Point(
                            self.x1 + l * self.cell_size_x,
                            self.y1 + w * self.cell_size_y,
                        ),
                        Point(
                            self.x1 + l * self.cell_size_x + self.cell_size_x,
                            self.y1 + w * self.cell_size_y + self.cell_size_y,
                        ),
                    )
                )
        self.__draw_cells()

    def __draw_cells(self):
        for l in range(0, self.num_cols):
            for w in range(0, self.num_rows):
                self.cells[l][w].draw()
                self.__animate()

    def __animate(self):
        self.win.redraw()
        time.sleep(0.01)


def main():
    pass


if __name__ == "__main__":
    main()
