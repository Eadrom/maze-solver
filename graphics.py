#!/usr/bin/env python

from tkinter import Tk, BOTH, Canvas

class Window():
    def __init__(self, width, height):
        self.__root = Tk()
        self.__root.title("Maze Solver")
        self.__root.protocol("WM_DELETE_WINDOW", self.close)
        self.__root.resizable(0, 0)
        self.canvas = Canvas(self.__root, width=width, height=height)
        self.canvas.pack(fill=BOTH, expand=1)
        self.window_is_running = False


    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()
    

    def wait_for_close(self):
        self.window_is_running = True
        while self.window_is_running is True:
            self.redraw()
        

    def close(self):
        self.window_is_running = False


def main():
    pass

if __name__ == "__main__":
    main()
