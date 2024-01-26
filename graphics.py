#!/usr/bin/env python

from tkinter import Tk, BOTH, Canvas
import time, random


class Window:
    def __init__(self, width, height):
        self.__root = Tk()
        self.__root.title("Maze Solver")
        self.__root.protocol("WM_DELETE_WINDOW", self.close)
        self.__root.resizable(0, 0)
        self.__canvas = Canvas(self.__root, width=width, height=height, bg="white")
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
    def __init__(self, start_point, end_point, color="black"):
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
    def __init__(self, tl_point, br_point, window=None):
        self.top_left_point = tl_point
        self.bottom_right_point = br_point
        self.__window = window
        self.has_left_wall = True
        self.has_top_wall = True
        self.has_right_wall = True
        self.has_bottom_wall = True
        self.visited = False

    def draw(self):
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
        win=None,
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
        for l in range(0, self.num_cols):
            for w in range(0, self.num_rows):
                self.cells[l][w].draw()
                self.__animate()
        self.__break_entrance_and_exit()
        self.__animate()
        self.__break_walls_r(0, 0)
        self.__reset_visited_state()

    def __animate(self):
        if self.win is not None:
            self.win.redraw()
            time.sleep(0.01)

    def __break_entrance_and_exit(self):
        self.cells[0][0].has_top_wall = False
        self.cells[self.num_cols - 1][self.num_rows - 1].has_bottom_wall = False

        if self.win is not None:
            self.cells[0][0].draw()
            self.cells[self.num_cols - 1][self.num_rows - 1].draw()

    def __break_walls_r(self, x, y):
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
        for x in range(0, self.num_cols):
            for y in range(0, self.num_rows):
                self.cells[x][y].visited = False


def main():
    pass


if __name__ == "__main__":
    main()
