#!/usr/bin/env python

import unittest
from graphics import Maze


class Tests(unittest.TestCase):
    def test_maze_create_cells(self):
        # Test if the Maze class creates cells with the correct dimensions
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
        # Test if Maze cells have the expected properties
        num_cols = 5
        num_rows = 3
        cell_size = 15
        m2 = Maze(0, 0, num_rows, num_cols, cell_size, cell_size)

        for col in m2.cells:
            for cell in col:
                self.assertTrue(cell.has_left_wall or cell.has_right_wall)
                self.assertTrue(cell.has_top_wall or cell.has_bottom_wall)

    def test_maze_animate(self):
        # Test if calling animate method does not raise an exception
        num_cols = 8
        num_rows = 6
        cell_size = 20
        win = None  # No window provided for testing
        m3 = Maze(0, 0, num_rows, num_cols, cell_size, cell_size, win)
        m3._Maze__animate()

    def test_maze_break_entrance_exit(self):
        # Test if entrance and exit walls are broken correctly
        num_cols = 10
        num_rows = 8
        cell_size = 15
        m4 = Maze(0, 0, num_rows, num_cols, cell_size, cell_size, None)

        m4._Maze__break_entrance_and_exit()

        self.assertFalse(m4.cells[0][0].has_top_wall)
        self.assertTrue(m4.cells[0][0].has_bottom_wall)
        self.assertTrue(m4.cells[num_cols - 1][num_rows - 1].has_top_wall)
        self.assertFalse(m4.cells[num_cols - 1][num_rows - 1].has_bottom_wall)

    def test_reset_visited_state(self):
        # Test if the visited state is reset for all cells
        num_cols = 8
        num_rows = 6
        cell_size = 20
        win = None  # No window provided for testing
        m = Maze(0, 0, num_rows, num_cols, cell_size, cell_size, win)

        # Set the visited state of some cells to True
        m.cells[1][1].visited = True
        m.cells[2][3].visited = True
        m.cells[5][4].visited = True

        # Reset the visited state
        m._Maze__reset_visited_state()

        # Check if the visited state is reset for all cells
        for col in m.cells:
            for cell in col:
                self.assertFalse(cell.visited)


if __name__ == "__main__":
    unittest.main()
