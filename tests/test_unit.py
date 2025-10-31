import pytest
from unittest.mock import Mock, patch
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from classes.item import Item
from classes.account import Account
from classes.auth import Authenticator
from enums.category import Category
from enums.accountPermission import AccountPermission


class TestItemClass:
    """Unit tests for Item class"""
    
    def test_item_creation_valid_data(self, mock_db):
        """Test Item creation with valid data"""
        # Mock the database operations
        mock_db.items.update_item = Mock()
        
        item = Item(1, "Test Tool", Category.Parts, 10, 2)
        
        assert item.id == 1
        assert item.name == "Test Tool"
        assert item.category == Category.Parts
        assert item.quantity == 10
        assert item.defective_quantity == 2
    
    def test_item_creation_negative_quantity_raises_error(self, mock_db):
        """Test Item creation with negative quantity raises ValueError"""
        with pytest.raises(ValueError, match="Quantity and defective quantity must be non-negative"):
            Item(1, "Invalid Item", Category.Parts, -5, 0)
    
    def test_item_creation_negative_defective_raises_error(self, mock_db):
        """Test Item creation with negative defective quantity raises ValueError"""
        with pytest.raises(ValueError, match="Quantity and defective quantity must be non-negative"):
            Item(1, "Invalid Item", Category.Parts, 10, -2)
    
    def test_increase_quantity(self, mock_db):
        """Test increasing item quantity"""
        # Mock the database operations
        mock_db.items.update_item = Mock()
        
        item = Item(1, "Test Tool", Category.Parts, 10, 2)
        item.increase_quantity(5)
        
        assert item.quantity == 15
        mock_db.items.update_item.assert_called_once_with(1, "Test Tool", Category.Parts, 15, 2)
    
    def test_decrease_quantity_valid(self, mock_db):
        """Test decreasing item quantity with valid amount"""
        # Mock the database operations
        mock_db.items.update_item = Mock()
        
        item = Item(1, "Test Tool", Category.Parts, 10, 2)
        item.decrease_quantity(3)
        
        assert item.quantity == 7
        mock_db.items.update_item.assert_called_once_with(1, "Test Tool", Category.Parts, 7, 2)
    
    def test_decrease_quantity_insufficient_stock(self, mock_db):
        """Test decreasing item quantity below available stock raises error"""
        # Mock the database operations
        mock_db.items.update_item = Mock()
        
        item = Item(1, "Test Tool", Category.Parts, 10, 2)
        
        with pytest.raises(ValueError, match="Cannot decrease quantity below zero"):
            item.decrease_quantity(15)
        
        # Verify quantity unchanged
        assert item.quantity == 10
        # Ensure update_item was not called
        mock_db.items.update_item.assert_not_called()
    
    def test_mark_defective_valid(self, mock_db):
        """Test marking items as defective with valid amount"""
        # Mock the database operations
        mock_db.items.update_item = Mock()
        
        item = Item(1, "Test Tool", Category.Parts, 10, 2)
        item.mark_defective(3)
        
        assert item.quantity == 7
        assert item.defective_quantity == 5
        mock_db.items.update_item.assert_called_once_with(1, "Test Tool", Category.Parts, 7, 5)
    
    def test_mark_defective_insufficient_stock(self, mock_db):
        """Test marking more items as defective than available raises error"""
        # Mock the database operations
        mock_db.items.update_item = Mock()
        
        item = Item(1, "Test Tool", Category.Parts, 10, 2)
        
        with pytest.raises(ValueError, match="Cannot mark more items as defective than available quantity"):
            item.mark_defective(15)
        
        # Verify quantities unchanged
        assert item.quantity == 10
        assert item.defective_quantity == 2
        mock_db.items.update_item.assert_not_called()
    
    def test_repair_defective_valid(self, mock_db):
        """Test repairing defective items with valid amount"""
        # Mock the database operations
        mock_db.items.update_item = Mock()
        
        item = Item(1, "Test Tool", Category.Parts, 10, 5)
        item.repair_defective(3)
        
        assert item.quantity == 13
        assert item.defective_quantity == 2
        mock_db.items.update_item.assert_called_once_with(1, "Test Tool", Category.Parts, 13, 2)
    
    def test_repair_defective_insufficient_defective(self, mock_db):
        """Test repairing more defective items than available raises error"""
        # Mock the database operations
        mock_db.items.update_item = Mock()
        
        item = Item(1, "Test Tool", Category.Parts, 10, 5)
        
        with pytest.raises(ValueError, match="Cannot repair more defective items than available defective quantity"):
            item.repair_defective(8)
        
        # Verify quantities unchanged
        assert item.quantity == 10
        assert item.defective_quantity == 5
        mock_db.items.update_item.assert_not_called()


class TestAccountClass:
    """Unit tests for Account class"""
    
    def test_account_creation(self):
        """Test Account creation with valid data"""
        account = Account(1, "testuser", "hashed_password", AccountPermission.WRITE)
        
        assert account.id == 1
        assert account.username == "testuser"
        assert account.password_hash == "hashed_password"
        assert account.permission == AccountPermission.WRITE


class TestAuthenticatorClass:
    """Unit tests for Authenticator class"""
    
    def test_hash_password(self):
        """Test password hashing produces consistent results"""
        auth = Authenticator()
        
        hash1 = auth.hash_password("testpassword123")
        hash2 = auth.hash_password("testpassword123")
        
        # Should produce same hash for same input
        assert hash1 == hash2
        # Should be 64 characters (SHA-256 hex digest)
        assert len(hash1) == 64
    
    def test_hash_password_different_inputs(self):
        """Test different passwords produce different hashes"""
        auth = Authenticator()
        
        hash1 = auth.hash_password("password1")
        hash2 = auth.hash_password("password2")
        
        assert hash1 != hash2
    
    def test_find_account_success(self):
        """Test successful account finding"""
        mock_account = Account(1, "testuser", "hashed_password", AccountPermission.WRITE)
        
        with patch('database.databaseService.db') as mock_db:
            mock_db.accounts.get_account_by_username.return_value = mock_account
            
            auth = Authenticator()
            account = auth.find_account("testuser", "password123")
            
            assert account is not None
            assert account.username == "testuser"
            assert account.permission == AccountPermission.WRITE
    
    def test_find_account_not_found(self):
        """Test account finding when account doesn't exist"""
        with patch('database.databaseService.db') as mock_db:
            mock_db.accounts.get_account_by_username.return_value = None
            
            auth = Authenticator()
            account = auth.find_account("nonexistent", "wrongpassword")
            
            assert account is None