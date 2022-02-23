
from dataclasses import dataclass
from enum import Enum


class Order():
    """
    Track quantities by item and type for quick reference
    """

    def __init__(self):
        """ Initialize order with empty map for items and list of zeroes for types """
        self.itemQuantities = {}
        # Track quantities of each ItemType as we add items
        self.typeQuantities = [0] * len(ItemType)
    
    def addItem(self, item):
        """ Update quantities accordingly """
        if item.id not in self.itemQuantities:
            self.itemQuantities[item.id] = 1
        else:
            self.itemQuantities[item.id] += 1
        self.typeQuantities[item.type.value] += 1

    def getQuantityByType(self, itemType):
        """ Return quantity of items with a certain type """
        return self.typeQuantities[itemType.value]
    
    def getQuantityByID(self, itemID):
        """ Return quantity of a specific item """
        if itemID not in self.itemQuantities:
            return 0
        return self.itemQuantities[itemID]
    
    def getItemIDList(self):
        """ Return list of item IDs in order """
        return list(self.itemQuantities.keys())


class ItemType(Enum):
    """ Enumerated item types """
    MAIN = 0
    SIDE = 1
    DRINK = 2
    DESSERT = 3


@dataclass
class MenuItem:
    """ Dataclass for items in a Course """
    id: int
    name: str 
    type: ItemType
