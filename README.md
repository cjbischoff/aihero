# AI Hero - RAG Course (Days 1-6)

A hands-on implementation from the AI Hero crash course on building RAG (Retrieval Augmented Generation) systems. This project demonstrates the complete RAG pipeline: GitHub data ingestion, document chunking strategies, search systems (text, vector, and hybrid), AI agents with tool integration, LLM-as-a-Judge evaluation, and production deployment with Streamlit Cloud.

## Current Status: v6.0 Phase 36 Complete ✓

**v1.0 - Day 1: GitHub Data Ingestion** (shipped 2026-03-30)
- Downloads GitHub repositories as zip archives
- Extracts markdown documentation with frontmatter metadata
- Returns structured data ready for indexing

**v1.1 - Day 2: Document Chunking** (shipped 2026-04-01)
- Four chunking strategies: sliding window, paragraph, section, LLM-based
- Hybrid approach combining paragraph boundaries with sliding window
- Token counting infrastructure with tiktoken
- Comparison framework for evaluating strategies

**v2.0 - Day 3: Search Systems** (shipped 2026-04-06)
- Text search with TF-IDF and field boosting (exact keyword matching)
- Vector search with sentence embeddings (semantic similarity)
- Hybrid search combining both via RRF fusion (k=60)
- Multi-granularity pattern (1,023 sections, 14,254 paragraphs)
- Production patterns (embedding cache, field boosting, RRF)

**v4.0 - Day 4: Agents and Tools** (shipped 2026-04-10)
- Manual OpenAI function calling (educational foundation for tool use)
- Pydantic AI framework migration (~70% code reduction)
- FAQ agent with text search tool integration (DataTalks corpus)
- OWASP security agent with hybrid search and domain-specific prompts

**v5.0 - Day 5: Evaluation** (Phase 27 complete 2026-04-14)
- JSON logging infrastructure for agent interactions (Phase 25)
- Test data generation: 125 triplets (25 manual + 100 AI-generated) (Phase 26)
- LLM-as-a-Judge evaluation with structured Pydantic schemas (Phase 27)
- Seven-dimension rubrics (instructions, answer quality, tool usage) + OWASP security extensions
- Chain-of-thought field ordering (justification before verdict reduces variance 10-15%)
- Separate judge model (gpt-4o-mini, temp=0.0) prevents self-evaluation bias

**v6.0 - Day 6: Publish Your Agent** (shipped 2026-04-17)
- Code refactored into standalone app/ modules (ingest, search, agent, logs)
- CLI interface for local testing (python app/main.py)
- Streamlit web UI with streaming responses
- Deployed to Streamlit Cloud with secrets management
- **Deployed:** https://aihero-nbzqjktqedjuiq6bqjbjwn.streamlit.app/

## Repository Structure

```
aihero/
├── course/              # Course reproduction (learning focus)
│   ├── day1.ipynb       # Day 1: GitHub data ingestion
│   ├── day2.ipynb       # Day 2: Chunking strategies
│   ├── day3.ipynb       # Day 3: Search systems (text, vector, hybrid)
│   ├── day4.ipynb       # Day 4: AI agents with tool calling
│   ├── day5.ipynb       # Day 5: LLM-as-a-Judge evaluation (inline implementation)
│   ├── requirements.lock # Hash-pinned dependencies
│   └── pyproject.toml   # Dependencies (requests, tiktoken, openai, groq, sentence-transformers, minsearch, pydantic-ai)
│
├── project/             # Engineering-quality implementations
│   ├── src/aihero/
│   │   ├── evaluation.py       # LLM-as-a-Judge schemas, rubrics, and judge agent
│   │   ├── logging.py          # JSON-based agent interaction logging
│   │   ├── test_data.py        # TestTriplet schema and validation utilities
│   │   └── question_generator.py # AI-powered question generation
│   ├── tests/
│   │   ├── conftest.py         # Shared pytest fixtures
│   │   └── test_evaluation.py  # 10/10 tests for EVAL-01 through EVAL-10
│   ├── owasp_homework.ipynb    # OWASP analysis (Days 1-4)
│   ├── requirements.lock       # Hash-pinned dependencies
│   ├── .pre-commit-config.yaml # Quality gates (black, ruff, mypy, snyk, pip-audit)
│   └── pyproject.toml          # Dependencies + dev tools
│
├── app/                 # Production deployment (Day 6)
│   ├── ingest.py        # Data loading, chunking, indexing
│   ├── search_tools.py  # SearchTool class (dependency injection)
│   ├── search_agent.py  # init_agent factory function
│   ├── logs.py          # JSON interaction logging
│   ├── main.py          # CLI entry point
│   ├── app.py           # Streamlit web UI entry point
│   ├── pyproject.toml   # uv project dependencies
│   └── requirements.txt # Generated for Streamlit Cloud
│
└── docs/
    └── diagrams/        # Mermaid diagrams for all phases
        ├── llm-as-a-judge-evaluation-flow.md  # Phase 27: Evaluation pipeline
        └── ...
```

