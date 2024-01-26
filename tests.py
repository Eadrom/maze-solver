#!/usr/bin/env python

import unittest
from graphics import Maze


class Tests(unittest.TestCase):
    def test_maze_create_cells(self):
        num_cols = 12
        num_rows = 10
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        self.assertEqual(
            len(m1.cells),
            num_cols,
        )
        self.assertEqual(
            len(m1.cells[0]),
            num_rows,
        )

    def test_maze_cell_properties(self):
        num_cols = 5
        num_rows = 3
        cell_size = 15
        m2 = Maze(0, 0, num_rows, num_cols, cell_size, cell_size)

        # Check if all cells have the expected properties
        for col in m2.cells:
            for cell in col:
                self.assertTrue(cell.has_left_wall or cell.has_right_wall)
                self.assertTrue(cell.has_top_wall or cell.has_bottom_wall)

    def test_maze_animate(self):
        num_cols = 8
        num_rows = 6
        cell_size = 20
        win = None  # No window provided for testing
        m3 = Maze(0, 0, num_rows, num_cols, cell_size, cell_size, win)

        # Ensure calling animate method does not raise an exception
        m3._Maze__animate()


if __name__ == "__main__":
    unittest.main()
