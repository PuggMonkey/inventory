import pytest
import sqlite3
import os
from unittest.mock import Mock, patch
import sys

# Add the project root to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Test database file
TEST_DB = "test_inventory.db"

@pytest.fixture
def test_database():
    """Set up and tear down test database"""
    # Remove test database if it exists
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)
    
    # Create test database with schema
    conn = sqlite3.connect(TEST_DB)
    cursor = conn.cursor()
    
    # Create tables
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Items(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            defective_quantity INTEGER NOT NULL
        );
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Accounts(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            permission INTEGER NOT NULL
        );
    """)
    
    # Insert test data
    cursor.execute("""
        INSERT INTO Accounts (username, password_hash, permission) 
        VALUES (?, ?, ?)
    """, ("admin", "8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918", 1))
    
    cursor.execute("""
        INSERT INTO Items (name, category, quantity, defective_quantity) 
        VALUES (?, ?, ?, ?)
    """, ("Test Hammer", 1, 10, 2))
    
    conn.commit()
    conn.close()
    
    yield TEST_DB
    
    # Cleanup - ensure all connections are closed first
    import gc
    gc.collect()
    
    # Try multiple times to remove the file
    for _ in range(5):
        try:
            if os.path.exists(TEST_DB):
                os.remove(TEST_DB)
            break
        except PermissionError:
            import time
            time.sleep(0.1)

@pytest.fixture
def mock_db_connection():
    """Mock database connection for unit tests"""
    mock_conn = Mock()
    mock_cursor = Mock()
    mock_conn.cursor.return_value = mock_cursor
    return mock_conn, mock_cursor

@pytest.fixture
def mock_db():
    """Mock the global db object"""
    with patch('database.databaseService.db') as mock_db:
        mock_db.items = Mock()
        mock_db.accounts = Mock()
        yield mock_db

@pytest.fixture
def db_service(test_database):
    """Provide a database service that automatically closes connections"""
    from database.databaseService import DatabaseService
    service = DatabaseService(test_database)
    yield service
    service.disconnect()