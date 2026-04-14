"""AI-powered question generation using Pydantic AI structured output.

This module provides question generation capabilities for scaling test coverage
beyond manual capacity. Uses Pydantic AI with QuestionsList output_type for
validated question generation from random corpus samples.

Typical usage:
    from aihero.question_generator import generate_questions_from_chunk

    # Sample random chunks
    chunks = sample_chunks_for_generation(corpus_chunks, n_samples=20, seed=42)

    # Generate questions
    for chunk in chunks:
        triplets = await generate_questions_from_chunk(chunk)
        all_triplets.extend(triplets)
"""

import random
from typing import Any, TypedDict

from pydantic_ai import Agent

from aihero.test_data import TestTriplet


class QuestionsList(TypedDict):
    """Validated list of questions generated from corpus chunk.

    Pydantic AI's output_type parameter auto-generates JSON schema from this
    TypedDict and validates LLM output, eliminating schema drift bugs.

    Attributes:
        questions: List of diverse questions that can be answered by the
            provided document chunk.

    Example:
        >>> result = await question_generator.run("Chunk: ...")
        >>> questions: list[str] = result.output['questions']
    """

    questions: list[str]


# Module-level agent instance (created on first import)
# Note: Requires OPENAI_API_KEY environment variable to be set
question_generator = Agent(
    "openai:gpt-4o-mini",
    output_type=QuestionsList,
    system_prompt="""You are a question generation expert. Generate diverse,
    realistic questions that could be answered by the provided document chunk.

    Guidelines:
    - Vary complexity: simple factual, conceptual understanding, multi-hop reasoning
    - Vary question styles: what, how, why, when, troubleshooting, comparison
    - Questions should require understanding the content, not just keyword matching
    - Generate 3-5 questions per chunk
    - Make questions natural as if asked by a real user

    Return as list under 'questions' key.""",
)


def sample_chunks_for_generation(
    chunks: list[dict[str, Any]], n_samples: int = 20, seed: int | None = None
) -> list[dict[str, Any]]:
    """Sample random chunks from corpus for question generation.

    Random sampling without replacement ensures broad coverage across corpus,
    preventing bias toward popular or recent documents.

    Args:
        chunks: Full corpus chunks with 'content' and 'metadata' fields.
        n_samples: Number of chunks to sample (default: 20).
        seed: Random seed for reproducibility (optional).

    Returns:
        Random sample of chunks without replacement.

    Example:
        >>> chunks = load_corpus()
        >>> sampled = sample_chunks_for_generation(chunks, n_samples=10, seed=42)
        >>> len(sampled)
        10
    """
    if seed is not None:
        random.seed(seed)

    sample_size = min(n_samples, len(chunks))
    return random.sample(chunks, sample_size)


async def generate_questions_from_chunk(chunk: dict[str, Any]) -> list[TestTriplet]:
    """Generate questions from corpus chunk via Pydantic AI.

    Extracts source file metadata, generates diverse questions, and creates
    test triplets with source='ai-generated' for traceability.

    Args:
        chunk: Document chunk with 'content' and 'metadata' fields.
            metadata should contain 'source_files' or 'source_file'.

    Returns:
        List of TestTriplet dicts with source='ai-generated'.

    Example:
        >>> chunk = {"content": "Docker is...", "metadata": {"source_file": "docker.md"}}
        >>> triplets = await generate_questions_from_chunk(chunk)
        >>> len(triplets)
        4
        >>> triplets[0]['source']
        'ai-generated'
    """
    content = chunk.get("content", chunk.get("text", ""))
    metadata = chunk.get("metadata", {})

    # Extract source files from chunk metadata
    source_files = metadata.get("source_files", [])
    if not source_files and "source_file" in metadata:
        source_files = [metadata["source_file"]]
    if not source_files and "filename" in metadata:
        source_files = [metadata["filename"]]

    # Generate questions via Pydantic AI
    result = await question_generator.run(
        f"Document chunk:\n\n{content}\n\nGenerate diverse questions."
    )

    # Extract validated questions list
    questions = result.output["questions"]

    # Create triplets with source tracking (TEST-08)
    triplets: list[TestTriplet] = []
    for question in questions:
        triplets.append(
            {
                "question": question,
                "expected_answer": "",  # To be filled by agent or human review
                "source_files": source_files,
                "source": "ai-generated",
            }
        )

    return triplets
