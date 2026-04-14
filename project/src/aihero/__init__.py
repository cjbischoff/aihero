"""AI Hero - RAG course evaluation infrastructure.

This package provides utilities for evaluating RAG pipeline agents:
- logging: Agent interaction capture for evaluation
- test_data: Test triplet schema and validation for RAG evaluation
- question_generator: AI-powered question generation for test data scaling
- evaluation: Pydantic schemas for LLM-as-a-Judge structured output (Phase 27)
"""

from aihero.test_data import TestTriplet, validate_test_set, save_test_set, load_test_set
from aihero.question_generator import (
    QuestionsList,
    question_generator,
    generate_questions_from_chunk,
    sample_chunks_for_generation,
)
from aihero.evaluation import (
    EvaluationCheck,
    EvaluationChecklist,
    RUBRICS,
    judge_agent,
)

__version__ = "0.1.0"
__all__ = [
    "logging",
    # Test data (Phase 26)
    "TestTriplet",
    "validate_test_set",
    "save_test_set",
    "load_test_set",
    # Question generation (Phase 26)
    "QuestionsList",
    "question_generator",
    "generate_questions_from_chunk",
    "sample_chunks_for_generation",
    # Evaluation schemas (Phase 27)
    "EvaluationCheck",
    "EvaluationChecklist",
    "RUBRICS",
    "judge_agent",
]
