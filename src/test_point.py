import unittest
from point import Point


class TestPoint(unittest.TestCase):
    def test_eq_self(self):
        point = Point(1, 1)
        self.assertTrue(point == point)

    def test_eq_other(self):
        point = Point(1, 1)
        point2 = Point(1, 1)
        self.assertTrue(point == point2)

    def test_eq_not_eq(self):
        point = Point(1, 1)
        point2 = Point(1, 2)
        self.assertTrue(point != point2)

    def test_add(self):
        point = Point(1, 1)
        point2 = Point(2, 2)
        expected_point = Point(3, 3)
        self.assertEqual(point + point2, expected_point)

    def test_sub(self):
        point = Point(1, 1)
        point2 = Point(2, 2)
        expected_point = Point(-1, -1)
        self.assertEqual(point - point2, expected_point)

    def test_rsub(self):
        point = Point(1, 1)
        point2 = Point(2, 2)
        expected_point = Point(1, 1)
        self.assertEqual(point.__rsub__(point2), expected_point)

    def test_mul(self):
        point = Point(1, 2)
        multiplier = 2
        expected_point = Point(2, 4)
        self.assertEqual(point * multiplier, expected_point)

    def test_rmul(self):
        point = Point(3, 6)
        multiplier = 3
        expected_point = Point(9, 18)
        self.assertEqual(multiplier * point, expected_point)

    def test_truediv(self):
        point = Point(3, 6)
        divisor = 3
        expected_point = Point(1, 2)
        self.assertEqual(point / divisor, expected_point)

    def test_floordiv(self):
        point = Point(3, 9)
        divisor = 2
        expected_point = Point(1, 4)
        self.assertEqual(point // divisor, expected_point)

    def test_neg(self):
        point = Point(1, 1)
        expected_point = Point(-1, -1)
        self.assertEqual(-point, expected_point)

    def test_repr(self):
        point = Point(10, 10)
        expected_repr = "Point(x=10, y=10)"
        self.assertEqual(f"{point}", expected_repr)


if __name__ == "__main__":
    unittest.main()
