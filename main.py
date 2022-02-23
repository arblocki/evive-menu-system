#!/usr/bin/env python3
"""
Menu Ordering System 
"""
import sys
from menu import Menu
from course import Breakfast, Lunch, Dinner


def main():
    """ Process order using Menu """
    menu = Menu()
    menu.addCourse('Breakfast', Breakfast())
    menu.addCourse('Lunch', Lunch()) 
    menu.addCourse('Dinner', Dinner())
    menu.pollForOrders()


if __name__ == "__main__":
    """ Execute main when run from the command line """
    main()
