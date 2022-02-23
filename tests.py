"""
This file performs unit tests on all classes, and full
acceptance testing on the menu ordering system as a whole
"""
import unittest
from menu import Menu
from course import Breakfast, Lunch, Dinner


class AcceptanceTests(unittest.TestCase):
    """ Acceptance tests  """

    def setUp(self):
        self.menu = Menu()
        self.menu.addCourse('Breakfast', Breakfast())
        self.menu.addCourse('Lunch', Lunch())
        self.menu.addCourse('Dinner', Dinner())

    def test_valid_breakfast(self):
        """ Test properly formatted breakfast orders """
        self.setUp()
        self.assertEqual(self.menu.processOrder('Breakfast 1,2,3'), 'Eggs, Toast, Coffee')
        self.assertEqual(self.menu.processOrder('Breakfast 2,3,1'), 'Eggs, Toast, Coffee')
        self.assertEqual(self.menu.processOrder('Breakfast 1,2,3,3,3'), 'Eggs, Toast, Coffee(3)')
        self.assertEqual(self.menu.processOrder('Breakfast 2,1'), 'Eggs, Toast, Water')

    def test_invalid_breakfast(self):
        """ Test invalid breakfast orders """
        self.setUp()
        self.assertEqual(self.menu.processOrder('Breakfast 1'), 'Unable to process: Side is missing')
        self.assertEqual(self.menu.processOrder('Breakfast 1,1,2'), 'Unable to process: Eggs cannot be ordered more than once')

    def test_valid_lunch(self):
        """ Test properly formatted lunch orders """
        self.setUp()
        self.assertEqual(self.menu.processOrder('Lunch 1,2,3'), 'Sandwich, Chips, Soda')
        self.assertEqual(self.menu.processOrder('Lunch 1,2'), 'Sandwich, Chips, Water')
        self.assertEqual(self.menu.processOrder('Lunch 1,2,2'), 'Sandwich, Chips(2), Water')
        self.assertEqual(self.menu.processOrder('Lunch 2,2,3,1,2'), 'Sandwich, Chips(3), Soda')

    def test_invalid_lunch(self):
        """ Test invalid lunch orders """
        self.setUp()
        self.assertEqual(self.menu.processOrder('Lunch 1,1,2,3'), 'Unable to process: Sandwich cannot be ordered more than once')
        self.assertEqual(self.menu.processOrder('Lunch '), 'Unable to process: Main is missing, side is missing')
        self.assertEqual(self.menu.processOrder('Lunch 1,3,2,3'), 'Unable to process: Soda cannot be ordered more than once')

    def test_valid_dinner(self):
        """ Test properly formatted dinner orders """
        self.setUp()
        self.assertEqual(self.menu.processOrder('Dinner 1,2,3,4'), 'Steak, Potatoes, Wine, Water, Cake')
        self.assertEqual(self.menu.processOrder('Dinner 1,2,4'), 'Steak, Potatoes, Water, Cake')

    def test_invalid_dinner(self):
        """ Test invalid dinner orders """
        self.setUp()
        self.assertEqual(self.menu.processOrder('Dinner 1,2,3'), 'Unable to process: Dessert is missing')
        self.assertEqual(self.menu.processOrder('Dinner 1'), 'Unable to process: Side is missing')

    def test_invalid_input(self):
        """ Test malformed input """
        self.setUp()
        self.assertEqual(self.menu.processOrder('Snack 1,2'), 'Unable to process: Invalid course \'Snack\' given in order')
        self.assertEqual(self.menu.processOrder('Breakfast 1,2a'), 'Unable to process: Invalid ID \'2a\' given in order')


if __name__ == '__main__':
    unittest.main()
