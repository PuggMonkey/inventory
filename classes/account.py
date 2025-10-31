from enums.accountPermission import AccountPermission


class Account:
    """Account class represents a user account."""
    def __init__(self, id: int, username: str, password_hash: str, permission: int):
        self.id = id
        self.username = username
        self.password_hash = password_hash
        self.permission = permission
        
    def __repr__(self) -> str:
        return f"Account(id={self.id}, username='{self.username}', permission={self.permission})"
    
    def __str__(self) -> str:
        return f"Account(id={self.id}, username='{self.username}', permission={self.permission})"
