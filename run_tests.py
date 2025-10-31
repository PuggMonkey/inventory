#!/usr/bin/env python3
"""
Test runner for Inventory Management System
"""
import pytest
import sys

if __name__ == "__main__":
    print("Running Inventory Management System Tests...")
    print("=" * 50)
    
    # Run unit tests
    print("\n1. Running Unit Tests...")
    unit_result = pytest.main(["-v", "tests/test_unit.py"])
    
    # Run integration tests  
    print("\n2. Running Integration Tests...")
    integration_result = pytest.main(["-v", "tests/test_integration.py"])
    
    # Run all tests
    print("\n3. Running All Tests...")
    all_result = pytest.main(["-v", "tests/"])
    
    print("\n" + "=" * 50)
    print("Test Execution Complete!")
    
    sys.exit(all_result)