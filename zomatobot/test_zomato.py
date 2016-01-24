import datetime as dt
import unittest

from zomatobot import zomato


class TestFixYear(unittest.TestCase):
    def test_next_year(self):
        print('TestFixYear.test_next_year')
        today = dt.date(2015, 12, 28)
        date = dt.date(1980, 1, 3)

        expected = dt.date(2016, 1, 3)
        actual = zomato._fix_year(date, today)

        self.assertEqual(actual, expected, "Menu to be served after new year")

    def test_last_year(self):
        print('TestFixYear.test_last_year')
        print("")
        today = dt.date(2016, 1, 3)
        date = dt.date(1980, 12, 28)

        actual = zomato._fix_year(date, today)
        expected = dt.date(2015, 12, 28)

        self.assertEqual(actual, expected, "Menu which was served before new year")


if __name__ == '__main__':
    unittest.main()