**course/**: Follows AI Hero course structure with DataTalks FAQ and Evidently AI docs as examples.

**project/**: Applies learned patterns to OWASP LLM Top 10 repository with engineering standards (type hints, docstrings, pre-commit hooks).

## Prerequisites

- **Python 3.10+** (this project uses Python 3.13)
- **uv** package manager ([installation guide](https://github.com/astral-sh/uv))

Check your setup:
```bash
python --version  # Should show 3.10 or higher
uv --version      # Should show uv is installed
```

## Getting Started

Both `course/` and `project/` are independent uv projects. Set up either or both:

### Course Implementation
```bash
cd course/
uv sync

# Day 1: GitHub data ingestion
uv run jupyter notebook day1.ipynb

# Day 2: Chunking strategies
uv run jupyter notebook day2.ipynb

# Day 3: Search systems
uv run jupyter notebook day3.ipynb

# Day 4: AI agents
uv run jupyter notebook day4.ipynb

# Day 5: Evaluation
uv run jupyter notebook day5.ipynb
```

**Day 1 notebook** walks through:
1. Helper functions (download_repo_zip, parse_markdown_with_frontmatter)
2. Main read_repo_data() function
3. Tests with DataTalks FAQ (1,285 docs) and Evidently docs (95 docs)

**Day 2 notebook** implements:
1. Sliding window chunking (2000 chars, 1000 overlap)
2. Paragraph-based chunking (regex `\n\s*\n`)
3. Section-based chunking (markdown `## ` headers)
4. LLM-based intelligent chunking (OpenAI/Groq)
5. Comparison framework and quality inspection
6. Learnings summary with decision framework

**Day 3 notebook** implements:
1. Text search with TF-IDF and field boosting
2. Vector search with sentence embeddings (all-MiniLM-L6-v2)
3. Hybrid search combining both via RRF fusion (k=60)
4. Embedding cache pattern (<1s reload vs 3-4 min generation)
5. Multi-granularity indexing (sections for text, paragraphs for vector)
6. Performance comparison across all three search methods

**Day 4 notebook** implements:
1. Manual OpenAI function calling with tool schemas
2. Pydantic AI agent framework migration
3. FAQ demonstration with 5 test questions
4. System prompt experiments (3 different tones)
5. Educational comparison: manual vs framework approach

**Day 5 notebook** implements:
1. JSON logging for agent interactions (session metadata, messages, response)
2. Test data generation: manual triplets + AI-generated questions via Pydantic AI
3. LLM-as-a-Judge evaluation with EvaluationCheck and EvaluationChecklist schemas
4. Seven-dimension rubrics (instructions_follow, answer_relevant, citations, completeness, tool usage)
5. Chain-of-thought evaluation pattern (justification before verdict)
6. Inline implementation with educational comments

### Project Homework
```bash
cd project/
uv sync
uv run jupyter notebook owasp_homework.ipynb
```

The project notebook demonstrates:
1. **Day 1:** Adapting course patterns to OWASP repository (542 docs, minimal frontmatter)
2. **Day 2:** Hybrid chunking strategy (paragraph + sliding window)
3. **Day 3:** Multi-granularity search (1,023 sections, 14,254 paragraphs)
4. **Day 4:** Security agent with hybrid search and domain-specific system prompt
5. Strategy comparison on OWASP corpus
6. Documented analysis: which search approach works best for security documentation

### Deployed Agent
Try the live FAQ agent at:
https://aihero-nbzqjktqedjuiq6bqjbjwn.streamlit.app/

### Running Locally
```bash
cd app/
uv sync

# CLI interface
python main.py

# Web UI
streamlit run app.py
```

**Environment Variables:**
- `OPENAI_API_KEY` (required): Your OpenAI API key
- `LOGS_DIRECTORY` (optional): Log directory path (default: "logs")

## Key Concepts

### Day 1: Data Ingestion

**Frontmatter**: YAML metadata at the start of markdown files (common in Jekyll, Hugo, Next.js docs):
```yaml
---
title: Getting Started
sidebar_position: 1
---
```

**In-Memory Processing**: Zip archives processed in memory using `BytesIO`, avoiding disk I/O.

**Structured Data**: Consistent format ready for RAG indexing:
```python
{
  'filename': 'path/to/doc.md',
  'metadata': {'title': 'Page Title', ...},
  'content': 'Markdown content...'
}
```

### Day 2: Chunking Strategies

**Chunking**: Breaking large documents into smaller pieces for embedding and retrieval.

**Four Strategies Implemented:**

1. **Sliding Window**: Fixed-size chunks (2000 chars) with overlap (1000 chars)
   - Predictable sizes, fast
   - Ignores document structure

2. **Paragraph**: Split on double newlines (`\n\s*\n`)
   - Respects natural text boundaries
   - Variable sizes (some huge, some tiny)

3. **Section**: Split by markdown headers (`## `)
   - Topic-aligned, preserves structure
   - Requires structured markdown

4. **LLM**: Semantic boundaries using GPT/Mixtral
   - Highest quality, context-aware
   - Costs scale with corpus size

**Hybrid Approach**: Paragraph-first with sliding window fallback for oversized paragraphs. Best of both worlds.

**Token Counting**: Uses `tiktoken` (cl100k_base) for accurate token counts matching GPT-3.5/4 tokenizers.

### Day 3: Search Systems

**Text Search (TF-IDF)**: Lexical search using term frequency-inverse document frequency scoring with field boosting.

### Day 4: Agents and Tools

**AI Agent**: LLM-based system that can decide when and how to use tools to answer questions.

**Function Calling**: OpenAI API pattern where the model can request tool invocations with structured arguments.

**Tool Schema**: JSON definition describing what a function does, its parameters, and return types.

**Pydantic AI**: Framework that auto-generates tool schemas from Python type hints and docstrings.

**Stateless Pattern**: LLMs have no memory; conversation history must be sent with every API call.

**Agent Loop**: Iterative cycle: User question → LLM decides → Tool invocation → Results → LLM response.

**Architecture:**
See [Agent-Tool Architecture](docs/diagrams/agent-tool-architecture.md) for the generic agent pattern.

### Day 5: Evaluation

**LLM-as-a-Judge**: Using a separate LLM (judge model) to evaluate agent responses with structured rubrics.

**Evaluation Dimensions**: Seven quality criteria - instructions_follow/avoid, answer_relevant/clear/citations, completeness, tool_call_search.

**Chain-of-Thought Evaluation**: Field ordering where justification comes before check_pass in schema enforces reasoning before verdict (reduces variance 10-15%).

**Structured Output**: Pydantic BaseModel schemas (EvaluationCheck, EvaluationChecklist) auto-validate LLM evaluation outputs.

**Test Triplet**: Question + expected answer + source files + source tracking ('user' vs 'ai-generated').

**Separate Judge Model**: Using gpt-4o-mini for evaluation instead of FAQ agent model prevents self-evaluation bias.

**Temperature=0.0**: Deterministic evaluation settings for consistent, reproducible verdicts.

**Evaluation Pipeline:**
See [LLM-as-a-Judge Flow](docs/diagrams/llm-as-a-judge-evaluation-flow.md) for the complete evaluation architecture.

**Key Features:**
- Fast exact keyword matching
- Field boosting (title: 2.0, content: 1.0)
- Excels at acronyms and codes (e.g., "LLM01", "CVE-2024-1234")
- Inverted index for O(log N) search

**Vector Search (Semantic)**: Embedding-based similarity using sentence-transformers.

**Key Features:**
- Semantic understanding (handles paraphrases and synonyms)
- all-MiniLM-L6-v2 model (384 dimensions, 22MB)
- Cosine similarity scoring
- Embedding cache pattern (<1s reload vs 3-4 min generation)

**Hybrid Search (RRF)**: Combines text and vector results using Reciprocal Rank Fusion.

**Algorithm:**
```
RRF_score(doc) = Σ [1 / (k + rank_i(doc))]
where k=60 (production-validated parameter)
```

**Benefits:**
- Best of both worlds: exact match + semantic understanding
- Parameter-free fusion (k=60 works across corpora)
- Documents appearing in both lists rank higher (consensus ranking)

**Multi-Granularity Pattern**: Different chunk sizes optimized per search method.
- Text search: Section chunks (1,023 chunks, avg 1,045 tokens) for better statistics
- Vector search: Paragraph chunks (14,254 chunks, avg 75 tokens) for semantic precision
- RRF fusion: Maps paragraphs to sections for coherent results

## What You'll Learn

By exploring the notebooks, you'll understand:

**Day 1:**
- How to download and process GitHub repositories programmatically
- Why frontmatter is useful for documentation structure
- How code adapts to different repository organizations

**Day 2:**
- Trade-offs between simple vs. semantic chunking strategies
- When to use sliding window vs. paragraph vs. section vs. LLM chunking
- How to implement hybrid strategies for real-world documents
- Cost analysis for LLM-based chunking (free tiers vs. paid)
- Comparison frameworks for evaluating chunking quality

**Day 3:**
- When to use text search vs. vector search vs. hybrid search
- How TF-IDF and field boosting improve exact keyword matching
- How semantic embeddings capture meaning beyond exact terms
- Why RRF fusion (k=60) is production-validated and parameter-free
- Multi-granularity pattern: optimizing chunk size per search method
- Production optimizations: embedding cache, parallel search, storage patterns

**Day 4:**
- How AI agents decide when to use tools vs answer directly
- OpenAI function calling with JSON tool schemas
- Pydantic AI framework for type-safe agent development
- System prompt engineering for agent behavior control
- Stateless LLM pattern (managing conversation history)
- Production patterns: error handling, loop termination

**Day 5:**
- Why LLM-as-a-Judge evaluation is necessary for RAG systems
- How to log agent interactions for downstream evaluation
- Test data generation: manual curation vs AI-powered synthesis
- Structured evaluation with Pydantic schemas (EvaluationCheck, EvaluationChecklist)
- Chain-of-thought evaluation pattern (justification before verdict)
- Seven-dimension rubrics for comprehensive quality assessment
- Separate judge model and temperature=0.0 for bias mitigation and determinism

**Day 6:**
- Notebook-to-production refactoring patterns (global variables -> dependency injection)
- CLI interface with asyncio for local testing
- Streamlit web UI with streaming responses and session state
- Streamlit Cloud deployment with secrets management
- Hash-pinned dependencies for supply chain security

## About the Course

This project follows the [AI Hero](https://www.ai-hero.com/) crash course on building intelligent systems.

**✓ Day 1 (v1.0)**: Data ingestion - downloading and parsing GitHub documentation
**✓ Day 2 (v1.1)**: Document chunking - preparing documents for embedding and retrieval
**✓ Day 3 (v2.0)**: Search systems - text, vector, and hybrid search with RRF fusion
**✓ Day 4 (v4.0)**: AI agents - function calling and tool integration
**✓ Day 5 (v5.0 Phase 27)**: LLM-as-a-Judge evaluation - structured rubrics and quality assessment
**✓ Day 6 (v6.0)**: Production deployment - code refactoring, CLI, Streamlit, cloud deployment

## Standards & Quality

**Course Context** (`course/` folder):
- Learning-focused Jupyter notebooks
- Inline comments explaining concepts
- Reproducible from fresh kernel
- No comprehensive test suite (learning, not production)

**Project Context** (`project/` folder):
- Engineering-quality implementations
- Type hints and Google-style docstrings
- Pre-commit hooks: black, ruff, mypy, bandit, snyk, pip-audit
- Hash-pinned dependencies (`requirements.lock`)
- CodeRabbit CLI review on pre-push

See `CLAUDE.md` for complete standards documentation.

## Next Steps

1. **Start with Day 1**: `course/day1.ipynb` - GitHub data ingestion
2. **Continue with Day 2**: `course/day2.ipynb` - Four chunking strategies
3. **Explore Day 3**: `course/day3.ipynb` - Text, vector, and hybrid search systems
4. **Explore Day 4**: `course/day4.ipynb` - AI agents with tool calling
5. **Explore Day 5**: `course/day5.ipynb` - LLM-as-a-Judge evaluation
6. **Explore Day 6**: `course/day6.ipynb` - Production deployment patterns
7. **Try deployed agent**: https://aihero-nbzqjktqedjuiq6bqjbjwn.streamlit.app/
8. **Review project work**: `project/owasp_homework.ipynb` - OWASP analysis (Days 1-4)
9. **Review project modules**: `project/src/aihero/` - Production evaluation system (logging, test data, LLM-as-a-Judge)
10. **Explore diagrams**: `docs/diagrams/` - Mermaid flowcharts for all phases including evaluation pipeline

---

*Last updated: 2026-04-17 | v6.0 Phase 36 Complete ✓*
