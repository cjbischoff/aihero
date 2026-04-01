# Phase 10: Course Notebook Educational Polish

```mermaid
flowchart TD
    Start([course/day2.ipynb<br/>with 4 chunking strategies]) --> Structure[Add notebook structure]

    Structure --> Import[Cell 1: Import Day 1 functions<br/>from day1.py]
    Import --> LoadData[Cell 2: Load Evidently docs<br/>using read_repo_data()]

    LoadData --> Section1[## Section: Sliding Window Chunking]
    Section1 --> Impl1[Implementation cell:<br/>chunk_sliding_window()]
    Impl1 --> Comment1[Add inline comments:<br/>'Slide by size - overlap'<br/>'Preserve metadata']
    Comment1 --> Demo1[Demo cell: Run on Evidently<br/>Show sample output]

    Demo1 --> Section2[## Section: Paragraph Chunking]
    Section2 --> Impl2[Implementation cell:<br/>chunk_by_paragraph()]
    Impl2 --> Comment2[Add inline comments:<br/>'Split by \\n\\s*\\n'<br/>'Filter empty paragraphs']
    Comment2 --> Demo2[Demo cell: Run on Evidently<br/>Show sample output]

    Demo2 --> Section3[## Section: Section Chunking]
    Section3 --> Impl3[Implementation cell:<br/>chunk_by_section()]
    Impl3 --> Comment3[Add inline comments:<br/>'Find ## headers'<br/>'Section ends at next ##']
    Comment3 --> Demo3[Demo cell: Run on Evidently<br/>Show sample output]

    Demo3 --> Section4[## Section: LLM Chunking]
    Section4 --> Impl4[Implementation cell:<br/>chunk_with_llm()]
    Impl4 --> Comment4[Add inline comments:<br/>'Provider switching'<br/>'Cost tracking']
    Comment4 --> Demo4[Demo cell: Run on subset<br/>Show cost analysis]

    Demo4 --> Learnings[## Day 2 Learnings Summary]
    Learnings --> Table[Create comparison table:<br/>Strategy | Best For | Pros | Cons | Cost]
    Table --> Gotchas[Add 'Key Gotchas' section:<br/>- LLM cost scaling<br/>- Paragraph size variance<br/>- Section chunking requires structure]
    Gotchas --> Framework[Add 'Decision Framework':<br/>Flowchart for strategy selection]

    Framework --> Dividers[Add visual dividers:<br/>--- separators<br/>Section headers]

    Dividers --> Validate[Validation:<br/>Execute from fresh kernel<br/>All cells run successfully<br/>Outputs committed]

    Validate --> End([Polished educational notebook<br/>ready for learners])

    style Start fill:#e1f5fe
    style End fill:#e1f5fe
    style Learnings fill:#fff9c4
    style Table fill:#fff9c4
    style Gotchas fill:#fff9c4
    style Framework fill:#fff9c4
```

## Educational Polish Elements

### 1. Day 1 Integration
```python
# Cell 1: Import from Day 1
from day1 import read_repo_data

# Load Evidently docs (from Day 1 ingestion)
evidently_docs = read_repo_data(
    "evidentlyai",
    "evidently",
    "main",
    "docs/book",
    [".md", ".mdx"]
)
print(f"Loaded {len(evidently_docs)} documents")
```

### 2. Inline Explanations
Added comments explaining:
- **Token counting rationale:** "cl100k_base matches GPT-3.5/4 tokenizer"
- **Overlap purpose:** "Prevents context loss at chunk boundaries"
- **Semantic boundaries:** "Paragraph splits preserve thought units"

### 3. Sample Outputs
Each strategy demo shows:
- Chunk count
- Example chunk structure
- Token distribution
- Metadata preservation

### 4. Learnings Summary Table

| Strategy | Best For | Pros | Cons | Cost |
|----------|----------|------|------|------|
| Sliding Window | Fixed-size embeddings, predictable chunks | Consistent sizes, fast | Ignores structure, mid-sentence splits | Free |
| Paragraph | Blog posts, narratives | Natural boundaries, preserves thoughts | Variable sizes, some huge paragraphs | Free |
| Section | Structured docs (## headers) | Topic-aligned, moderate sizes | Requires structure, author-dependent | Free |
| LLM | Unstructured complex docs | Semantic boundaries, context-aware | Slow (1-2s/doc), costs scale | $0.15-1.50/1M tokens |

### 5. Key Gotchas

**LLM Chunking:**
- Free tier quotas (Groq: 14.4K req/day)
- Cost scales linearly with corpus size (542 docs = $0.28)
- API latency adds up (1-2s per doc × 10K docs = 3-6 hours)

**Paragraph Chunking:**
- Size variance extreme (3 tokens to 43K tokens observed)
- Single-paragraph docs become single chunks (defeats purpose)
- Need hybrid approach for oversized paragraphs

**Section Chunking:**
- Requires `## ` headers (unstructured docs → single chunk)
- Quality depends on author's section sizing
- Nested `###` headers preserved with parent

### 6. Decision Framework

```
START → Structured docs with ## headers?
    ├─ YES → Section chunking
    │        └─ Preserves topics, moderate sizes
    └─ NO → Natural paragraph breaks?
            ├─ YES → Paragraph chunking
            │        └─ Check size variance, use hybrid if needed
            └─ NO → Complex unstructured content?
                    ├─ YES → LLM chunking (if budget allows)
                    │        └─ Best semantic boundaries
                    └─ NO → Sliding window
                             └─ Simple, predictable fallback
```

## Validation Checklist

- [x] All cells execute from fresh kernel
- [x] No errors or warnings
- [x] Sample outputs visible (committed to git)
- [x] Inline comments explain key decisions
- [x] Learnings summary comprehensive
- [x] Decision framework actionable
- [x] Visual dividers improve readability
- [x] Imports Day 1 functions (demonstrates continuity)
