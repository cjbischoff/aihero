"""AI Hero - RAG course evaluation infrastructure.

This package provides utilities for evaluating RAG pipeline agents:
- logging: Agent interaction capture for evaluation
- test_data: Test triplet schema and validation for RAG evaluation
- question_generator: AI-powered question generation for test data scaling
"""

from aihero.test_data import TestTriplet, validate_test_set, save_test_set, load_test_set
from aihero.question_generator import (
    QuestionsList,
    question_generator,
    generate_questions_from_chunk,
    sample_chunks_for_generation,
)

__version__ = "0.1.0"
__all__ = [
    "logging",
    "TestTriplet",
    "validate_test_set",
    "save_test_set",
    "load_test_set",
    "QuestionsList",
    "question_generator",
    "generate_questions_from_chunk",
    "sample_chunks_for_generation",
]
