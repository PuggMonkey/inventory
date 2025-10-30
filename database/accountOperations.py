import sqlite3
from classes.account import Account


class AccountOperations:
    """Class to handle account operations in the database."""
    def __init__(self, cursor: sqlite3.Cursor, connection: sqlite3.Connection):
        self.cursor = cursor
        self.connection = connection
        
    def create_account(self, username: str, password_hash: str, permission: int) -> Account | None:
        """Create a new account in the Accounts table."""
        self.cursor.execute("""
        INSERT INTO Accounts (username, password_hash, permission)
        VALUES (?, ?, ?);
        """, (username, password_hash, permission))
        self.connection.commit()
        return self.get_account_by_username(username, password_hash)
        
    def get_account_by_username(self, username: str, password_hash: str) -> Account | None:
        """Retrieve an account from the Accounts table by username and password hash."""
        self.cursor.execute("""
        SELECT id, username, password_hash, permission
        FROM Accounts
        WHERE username = ? AND password_hash = ?;
        """, (username, password_hash))
        row = self.cursor.fetchone()
        if row:
            return Account(id=row[0], username=row[1], password_hash=row[2], permission=row[3])
        return 
    
    def delete_account(self, account_id: int) -> None:
        """Delete an account from the Accounts table by ID."""
        self.cursor.execute("""
        DELETE FROM Accounts
        WHERE id = ?;
        """, (account_id,))
        self.connection.commit()
