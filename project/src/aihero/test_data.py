"""Test data generation and validation for RAG evaluation.

This module provides the TestTriplet schema and utilities for creating,
validating, and managing test Q&A pairs with ground-truth context labels.

Typical usage:
    from aihero.test_data import TestTriplet, validate_test_set, save_test_set

    # Create test triplets
    triplets: list[TestTriplet] = [
        {
            "question": "What is Docker?",
            "expected_answer": "Docker is a containerization platform...",
            "source_files": ["docker-setup.md"],
            "source": "user"
        }
    ]

    # Validate and save
    validate_test_set(triplets)
    save_test_set(triplets, Path("data/test_data/manual_qa.json"))
"""

from pathlib import Path
from typing import TypedDict
import json


class TestTriplet(TypedDict):
    """Structure for test Q&A pairs with ground-truth context.

    Each triplet represents a complete test case for RAG evaluation,
    containing the question, expected answer, source documents, and
    origin tracking (manual vs AI-generated).

    Attributes:
        question: User query or question to be answered.
        expected_answer: Ground truth answer for evaluation.
        source_files: List of document filenames that contain the answer.
            Used for retrieval metrics (hit rate, MRR).
        source: Origin of the question - either "user" (manually curated)
            or "ai-generated" (synthetic from LLM).

    Example:
        >>> triplet: TestTriplet = {
        ...     "question": "How do I install Docker?",
        ...     "expected_answer": "Install Docker Desktop from docker.com...",
        ...     "source_files": ["docker-setup.md", "environment.md"],
        ...     "source": "user"
        ... }
    """

    question: str
    expected_answer: str
    source_files: list[str]
    source: str  # Literal["user", "ai-generated"]


def validate_test_set(triplets: list[TestTriplet]) -> bool:
    """Validate structure and content of test triplets.

    Ensures each triplet has all required fields with valid values:
    - All fields present (question, expected_answer, source_files, source)
    - source is either "user" or "ai-generated"
    - source_files is a non-empty list

    Args:
        triplets: List of test triplets to validate.

    Returns:
        True if all triplets pass validation.

    Raises:
        ValueError: If any triplet is missing required fields, has invalid
            source value, or has empty source_files list.

    Example:
        >>> triplets = [{"question": "Q?", "expected_answer": "A",
        ...              "source_files": ["doc.md"], "source": "user"}]
        >>> validate_test_set(triplets)
        True
    """
    required_fields = {"question", "expected_answer", "source_files", "source"}

    for idx, triplet in enumerate(triplets):
        # Check all required fields present
        missing_fields = required_fields - set(triplet.keys())
        if missing_fields:
            raise ValueError(
                f"Triplet {idx} missing required fields: {missing_fields}"
            )

        # Validate source field
        if triplet["source"] not in ["user", "ai-generated"]:
            raise ValueError(
                f"Triplet {idx} has invalid source '{triplet['source']}'. "
                f"Must be 'user' or 'ai-generated'."
            )

        # Validate source_files is non-empty list
        if not isinstance(triplet["source_files"], list):
            raise ValueError(
                f"Triplet {idx} source_files must be a list, "
                f"got {type(triplet['source_files'])}"
            )

        if len(triplet["source_files"]) == 0:
            raise ValueError(
                f"Triplet {idx} source_files must be non-empty. "
                f"Question: {triplet['question'][:50]}..."
            )

    return True


def save_test_set(triplets: list[TestTriplet], output_path: Path) -> Path:
    """Save test triplets to JSON file.

    Creates parent directories if needed, validates triplets before saving,
    and writes formatted JSON with 2-space indentation.

    Args:
        triplets: List of validated test triplets.
        output_path: Path to output JSON file.

    Returns:
        Path to the created file (same as output_path).

    Raises:
        ValueError: If triplets fail validation.
        IOError: If file cannot be written.

    Example:
        >>> triplets = [{"question": "Q?", "expected_answer": "A",
        ...              "source_files": ["doc.md"], "source": "user"}]
        >>> save_test_set(triplets, Path("data/test_data/manual_qa.json"))
        PosixPath('data/test_data/manual_qa.json')
    """
    # Validate before saving
    validate_test_set(triplets)

    # Create parent directories if needed
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Write JSON with formatting
    with open(output_path, "w") as f:
        json.dump(triplets, f, indent=2)

    return output_path


def load_test_set(input_path: Path) -> list[TestTriplet]:
    """Load and validate test triplets from JSON file.

    Reads JSON file, validates structure, and returns typed triplets.

    Args:
        input_path: Path to JSON file containing test triplets.

    Returns:
        List of validated TestTriplet dicts.

    Raises:
        ValueError: If loaded triplets fail validation.
        FileNotFoundError: If input file does not exist.
        json.JSONDecodeError: If file is not valid JSON.

    Example:
        >>> triplets = load_test_set(Path("data/test_data/manual_qa.json"))
        >>> print(f"Loaded {len(triplets)} triplets")
        Loaded 10 triplets
    """
    # Read JSON file
    with open(input_path, "r") as f:
        triplets = json.load(f)

    # Validate loaded data
    validate_test_set(triplets)

    return triplets
