
from abc import ABC
from order import Order, ItemType, MenuItem


class Course(ABC):
    """
    Processes lists of item IDs into orders
    Checks for malformed orders

    Abstract base class with subclasses for each course (Breakfast, Lunch, Dinner)
    """

    def __init__(self):
        """ Initialize course with item list and a blank order """
        self.items = {
            0: MenuItem(0, 'Water', ItemType.DRINK)
        }
        self.order = Order()

    def processOrder(self, itemIDList):
        """ Reset order variable and pass onto subclass implementation """
        self.order = Order()
        self.processOrderItems(itemIDList)
    
    def processOrderItems(self, itemIDList):
        """ 
        Process item list and return Order 
        Add water if necessary and check for generic errors
        """
        self.addItemIDsToOrder(itemIDList)
        # If no drinks were given, add water
        if self.order.getQuantityByType(ItemType.DRINK) == 0:
            self.addItemToOrder(0)
        self.checkForErrors()
        return self.order
    
    def addItemIDsToOrder(self, itemIDList):
        """ Add each ID in itemIDList to order """
        for itemID in itemIDList:
            self.addItemToOrder(itemID)

    def addItemToOrder(self, itemID):
        """ Check if item exists in course, then add to order """
        if itemID not in self.items:
            raise ValueError(f'Invalid ID {itemID} given in order')
        newItem = self.items[itemID]
        self.order.addItem(newItem)
    
    def checkForErrors(self):
        """ Check for errors generic to all orders """
        mainMissing = self.order.getQuantityByType(ItemType.MAIN) == 0
        sideMissing = self.order.getQuantityByType(ItemType.SIDE) == 0
        if mainMissing and sideMissing:
            raise ValueError('Main is missing, side is missing')
        elif mainMissing:
            raise ValueError('Main is missing')
        elif sideMissing:
            raise ValueError('Side is missing')

    def orderToString(self):
        """ Print order items with quantities """
        orderItemStrList = []
        orderItemIDList = self.order.getItemIDList()
        # Sort items by type and ID
        sortedOrderItemIDList = self.sortOrder(orderItemIDList)
        for itemID in sortedOrderItemIDList:
            itemName = self.items[itemID].name
            itemQty = self.order.getQuantityByID(itemID)
            if itemQty == 1:
                orderItemStrList.append(itemName)
            else:
                orderItemStrList.append(f'{itemName}({itemQty})')
        orderStr = ', '.join(orderItemStrList)
        return orderStr

    def sortOrder(self, itemIDList):
        """ Sort items in order by type, then ID """
        menuItemList = [self.items[id] for id in itemIDList]
        # Sort by ItemType, then id
        menuItemList.sort(key=lambda item: (item.type.value, item.id))
        # Move water behind other drinks if it is in the list and there are other drinks
        if 0 in itemIDList and self.order.getQuantityByType(ItemType.DRINK) > 1:
            menuItemList = self.moveWaterBack(menuItemList)
        # Return list of ids
        finalIDList = [item.id for item in menuItemList]
        return finalIDList

    def moveWaterBack(self, menuItemList):
        """ Handle case where water (ID 0) gets sorted behind other beverages """
        # Get indices of all drinks
        drinkIndices = [index for index, element in enumerate(menuItemList) if element.type == ItemType.DRINK]
        if len(drinkIndices) < 2: 
            return menuItemList
        # Move element at first index (water) to last index, shift other elements forward by 1
        firstIndex = drinkIndices[0]
        lastIndex = drinkIndices[-1]
        firstElem = menuItemList[firstIndex]
        menuItemList[firstIndex:lastIndex] = menuItemList[firstIndex+1:lastIndex+1]
        menuItemList[lastIndex] = firstElem
        return menuItemList


class Breakfast(Course):
    def __init__(self):
        """ Initialize with water and breakfast items """
        super().__init__()
        self.items[1] = MenuItem(1, 'Eggs', ItemType.MAIN)
        self.items[2] = MenuItem(2, 'Toast', ItemType.SIDE)
        self.items[3] = MenuItem(3, 'Coffee', ItemType.DRINK)

    def checkForErrors(self):
        """ Check for breakfast-specific errors """
        super().checkForErrors()
        # The only item with quantity > 1 should be coffee
        for itemID in self.items.keys():
            if self.order.getQuantityByID(itemID) > 1 and itemID != 3:
                raise ValueError(f'{self.items[itemID].name} cannot be ordered more than once')


class Lunch(Course):
    def __init__(self):
        """ Initialize with water and lunch items """
        super().__init__()
        self.items[1] = MenuItem(1, 'Sandwich', ItemType.MAIN)
        self.items[2] = MenuItem(2, 'Chips', ItemType.SIDE)
        self.items[3] = MenuItem(3, 'Soda', ItemType.DRINK)

    def checkForErrors(self):
        """ Check for lunch-specific errors """
        super().checkForErrors()
        # The only item with quantity > 1 should be sides
        for itemID in self.items.keys():
            if self.order.getQuantityByID(itemID) > 1 and self.items[itemID].type != ItemType.SIDE:
                raise ValueError(f'{self.items[itemID].name} cannot be ordered more than once')
        # The only item category with quantity > 1 should be sides
        for type in ItemType:
            if self.order.getQuantityByType(type) > 1 and type != ItemType.SIDE:
                raise ValueError(f'{type} cannot be ordered more than once')


class Dinner(Course):
    def __init__(self):
        """ Initialize with water and breakfast items """
        super().__init__()
        self.items[1] = MenuItem(1, 'Steak', ItemType.MAIN)
        self.items[2] = MenuItem(2, 'Potatoes', ItemType.SIDE)
        self.items[3] = MenuItem(3, 'Wine', ItemType.DRINK)
        self.items[4] = MenuItem(4, 'Cake', ItemType.DESSERT)

    def processOrderItems(self, itemIDList):
        """ Add water to dinner orders before calling parent functionality """
        self.addItemToOrder(0)
        super().processOrderItems(itemIDList)

    def checkForErrors(self):
        """ Check for dinner-specific errors """
        super().checkForErrors()
        # No dinner item should be ordered more than once
        for itemID in self.items.keys():
            if self.order.getQuantityByID(itemID) > 1:
                raise ValueError(f'{self.items[itemID].name} cannot be ordered more than once')
        # Dessert must be ordered with dinner 
        if self.order.getQuantityByType(ItemType.DESSERT) == 0:
            raise ValueError('Dessert is missing')
