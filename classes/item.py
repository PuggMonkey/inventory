from enums.category import Category
class Item:
    """
Item class represents an item in the inventory.

An item has a name, a category and a quantity. The quantity can be increased or decreased.

The quantity of an item must be non-negative.

The item also keeps track of the number of defective items of that type.
"""
    def __init__(self,id: int, name: str, category: Category, quantity: int, defective_quantity: int = 0):
        from database.databaseService import db
        if quantity < 0 or defective_quantity < 0:
            raise ValueError("Quantity and defective quantity must be non-negative")
        
        self.id = id
        self.name = name
        self.category = category
        self.quantity = quantity
        self.defective_quantity = defective_quantity
        self.db = db
    
    def _update_db(self) -> None:
        """Update the item in the database"""
        self.db.items.update_item(
            self.id,
            self.name,
            self.category,
            self.quantity,
            self.defective_quantity
        )

    def increase_quantity(self, amount: int) -> None:
        """Increase the quantity of the item by the specified amount"""
        self.quantity += amount
        self._update_db()

    def decrease_quantity(self, amount: int) -> None:
        """Decrease the quantity of the item by the specified amount"""
        if amount <= self.quantity:
            self.quantity -= amount
            self._update_db()
        else:
            raise ValueError("Cannot decrease quantity below zero")
        
    def mark_defective(self, amount: int) -> None:
        """Mark a certain amount of items as defective"""
        if amount <= self.quantity:
            self.quantity -= amount
            self.defective_quantity += amount
            self._update_db()
        else:
            raise ValueError("Cannot mark more items as defective than available quantity")
    
    def repair_defective(self, amount: int) -> None:
        """Repair a certain amount of defective items"""
        if amount <= self.defective_quantity:
            self.defective_quantity -= amount
            self.quantity += amount
            self._update_db()
        else:
            raise ValueError("Cannot repair more defective items than available defective quantity")
