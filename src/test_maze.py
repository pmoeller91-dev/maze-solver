import unittest
from maze import Maze, Direction


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

    def test_get_visitable_cells_all_directions(self):
        maze = Maze(0, 0, 10, 12, 10, 10)
        target_cell = (1, 1)
        expected_visitable_cells = [
            (Direction.UP, 1, 0),
            (Direction.RIGHT, 2, 1),
            (Direction.DOWN, 1, 2),
            (Direction.LEFT, 0, 1),
        ]
        visitable_cells = maze._get_visitable_cells(*target_cell)
        self.assertEqual(visitable_cells, expected_visitable_cells)

    # Should not wrap around or include invalid cells
    def test_get_visitable_cells_close_corner(self):
        maze = Maze(0, 0, 10, 12, 10, 10)
        target_cell = (0, 0)
        expected_visitable_cells = [
            (Direction.RIGHT, 1, 0),
            (Direction.DOWN, 0, 1),
        ]
        visitable_cells = maze._get_visitable_cells(*target_cell)
        self.assertEqual(visitable_cells, expected_visitable_cells)

    def test_get_visitable_cells_far_corner(self):
        maze = Maze(0, 0, 10, 12, 10, 10)
        target_cell = (11, 9)
        expected_visitable_cells = [
            (Direction.UP, 11, 8),
            (Direction.LEFT, 10, 9),
        ]
        visitable_cells = maze._get_visitable_cells(*target_cell)
        self.assertEqual(visitable_cells, expected_visitable_cells)

    # should not included visited cells
    def test_get_visitable_cells_visited(self):
        maze = Maze(0, 0, 10, 12, 10, 10)
        target_cell = (1, 1)
        maze._cells[0][1].visited = True
        maze._cells[2][1].visited = True
        expected_visitable_cells = [
            (Direction.UP, 1, 0),
            (Direction.DOWN, 1, 2),
        ]
        visitable_cells = maze._get_visitable_cells(*target_cell)
        self.assertEqual(visitable_cells, expected_visitable_cells)

    def test_get_visitable_cells_all_visited(self):
        maze = Maze(0, 0, 10, 12, 10, 10)
        target_cell = (1, 1)
        maze._cells[1][0].visited = True
        maze._cells[1][2].visited = True
        maze._cells[0][1].visited = True
        maze._cells[2][1].visited = True
        expected_visitable_cells = []
        visitable_cells = maze._get_visitable_cells(*target_cell)
        self.assertEqual(visitable_cells, expected_visitable_cells)

    def test_get_visitable_cells_out_of_bounds_low(self):
        maze = Maze(0, 0, 10, 12, 10, 10)
        target_cell = (-1, -1)
        self.assertRaises(ValueError, maze._get_visitable_cells, *target_cell)

    def test_get_visitable_cells_out_of_bounds_high(self):
        maze = Maze(0, 0, 10, 12, 10, 10)
        target_cell = (12, 10)
        self.assertRaises(ValueError, maze._get_visitable_cells, *target_cell)

    def test_break_walls_r_right(self):
        maze = Maze(0, 0, 1, 2, 10, 10, seed=0)
        maze._break_cells_r(0, 0)
        self.assertEqual(maze._cells[0][0].has_right_wall, False)
        self.assertEqual(maze._cells[1][0].has_left_wall, False)

    def test_break_walls_r_left(self):
        maze = Maze(0, 0, 1, 2, 10, 10, seed=0)
        maze._break_cells_r(1, 0)
        self.assertEqual(maze._cells[0][0].has_right_wall, False)
        self.assertEqual(maze._cells[1][0].has_left_wall, False)

    def test_break_walls_r_down(self):
        maze = Maze(0, 0, 2, 1, 10, 10, seed=0)
        maze._break_cells_r(0, 0)
        self.assertEqual(maze._cells[0][0].has_bottom_wall, False)
        self.assertEqual(maze._cells[0][1].has_top_wall, False)

    def test_break_walls_r_up(self):
        maze = Maze(0, 0, 2, 1, 10, 10, seed=0)
        maze._break_cells_r(0, 1)
        self.assertEqual(maze._cells[0][0].has_bottom_wall, False)
        self.assertEqual(maze._cells[0][1].has_top_wall, False)

    def test_break_walls_r_visit_all(self):
        maze = Maze(0, 0, 10, 10, 10, 10, seed=0)
        maze._break_cells_r(0, 0)
        expected_cells_visited = [[True] * len(col) for col in maze._cells]
        cells_visited = [[row.visited for row in col] for col in maze._cells]
        self.assertEqual(cells_visited, expected_cells_visited)


if __name__ == "__main__":
    unittest.main()
