"""AI Hero - RAG course evaluation infrastructure.

This package provides utilities for evaluating RAG pipeline agents:
- logging: Agent interaction capture for evaluation
- test_data: Test triplet schema and validation for RAG evaluation
"""

from aihero.test_data import TestTriplet, validate_test_set, save_test_set, load_test_set

__version__ = "0.1.0"
__all__ = ["logging", "TestTriplet", "validate_test_set", "save_test_set", "load_test_set"]
