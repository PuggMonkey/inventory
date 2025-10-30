from enum import Enum

class Page(Enum):
    """Enumeration for different pages in the application."""
    LOGIN = 1
    MAIN = 2
    INVENTORY = 3
    ACCOUNT_MANAGEMENT = 4
    VIEW_INVENTORY = 5
    EDIT_INVENTORY = 6
    CREATE_ITEM = 7
    EDIT_ITEM = 8
    CREATE_USER = 9
