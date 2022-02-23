
import sys
from course import Course


class Menu:
    """ 
    Handles user input of orders
    Processes user orders by calling appropriate Course object method
    """
    
    def __init__(self):
        """ Initialize Menu with empty dict of Courses """
        self.courses = {}

    def addCourse(self, courseName, courseObj):
        """ Add course with given name and instance to dict """
        if courseName in self.courses:
            raise ValueError(f'Duplicate course name added to menu: \'{courseName}\' course already exists')
        self.courses[courseName] = courseObj

    def pollForOrders(self):
        """ Poll stdin for order strings, stop on 'q' or end-of-file """
        while True:
            try:
                order = input('Enter your order: ')
            except EOFError:
                break
            if order == 'q':
                break
            orderStr = self.processOrder(order)
            print(orderStr)

    def processOrder(self, order):
        """ Process full string order (e.g. 'Breakfast 1,2,3' ) """
        order = order.strip()
        try:
            [courseName, itemListStr] = order.split(' ', 1)
        except ValueError:
            # Handle case of no ids given
            return 'Unable to process: Main is missing, side is missing'
        itemIDStrList = itemListStr.split(',')
        try:
            itemIDList = [Menu.strToIntFunctor(id) for id in itemIDStrList]
            if courseName not in self.courses:
                raise ValueError(f'Invalid course \'{courseName}\' given in order')
            orderCourse = self.courses[courseName]
            orderCourse.processOrder(itemIDList)
            return orderCourse.orderToString()
        except ValueError as err:
            return f'Unable to process: {err}'

    @staticmethod
    def strToIntFunctor(id):
        """ Convert str to int, raise error if not a digit """
        if id.isdigit():
            return int(id)
        else:
            raise ValueError(f'Invalid ID \'{id}\' given in order')