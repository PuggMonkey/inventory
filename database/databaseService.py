import sqlite3
from database.itemOperations import ItemOperations
from database.accountOperations import AccountOperations


class DatabaseService:
    """Service to manage database connections and operations."""
    connection: sqlite3.Connection
    cursor: sqlite3.Cursor
    items: ItemOperations
    accounts: AccountOperations
    database_file: str

    def __init__(self, database_file: str):
        self.database_file = database_file
        self.connect()
        self.items = ItemOperations(self.cursor, self.connection)
        self.accounts = AccountOperations(self.cursor, self.connection)
        self._create_collections_if_not_exist()

    def connect(self) -> None:
        """Connect to the database"""
        self.connection = sqlite3.connect(self.database_file)
        self.cursor = self.connection.cursor()

    def disconnect(self) -> None:
        """Disconnect from the database"""
        self.connection.close()

    def _create_collections_if_not_exist(self) -> None:
        """Create the Items and Accounts tables if they don't exist."""
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = self.cursor.fetchall()
        tables = [table[0] for table in tables]
        if "Items" not in tables:
            self.cursor.execute("""
            CREATE TABLE Items(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                category INTEGER NOT NULL,
                quantity INTEGER NOT NULL,
                defective_quantity INTEGER NOT NULL
            );
            """)
            self.connection.commit()
        if "Accounts" not in tables:
            self.cursor.execute("""
            CREATE TABLE Accounts(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                permission INTEGER NOT NULL
            );
            """)
            self.connection.commit()


db = DatabaseService("inventory.db")