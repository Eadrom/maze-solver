#!/usr/bin/env python

from tkinter import Tk, BOTH, Canvas

class Window():
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

class Point():
    def __init__(self, x, y):
        # x = 0 is the left side of the window
        # y = 0 is the top side of the window
        self.x = x
        self.y = y

class Line():
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
            width=2)
        canvas.pack(fill=BOTH, expand=1)

class Cell():
    def __init__(self, window, tl_point, br_point):
        self.__top_left_point = tl_point
        self.__bottom_right_point = br_point
        self.__window = window
        self.has_left_wall = True
        self.has_top_wall = True
        self.has_right_wall = True
        self.has_bottom_wall = True

    def draw(self):
        if self.has_left_wall:
            line = Line(
                Point(self.__top_left_point.x, self.__top_left_point.y),
                Point(self.__top_left_point.x, self.__bottom_right_point.y)
            )
            self.__window.draw_line(line)

        if self.has_top_wall:
            line = Line(
                Point(self.__top_left_point.x, self.__top_left_point.y),
                Point(self.__bottom_right_point.x, self.__top_left_point.y)
            )
            self.__window.draw_line(line)

        if self.has_right_wall:
            line = Line(
                Point(self.__bottom_right_point.x, self.__top_left_point.y),
                Point(self.__bottom_right_point.x, self.__bottom_right_point.y)
            )
            self.__window.draw_line(line)
            
        if self.has_bottom_wall:
            line = Line(
                Point(self.__top_left_point.x, self.__bottom_right_point.y),
                Point(self.__bottom_right_point.x, self.__bottom_right_point.y)
            )
            self.__window.draw_line(line)
            
def main():
    pass

if __name__ == "__main__":
    main()
