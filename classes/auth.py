from classes.account import Account


class Authenticator:
    """Authenticator class handles user authentication."""
    def __init__(self):
        pass
    
    def hash_password(self, password: str) -> str:
        """Hashes a password using SHA-256."""
        import hashlib
        return hashlib.sha256(password.encode()).hexdigest()
    
    def find_account(self, username: str, password: str) -> Account | None:
        """Finds an account by username and password."""
        from database.databaseService import db
        return db.accounts.get_account_by_username(username, self.hash_password(password))