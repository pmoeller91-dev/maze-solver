import unittest
from maze import Maze


class TestMaze(unittest.TestCase):
    def test_maze_create_cells(self):
        num_cols = 12
        num_rows = 10
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        self.assertEqual(len(m1._cells), num_cols)
        self.assertEqual(len(m1._cells[0]), num_rows)

    def test_maze_create_cells_many(self):
        num_cols = 120
        num_rows = 100
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        self.assertEqual(len(m1._cells), num_cols)
        self.assertEqual(len(m1._cells[0]), num_rows)

    def test_maze_init_zero_cells(self):
        num_cols = 0
        num_rows = 0
        self.assertRaises(ValueError, lambda: Maze(0, 0, num_rows, num_cols, 10, 10))

    def test_maze_init_zero_size(self):
        num_cols = 12
        num_rows = 10
        width = 0
        height = 0
        self.assertRaises(
            ValueError, lambda: Maze(0, 0, num_rows, num_cols, width, height)
        )

    def test_break_entrance_and_exit(self):
        maze = Maze(0, 0, 10, 10, 10, 10)
        maze._break_entrance_and_exit()
        self.assertEqual(maze._cells[0][0].has_top_wall, False)
        self.assertEqual(maze._cells[-1][-1].has_bottom_wall, False)

    def test_break_entrance_and_exit_single_cell(self):
        maze = Maze(0, 0, 1, 1, 10, 10)
        maze._break_entrance_and_exit()
        self.assertEqual(maze._cells[0][0].has_top_wall, False)
        self.assertEqual(maze._cells[0][0].has_bottom_wall, False)


if __name__ == "__main__":
    unittest.main()
