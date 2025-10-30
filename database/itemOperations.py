import sqlite3
from classes.item import Item

class ItemOperations:
    """Class to handle item operations in the database."""
    def __init__(self, cursor: sqlite3.Cursor, connection: sqlite3.Connection):
        self.cursor = cursor
        self.connection = connection
    
    def add_item(self, name: str, category: int, quantity: int = 0, defective_quantity: int = 0) -> None:
        """Add a new item to the Items table."""
        self.cursor.execute("""
        INSERT INTO Items (name, category, quantity, defective_quantity)
        VALUES (?, ?, ?, ?);
        """, (name, category, quantity, defective_quantity))
        self.connection.commit()

    def delete_item(self, item_id: int) -> None:
        """Delete an item from the Items table by ID."""
        self.cursor.execute("""
        DELETE FROM Items
        WHERE id = ?;
        """, (item_id,))
        self.connection.commit()

    def update_item(self, item_id: int, name: str, category: int, quantity: int, defective_quantity: int) -> None:
        """Update an existing item in the Items table."""
        self.cursor.execute("""
        UPDATE Items
        SET name = ?, category = ?, quantity = ?, defective_quantity = ?
        WHERE id = ?;
        """, (name, category, quantity, defective_quantity, item_id))
        self.connection.commit()

    def get_item(self, item_id: int) -> Item | None:
        """Retrieve an item from the Items table by ID."""
        self.cursor.execute("""
        SELECT * FROM Items
        WHERE id = ?;
        """, (item_id,))
        row = self.cursor.fetchone()
        if row:
            return Item(id=row[0], name=row[1], category=row[2], quantity=row[3], defective_quantity=row[4])
        return 
    
    def get_all_items(self) -> list[Item] | None:
        """Retrieve all items from the Items table."""
        self.cursor.execute("""
        SELECT * FROM Items;
        """)
        rows = self.cursor.fetchall()
        if rows:
            return [Item(id=row[0], name=row[1], category=row[2], quantity=row[3], defective_quantity=row[4]) for row in rows]
        return 
