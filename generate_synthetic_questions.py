#!/usr/bin/env python3
"""Generate synthetic test questions for DataTalksClub FAQ and OWASP corpus.

This script generates AI-powered questions using the Pydantic AI question generator
from random corpus samples. Requires OPENAI_API_KEY environment variable.

Usage:
    # Generate DataTalksClub FAQ questions
    python generate_synthetic_questions.py --corpus datatalk --output course/data/test_data/synthetic_questions.json

    # Generate OWASP questions
    python generate_synthetic_questions.py --corpus owasp --output project/data/test_data/owasp_synthetic_qa.json
"""

import asyncio
import json
import sys
from pathlib import Path

# Add course and project to path
sys.path.insert(0, str(Path(__file__).parent / "course"))
sys.path.insert(0, str(Path(__file__).parent / "project" / "src"))

from day1 import read_repo_data  # type: ignore
from aihero.question_generator import sample_chunks_for_generation, generate_questions_from_chunk  # type: ignore


def create_chunks_from_docs(docs: list[dict]) -> list[dict]:
    """Convert documents to simple chunks with metadata.

    Args:
        docs: List of documents with filename, metadata, content fields.

    Returns:
        List of chunks with content and metadata.source_file.
    """
    chunks = []
    for doc in docs:
        # Simple paragraph-based chunking
        content = doc.get("content", "")
        paragraphs = [p.strip() for p in content.split("\n\n") if p.strip()]

        for idx, paragraph in enumerate(paragraphs):
            if len(paragraph) < 50:  # Skip very short paragraphs
                continue

            chunks.append({
                "content": paragraph,
                "metadata": {
                    "source_file": doc["filename"],
                    "chunk_id": f"{doc['filename']}_para_{idx}",
                }
            })

    return chunks


async def generate_datatalk_questions(output_path: Path, n_samples: int = 10):
    """Generate synthetic questions from DataTalksClub FAQ corpus."""
    print("Loading DataTalksClub FAQ corpus...")
    docs = read_repo_data("DataTalksClub", "faq")
    print(f"Loaded {len(docs)} documents")

    print("Creating chunks...")
    chunks = create_chunks_from_docs(docs)
    print(f"Created {len(chunks)} chunks")

    print(f"Sampling {n_samples} random chunks...")
    sampled_chunks = sample_chunks_for_generation(chunks, n_samples=n_samples, seed=42)

    print("Generating questions from sampled chunks...")
    all_triplets = []
    for idx, chunk in enumerate(sampled_chunks, 1):
        print(f"  Processing chunk {idx}/{len(sampled_chunks)}...")
        triplets = await generate_questions_from_chunk(chunk)
        all_triplets.extend(triplets)
        print(f"    Generated {len(triplets)} questions")

    print(f"Total questions generated: {len(all_triplets)}")

    # Save to JSON
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w') as f:
        json.dump(all_triplets, f, indent=2)

    print(f"Saved to {output_path}")
    return all_triplets


async def generate_owasp_questions(output_path: Path, n_samples: int = 10):
    """Generate synthetic questions from OWASP LLM Top 10 corpus."""
    print("Loading OWASP corpus...")
    docs = read_repo_data("OWASP", "www-project-top-10-for-large-language-model-applications")
    print(f"Loaded {len(docs)} documents")

    print("Creating chunks...")
    chunks = create_chunks_from_docs(docs)
    print(f"Created {len(chunks)} chunks")

    print(f"Sampling {n_samples} random chunks...")
    sampled_chunks = sample_chunks_for_generation(chunks, n_samples=n_samples, seed=42)

    print("Generating questions from sampled chunks...")
    all_triplets = []
    for idx, chunk in enumerate(sampled_chunks, 1):
        print(f"  Processing chunk {idx}/{len(sampled_chunks)}...")
        triplets = await generate_questions_from_chunk(chunk)
        all_triplets.extend(triplets)
        print(f"    Generated {len(triplets)} questions")

    print(f"Total questions generated: {len(all_triplets)}")

    # Save to JSON
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w') as f:
        json.dump(all_triplets, f, indent=2)

    print(f"Saved to {output_path}")
    return all_triplets


async def main():
    """Generate both DataTalksClub and OWASP synthetic questions."""
    # Generate DataTalksClub questions
    print("\n=== Generating DataTalksClub FAQ Questions ===")
    datatalk_output = Path("course/data/test_data/synthetic_questions.json")
    await generate_datatalk_questions(datatalk_output, n_samples=10)

    print("\n=== Generating OWASP Questions ===")
    owasp_output = Path("project/data/test_data/owasp_synthetic_qa.json")
    await generate_owasp_questions(owasp_output, n_samples=10)

    print("\n=== Generation Complete ===")


if __name__ == "__main__":
    asyncio.run(main())
