"""Shared pytest fixtures for Phase 27 LLM-as-a-Judge evaluation testing.

Provides reusable test data and temporary file fixtures to reduce duplication
across all 10 EVAL requirement test stubs.
"""

import json
from pathlib import Path
from typing import Any

import pytest

from aihero.test_data import TestTriplet


@pytest.fixture
def sample_log_data() -> dict[str, Any]:
    """Provide mock Phase 25 log structure for testing.

    Returns:
        dict: Complete log entry with session metadata, agent config, and messages.
            Matches the structure from aihero.logging.log_agent_call().
    """
    return {
        "session_id": "test_20260414_120000_a1b2",
        "agent_name": "faq_agent",
        "model": "openai:gpt-5-nano",
        "system_prompt": "You are a helpful FAQ assistant.",
        "tools": ["text_search"],
        "response": "Docker is a containerization platform...",
        "messages": [
            {"role": "user", "content": "What is Docker?"},
            {"role": "tool", "content": "Docker documentation..."},
        ],
    }


@pytest.fixture
def sample_test_triplet() -> TestTriplet:
    """Provide mock Phase 26 TestTriplet for testing.

    Returns:
        TestTriplet: Test data with question, expected answer, sources, and origin.
            Matches the TypedDict structure from aihero.test_data.
    """
    return {
        "question": "What is Docker?",
        "expected_answer": "Docker is a containerization platform...",
        "source_files": ["docker-setup.md"],
        "source": "user",
    }


@pytest.fixture
def mock_log_file(tmp_path: Path, sample_log_data: dict[str, Any]) -> Path:
    """Create temporary JSON log file for file I/O testing.

    Args:
        tmp_path: pytest's built-in temporary directory fixture.
        sample_log_data: Mock log structure from sample_log_data fixture.

    Returns:
        Path: Path to temporary log file containing serialized log data.
    """
    log_file = tmp_path / "test_log.json"
    with open(log_file, "w") as f:
        json.dump(sample_log_data, f)
    return log_file


@pytest.fixture
def mock_evaluation_check() -> dict[str, Any]:
    """Provide sample EvaluationCheck for schema validation testing.

    Returns:
        dict: EvaluationCheck fields matching expected Pydantic schema.
            Includes dimension, justification, and check_pass fields.
    """
    return {
        "dimension": "answer_relevant",
        "justification": "The response directly addresses Docker...",
        "check_pass": True,
    }
