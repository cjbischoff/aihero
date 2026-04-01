# Phase 8: Semantic Chunking Flow

```mermaid
flowchart TD
    Start([Input: Document with metadata]) --> ChooseStrategy{Choose Strategy}

    ChooseStrategy -->|Paragraph-based| ParagraphFlow
    ChooseStrategy -->|Section-based| SectionFlow

    subgraph ParagraphFlow ["Paragraph Chunking"]
        Para1[Split text by regex:<br/>\\n\\s*\\n] --> Para2[Filter empty paragraphs]
        Para2 --> Para3[For each paragraph:<br/>create chunk dict]
        Para3 --> Para4[Preserve metadata:<br/>chunk_method='paragraph']
        Para4 --> Para5[Count tokens using tiktoken]
        Para5 --> ParaOut([Chunks: Natural text boundaries])
    end

    subgraph SectionFlow ["Section Chunking"]
        Sec1[Find all markdown headers:<br/>regex ^## .+$] --> Sec2{Headers found?}
        Sec2 -->|No| Sec3[Return full document<br/>as single chunk]
        Sec2 -->|Yes| Sec4[For each ## header section]
        Sec4 --> Sec5[Extract section text:<br/>from current ## to next ##<br/>or end of document]
        Sec5 --> Sec6[Include nested subsections:<br/>### headers stay with parent ##]
        Sec6 --> Sec7[Create chunk dict with:<br/>chunk_method='section']
        Sec7 --> Sec8[Preserve original metadata<br/>+ section header as context]
        Sec8 --> Sec9[Count tokens using tiktoken]
        Sec9 --> SecOut([Chunks: Topic-aligned sections])
        Sec3 --> SecOut
    end

    ParaOut --> Compare[Comparison Framework]
    SecOut --> Compare

    Compare --> Metrics[Calculate metrics:<br/>- Chunk counts<br/>- Token statistics<br/>- Size distributions<br/>- P25/P50/P75/P95 percentiles]

    Metrics --> Quality[Quality inspection:<br/>- Boundary problems<br/>- Unclosed code blocks<br/>- Orphaned references<br/>- Size outliers]

    Quality --> End([Output: Chunks + Analysis])

    style Start fill:#e1f5fe
    style End fill:#e1f5fe
    style Compare fill:#c8e6c9
    style Metrics fill:#c8e6c9
    style Quality fill:#c8e6c9
```

## Strategy Comparison

### Paragraph Chunking
**Pattern:** `\n\s*\n` (double newlines)

**Strengths:**
- Respects natural text boundaries
- Preserves thought units
- No mid-sentence splits

**Trade-offs:**
- Variable chunk sizes (3-15K chars observed)
- Some paragraphs too large for embeddings
- Many tiny chunks (single-line paragraphs)

**OWASP Results:**
- 14,254 chunks (vs 3,563 sliding window)
- Avg 75 tokens per chunk
- Max 43,195 tokens (single huge paragraph)

### Section Chunking
**Pattern:** `^## ` (markdown level-2 headers)

**Strengths:**
- Preserves document structure
- Topic-aligned boundaries
- Includes nested subsections (### headers)
- Moderate, predictable sizes

**Trade-offs:**
- Requires structured markdown
- Unstructured docs → single chunk
- Section size depends on author style

**OWASP Results:**
- 1,023 chunks
- Avg 1,045 tokens per chunk
- Median 1,598 chars
- Preserves LLM01, LLM02, etc. topic boundaries

## Comparison Framework Features

**Metrics calculated:**
1. **Counts:** Total chunks per strategy
2. **Token stats:** Mean, median, P25/P75/P95
3. **Size distribution:** Character count percentiles
4. **Efficiency:** Chunks per document

**Quality checks:**
1. **Boundary problems:** Mid-code-block splits
2. **Unclosed blocks:** Orphaned ``` or """
3. **Orphaned references:** Dangling [links] or footnotes
4. **Size outliers:** Chunks >10K chars or <50 chars

## Helper Functions

- `compare_chunking_strategies()` - Multi-metric comparison table
- `inspect_chunk_quality()` - Automated quality detection
- `show_sample_chunks()` - Manual inspection interface
