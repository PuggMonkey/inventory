import os
import sys

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from database.databaseService import DatabaseService
from enums.category import Category
from enums.accountPermission import AccountPermission


class TestDatabaseServiceIntegration:
    """Integration tests for DatabaseService"""
    
    def test_database_service_initialization(self, test_database):
        """Test DatabaseService initializes correctly with test database"""
        db_service = DatabaseService(test_database)
        
        assert db_service.database_file == test_database
        assert db_service.connection is not None
        assert db_service.cursor is not None
        assert db_service.items is not None
        assert db_service.accounts is not None
        
        db_service.disconnect()
    
    def test_table_creation(self, test_database):
        """Test tables are created if they don't exist"""
        # Remove existing test database to test table creation
        if os.path.exists(test_database):
            os.remove(test_database)
        
        db_service = DatabaseService(test_database)
        
        # Verify tables exist
        db_service.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [table[0] for table in db_service.cursor.fetchall()]
        
        assert "Items" in tables
        assert "Accounts" in tables
        
        db_service.disconnect()


class TestItemOperationsIntegration:
    """Integration tests for ItemOperations"""
    
    def test_add_item(self, test_database):
        """Test adding a new item to database"""
        db_service = DatabaseService(test_database)
        
        # Add new item
        db_service.items.add_item("New Wrench", Category.Parts, 15, 1)
        
        # Verify item was added
        db_service.cursor.execute("SELECT * FROM Items WHERE name = ?", ("New Wrench",))
        result = db_service.cursor.fetchone()
        
        assert result is not None
        assert result[1] == "New Wrench"
        assert result[2] == Category.Parts
        assert result[3] == 15
        assert result[4] == 1
        
        db_service.disconnect()
    
    def test_get_item(self, test_database):
        """Test retrieving an item by ID"""
        db_service = DatabaseService(test_database)
        
        item = db_service.items.get_item(1)  # ID from test data
        
        assert item is not None
        assert item.id == 1
        assert item.name == "Test Hammer"
        assert item.category == Category.Parts
        assert item.quantity == 10
        assert item.defective_quantity == 2
        
        db_service.disconnect()
    
    def test_get_all_items(self, test_database):
        """Test retrieving all items"""
        db_service = DatabaseService(test_database)
        
        # Add another item for testing
        db_service.items.add_item("Test Screwdriver", Category.Parts, 25, 0)
        
        items = db_service.items.get_all_items()
        
        assert items is not None
        assert len(items) >= 2
        assert any(item.name == "Test Hammer" for item in items)
        assert any(item.name == "Test Screwdriver" for item in items)
        
        db_service.disconnect()
    
    def test_update_item(self, test_database):
        """Test updating an existing item"""
        db_service = DatabaseService(test_database)
        
        # Update the test item
        db_service.items.update_item(1, "Updated Hammer", Category.Parts, 20, 3)
        
        # Verify update
        updated_item = db_service.items.get_item(1)
        
        assert updated_item.name == "Updated Hammer"
        assert updated_item.quantity == 20
        assert updated_item.defective_quantity == 3
        
        db_service.disconnect()
    
    def test_delete_item(self, test_database):
        """Test deleting an item"""
        db_service = DatabaseService(test_database)
        
        # Add item to delete
        db_service.items.add_item("Item to Delete", Category.Consumables, 5, 0)
        
        # Get its ID
        db_service.cursor.execute("SELECT id FROM Items WHERE name = ?", ("Item to Delete",))
        item_id = db_service.cursor.fetchone()[0]
        
        # Delete the item
        db_service.items.delete_item(item_id)
        
        # Verify deletion
        deleted_item = db_service.items.get_item(item_id)
        assert deleted_item is None
        
        db_service.disconnect()


class TestAccountOperationsIntegration:
    """Integration tests for AccountOperations"""
    
    def test_create_account(self, test_database):
        """Test creating a new account"""
        db_service = DatabaseService(test_database)
        
        # Create new account
        password_hash = "5e884898da28047151d0e56f8dc6292773603d0d6aabbddad4a6a6a6a6a6a6a6"
        new_account = db_service.accounts.create_account("newuser", password_hash, AccountPermission.READ)
        
        assert new_account is not None
        assert new_account.username == "newuser"
        assert new_account.permission == AccountPermission.READ
        
        # Verify account exists in database
        db_service.cursor.execute(
            "SELECT * FROM Accounts WHERE username = ?", 
            ("newuser",)
        )
        result = db_service.cursor.fetchone()
        assert result is not None
        assert result[1] == "newuser"
        
        db_service.disconnect()
    
    def test_get_account_by_username(self, test_database):
        """Test retrieving account by username and password hash"""
        db_service = DatabaseService(test_database)
        
        # Test with admin account from test data
        password_hash = "8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918"
        account = db_service.accounts.get_account_by_username("admin", password_hash)
        
        assert account is not None
        assert account.username == "admin"
        assert account.permission == AccountPermission.ADMIN
        
        db_service.disconnect()
    
    def test_get_account_invalid_credentials(self, test_database):
        """Test retrieving account with invalid credentials returns None"""
        db_service = DatabaseService(test_database)
        
        account = db_service.accounts.get_account_by_username("admin", "wronghash")
        
        assert account is None
        
        db_service.disconnect()
    
    def test_delete_account(self, test_database):
        """Test deleting an account"""
        db_service = DatabaseService(test_database)
        
        # Create account to delete
        password_hash = "hash123"
        db_service.accounts.create_account("user_to_delete", password_hash, AccountPermission.WRITE)
        
        # Get account ID
        db_service.cursor.execute(
            "SELECT id FROM Accounts WHERE username = ?", 
            ("user_to_delete",)
        )
        account_id = db_service.cursor.fetchone()[0]
        
        # Delete account
        db_service.accounts.delete_account(account_id)
        
        # Verify deletion
        db_service.cursor.execute(
            "SELECT * FROM Accounts WHERE username = ?", 
            ("user_to_delete",)
        )
        result = db_service.cursor.fetchone()
        assert result is None
        
        db_service.disconnect()


class TestAuthenticationIntegration:
    """Integration tests for authentication flow"""
    
    def test_successful_authentication_flow(self, test_database):
        """Test complete authentication flow with real database"""
        from classes.auth import Authenticator
        
        auth = Authenticator()
        
        # Test with admin credentials
        account = auth.find_account("admin", "admin")
        
        assert account is not None
        assert account.username == "admin"
        assert account.permission == AccountPermission.ADMIN
    
    def test_failed_authentication_flow(self, test_database):
        """Test authentication failure with wrong credentials"""
        from classes.auth import Authenticator
        
        auth = Authenticator()
        account = auth.find_account("admin", "wrongpassword")
        
        assert account is None