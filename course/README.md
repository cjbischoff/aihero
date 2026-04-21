# Course: Days 1-6 - RAG Fundamentals

This folder contains course reproductions for Days 1-6 of the AI Hero RAG crash course:
- **Day 1:** GitHub repository data ingestion
- **Day 2:** Document chunking strategies
- **Day 3:** Search methods (text, vector, hybrid)
- **Day 4:** AI agents with tool calling
- **Day 5:** LLM-as-a-Judge evaluation
- **Day 6:** Publishing and deploying your agent

All notebooks demonstrate core concepts with hands-on implementations and real-world examples.

## Notebook: day1.ipynb

### What It Does

Implements a complete GitHub ingestion pipeline:
1. Downloads repositories as zip archives via GitHub's codeload API
2. Extracts markdown documentation (.md and .mdx files)
3. Parses YAML frontmatter metadata from each file
4. Returns structured data ready for indexing

### Key Components

**Helper Functions:**
- `download_repo_zip()` - Downloads repo without authentication
- `is_markdown_file()` - Filters for .md/.mdx files
- `parse_markdown_with_frontmatter()` - Extracts metadata and content

**Main Function:**
- `read_repo_data(repo_owner, repo_name)` - Orchestrates the complete workflow

**Architecture:**
See [Pipeline Data Flow Diagram](../docs/diagrams/github-ingestion-pipeline.md) for a visual representation of how data transforms through the pipeline.

### Test Repositories

The notebook validates the implementation with two real-world repositories:

1. **DataTalks.Club FAQ** (1,285 documents)
   - Community Q&A documentation
   - Demonstrates handling of repositories with frontmatter

2. **Evidently AI Docs** (95 documents)
   - Technical product documentation
   - Uses MDX format with complex frontmatter

### Running the Notebook

**Setup:**
```bash
cd course/
uv sync
uv run jupyter notebook day1.ipynb
```

**Execution:**
- Run all cells from top to bottom (Kernel → Restart & Run All)
- Expected runtime: ~30-60 seconds (downloading test repos)
- All cells should execute without errors

### Key Concepts Explained

**Frontmatter:**
YAML metadata at the start of markdown files used by static site generators (Jekyll, Hugo, Next.js). Provides structured data like titles, descriptions, and navigation hints.

**In-Memory Processing:**
Uses BytesIO to process zip archives without disk I/O, making the pipeline more efficient for batch processing.

**Structured Output:**
Returns consistent format (`filename`, `metadata`, `content`) regardless of source repository structure.

### What You'll Learn

- How GitHub's codeload API works
- Why frontmatter is useful for documentation
- In-memory zip processing patterns
- Foundation for building RAG ingestion pipelines

## Notebook: day2.ipynb

### What It Does

Implements and compares four document chunking strategies for RAG systems:
1. **Sliding Window**: Fixed-size chunks (2000 chars) with overlap (1000 chars)
2. **Paragraph**: Splits on natural paragraph boundaries (`\n\s*\n`)
3. **Section**: Splits by markdown headers (`## `)
4. **LLM**: Semantic boundaries using OpenAI or Groq APIs

### Key Components

**Chunking Functions:**
- `chunk_sliding_window()` - Predictable fixed-size chunks
- `chunk_by_paragraph()` - Natural text boundaries
- `chunk_by_section()` - Topic-aligned via markdown structure
- `chunk_with_llm()` - AI-driven semantic chunking

**Analysis Tools:**
- `compare_chunking_strategies()` - Multi-metric comparison table
- `inspect_chunk_quality()` - Automated quality detection
- Token counting with tiktoken (cl100k_base encoding)

**Architecture:**
See `../docs/diagrams/phase-*-*.md` for visual representations of each chunking strategy.

### Test Data

Tests all strategies on Evidently AI docs from Day 1:
- 95 markdown documents
- Mix of structured and unstructured content
- Real-world complexity (code blocks, tables, headers)

### Running the Notebook

**Setup:**
```bash
cd course/
uv sync
uv run jupyter notebook day2.ipynb
```

**Dependencies:**
- tiktoken==0.12.0 (token counting)
- openai==2.30.0 (optional, for LLM chunking)
- groq==1.1.2 (optional, free tier alternative)

**Execution:**
- Requires Day 1 completion (imports `read_repo_data` from day1.py)
- LLM chunking section requires API key in `.env` (optional to run)
- Expected runtime: ~2-3 minutes (includes LLM API calls if enabled)

### Key Concepts Explained

**Chunking Trade-offs:**
- Sliding window: Fast, predictable, ignores structure
- Paragraph: Natural boundaries, variable sizes
- Section: Topic-aligned, requires structured docs
- LLM: Highest quality, costs scale with corpus

**Token Counting:**
Uses tiktoken with cl100k_base encoding (matches GPT-3.5/4 tokenizers) for accurate chunk sizing.

**Metadata Preservation:**
All strategies preserve original document metadata (filename, frontmatter) plus add chunk-specific fields (chunk_id, chunk_index, chunk_method, token_count).

### What You'll Learn

- Trade-offs between simple vs. semantic chunking
- When to use each strategy (decision framework)
- Cost analysis for LLM-based chunking
- Comparison frameworks for evaluating quality
- Hybrid approaches (combining strategies)

### Day 2 Learnings Summary

The notebook includes a comprehensive learnings summary with:
- Strategy comparison table (Best For | Pros | Cons | Cost)
- Key gotchas (cost scaling, size variance, structure requirements)
- Decision framework (when to use which strategy)

## Notebook: day3.ipynb

### What It Does

Implements and compares three search methods for RAG systems:
1. **Text Search**: TF-IDF with field boosting (exact term matching)
2. **Vector Search**: Semantic search with sentence embeddings
3. **Hybrid Search**: RRF fusion combining both approaches

### Key Components

**Search Functions:**
- `text_search()` - Lexical search with TF-IDF scoring
- `vector_search()` - Semantic search with cosine similarity
- `hybrid_search()` - Reciprocal Rank Fusion (RRF) combining both
- `compare_search_methods()` - Side-by-side comparison tool

**Models & Libraries:**
- `minsearch` - Lightweight TF-IDF and vector search
- `sentence-transformers` - Embedding generation (all-MiniLM-L6-v2)
- `torch` - Backend for sentence-transformers (CPU-only)

**Architecture:**
See `../docs/diagrams/` for visual representations:
- [Text Search Foundation](../docs/diagrams/text-search-foundation.md)
- [Vector Search Integration](../docs/diagrams/vector-search-integration.md)
- [Hybrid Search RRF Fusion](../docs/diagrams/hybrid-search-rrf-fusion.md)

### Test Data

Tests all strategies on DataTalks.Club FAQ and Evidently AI docs from Day 1:
- DataTalks: 1,285 documents (FAQ format)
- Evidently: 95 documents (technical documentation)

### Running the Notebook

**Setup:**
```bash
cd course/
uv sync
uv run jupyter notebook day3.ipynb
```

**Dependencies:**
- minsearch==0.0.6 (text and vector search)
- sentence-transformers==3.3.1 (embedding generation)
- torch==2.11.0 (CPU backend for transformers)

**Execution:**
- Requires Day 1 completion (imports `read_repo_data` from day1.py)
- First run generates embeddings (~3-4 min), subsequent runs use cache (<1s)
- Expected runtime: ~5 minutes first run, ~30 seconds cached

### Key Concepts Explained

**Text Search (TF-IDF):**
- Fast exact matching on keywords
- Field boosting (title:2.0, content:1.0)
- Best for acronyms and codes

**Vector Search (Semantic):**
- Understands meaning and paraphrases
- 384-dimensional embeddings
- Best for conceptual queries

**Hybrid Search (RRF):**
- Combines both methods using Reciprocal Rank Fusion
- k=60 (production-validated parameter)
- Best overall coverage

**Search Trade-offs:**
- Text: Fast, exact, fails on paraphrases
- Vector: Semantic, slower, may miss exact codes
- Hybrid: Best of both, slightly more complex

### What You'll Learn

- When to use each search method (decision framework)
- How TF-IDF scoring works with field boosting
- How sentence embeddings capture semantic meaning
- How RRF fusion combines rankings from multiple methods
- Production optimization patterns (embedding cache)
- Search strategy selection for different query types

### Day 3 Learnings Summary

The notebook includes a comprehensive learnings summary with:
- Search method comparison table (Best For | Strengths | Limitations | Production Use)
- Key insights (acronym handling, semantic queries, RRF fusion, cache pattern)
- Production recommendations (when to use each method)

## Notebook: day6.ipynb

### What It Does

Documents the journey from Day 4-5 notebooks to a deployed production agent:
1. Code extraction into standalone app/ modules
2. CLI interface for local testing
3. Streamlit web UI with streaming responses
4. Deployment to Streamlit Cloud with secrets management

**Deployed Agent:** https://aihero-nbzqjktqedjuiq6bqjbjwn.streamlit.app/

### Key Topics

**Module Extraction Patterns:**
- ingest.py: Data loading, chunking, indexing pipeline
- search_tools.py: SearchTool class with dependency injection
- search_agent.py: init_agent factory function
- logs.py: JSON logging with environment configuration

**SearchTool Class Pattern:**
- Problem: Global variables (text_index) work for notebooks but break for testing/reuse
- Solution: Dependency injection via class constructor
- Benefit: Testable, reusable, no import order dependencies

**Deployment Process:**
1. Generate requirements.txt: `uv export --no-dev > requirements.txt`
2. Configure Streamlit Cloud with app/ as root directory
3. Set Python 3.11 in Advanced settings
4. Configure TOML secrets: `OPENAI_API_KEY = "sk-..."`

### Running the Notebook

**Note:** This is a documentation-only notebook (no executable code cells).

```bash
cd course/
uv run jupyter notebook day6.ipynb
```

Read through the notebook to understand:
- Architecture comparison (notebook vs production)
- Dependency injection pattern (SearchTool class)
- Streamlit patterns (@st.cache_resource, session_state)
- Deployment troubleshooting (Python version, TOML secrets format)

### What You'll Learn

- Notebook-to-production refactoring patterns
- Dependency injection vs global variables
- CLI interface with asyncio
- Streamlit web UI with streaming
- Streamlit Cloud deployment step-by-step
- Hash-pinned dependencies for supply chain security

### Day 6 Learnings Summary

| Aspect | Notebook (Learning) | Production (app/) |
|--------|---------------------|-------------------|
| State | Global variables | Dependency injection |
| Config | Hardcoded | Environment variables |
| Execution | Cell-by-cell | Entry points |
| Interfaces | Single notebook | CLI + Web UI |

## Notebook: day4.ipynb

### What It Does

Implements AI agents that use search tools to answer questions:
1. **Manual OpenAI**: Function calling with JSON tool schemas and conversation history management
2. **Pydantic AI**: Framework that auto-generates schemas from type hints (~70% code reduction)
3. **FAQ Demonstration**: 5 test questions with agent responses
4. **System Prompt Experiments**: 3 different tones showing behavior control

### Key Components

**Agent Functions:**
- `run_agent()` - Manual OpenAI loop with tool calling
- Pydantic AI `Agent()` initialization with `@agent.tool_plain` decorator
- `text_search()` - Tool for searching indexed documents

**Models & Libraries:**
- `openai` - OpenAI Responses API for manual function calling
- `pydantic-ai` - Type-safe agent framework

**Architecture:**
See `../docs/diagrams/`:
- [Manual Agent Loop Flow](../docs/diagrams/manual-agent-loop-flow.md)
- [Pydantic AI Migration](../docs/diagrams/pydantic-ai-migration-comparison.md)
- [Agent-Tool Architecture](../docs/diagrams/agent-tool-architecture.md) (generic pattern)

### Running the Notebook

**Setup:**
```bash
cd course/
uv sync
uv run jupyter notebook day4.ipynb
```

**Dependencies:**
- openai==2.30.0 (function calling API)
- pydantic-ai>=1.77.0 (agent framework)
- Requires Day 3 completion (imports search functions and index)

**Execution:**
- Requires OPENAI_API_KEY in `.env` file
- Expected runtime: ~2-3 minutes (includes LLM API calls)

### Key Concepts Explained

**Function Calling:**
- LLM decides when to invoke tools based on user question
- Returns structured arguments matching tool schema
- Agent executes tool and feeds results back to LLM

**Stateless Pattern:**
- LLMs have no memory between API calls
- Full conversation history sent with every request
- Agent manages message array: [system, user, assistant, tool, ...]

**Framework Benefits:**
- Pydantic AI reduces ~50 lines to ~15 lines
- Type hints + docstrings become tool schema
- Error handling and loop termination built-in

### What You'll Learn

- How OpenAI function calling works at the API level
- Why Pydantic AI simplifies agent development
- System prompt engineering for behavior control
- Stateless conversation management pattern
- Production patterns: error handling, max steps

## Notebook: day5.ipynb

### What It Does

Implements LLM-as-a-Judge evaluation system for assessing agent response quality:
1. **JSON Logging**: Capture agent interactions with session metadata for evaluation
2. **Test Data Generation**: Manual test triplets + AI-powered question synthesis via Pydantic AI
3. **LLM-as-a-Judge Evaluation**: Structured rubrics with chain-of-thought reasoning
4. **Seven-Dimension Rubrics**: Comprehensive quality assessment across instruction following, answer quality, and tool usage

### Key Components

**Evaluation Schemas:**
- `EvaluationCheck` - Single dimension with justification and pass/fail verdict
- `EvaluationChecklist` - Aggregates all checks with overall_pass and metadata

**Rubrics:**
- Seven base dimensions: instructions_follow, instructions_avoid, answer_relevant, answer_clear, answer_citations, completeness, tool_call_search
- Chain-of-thought field ordering (justification before check_pass)

**Judge Agent:**
- Separate model (gpt-4o-mini) to prevent self-evaluation bias
- Temperature=0.0 for deterministic, reproducible verdicts
- Structured output via Pydantic ensures consistent evaluation format

**Architecture:**
See `../docs/diagrams/`:
- [LLM-as-a-Judge Evaluation Flow](../docs/diagrams/llm-as-a-judge-evaluation-flow.md)

### Running the Notebook

**Setup:**
```bash
cd course/
uv sync
uv run jupyter notebook day5.ipynb
```

**Dependencies:**
- pydantic-ai>=1.77.0 (structured output for evaluation)
- Requires Day 4 completion (uses FAQ agent logs)

**Execution:**
- Requires OPENAI_API_KEY in `.env` file
- Expected runtime: ~3-5 minutes (includes judge LLM API calls)

### Key Concepts Explained

**LLM-as-a-Judge:**
- Uses a separate LLM to evaluate agent outputs with structured rubrics
- More scalable than human review for large test sets
- Separate judge model prevents self-evaluation bias

**Chain-of-Thought Evaluation:**
- Field ordering in schema enforces LLM to generate reasoning (justification) before verdict (check_pass)
- Reduces evaluation variance by 10-15% (Pydantic AI best practice)

**Test Triplets:**
- Question + expected_answer + source_files + source tracking ('user' vs 'ai-generated')
- Enables retrieval metrics (hit rate, MRR) and answer quality assessment

**Structured Output:**
- Pydantic BaseModel schemas auto-validate LLM evaluation outputs
- Eliminates schema drift and JSON parsing errors

### What You'll Learn

- Why LLM-as-a-Judge evaluation is necessary for RAG systems
- How to design multi-dimension rubrics for comprehensive quality assessment
- Chain-of-thought pattern for reducing evaluation variance
- Separate judge model and temperature=0.0 for bias mitigation
- Structured output with Pydantic for reliable evaluation pipelines
- Test data generation strategies (manual curation vs AI synthesis)

## Notebook: day7.ipynb

### What It Does

Documents portfolio presentation best practices for AI/RAG projects:
1. **README Structure**: 11-section industry standard with RAG-specific guidance
2. **Evaluation Organization**: Learning artifacts (notebooks) vs production modules pattern
3. **Demo Creation**: Terminal GIFs (asciinema+agg, VHS), web recording (Streamlit), screenshots
4. **Social Sharing**: LinkedIn narrative templates, GitHub social preview, badge selection, community engagement

**This is a documentation-only notebook** (no executable code cells). It completes the course by teaching how to present your work effectively as a portfolio piece.

### Key Components

**Documentation Sections:**
- Section 1: README Structure (11-section standard comparison with v6.0 README)
- Section 2: Evaluation Organization (day5.ipynb vs project/src/aihero/ comparison)
- Section 3: Demo Creation Workflows (terminal GIFs, web recordings, screenshots)
- Section 4: Social Sharing Strategies (LinkedIn, GitHub, community engagement)
- Section 5: Learnings Summary (documentation vs implementation distinction)

**Reference Materials:**
- Live deployment example: https://aihero-nbzqjktqedjuiq6bqjbjwn.streamlit.app/
- LinkedIn five-part narrative template (hook/context/solution/learnings/CTA)
- GitHub social preview specifications (1280x640px)
- shields.io badge URL patterns

### Running the Notebook

**Note:** This is a documentation-only notebook with no executable code cells.

```bash
cd course/
uv run jupyter notebook day7.ipynb
```

Read through the notebook to understand:
- Industry-standard README structure and how v6.0 README compares
- When to separate learning artifacts from production modules
- Demo creation tool selection (asciinema vs VHS, Streamlit recorder, screencapture)
- LinkedIn algorithm optimization and cross-posting strategies

### Key Concepts Explained

**Documentation vs Implementation:**
Day 7 teaches a key professional skill: knowing when to document vs when to build. Portfolio presentation materials create value through clarity and synthesis, not through code. This notebook documents best practices WITHOUT implementing repository reorganization.

**11-Section README Standard:**
Modern README files follow: Title & Description, Overview, Features, Installation, Usage, Contributing, Tests, Deployment, FAQ, Credits, License. Day 7 compares this standard against v6.0 README.md to identify gaps (Contributing, Tests, FAQ, License deferred to v8.0+).

**Social Sharing as Technical Communication:**
The ability to explain complex systems clearly signals strong technical understanding. LinkedIn narrative posts (300-450 words), GitHub social previews, and cross-posting strategies demonstrate communication skills valued by hiring managers.

### What You'll Learn

- 11-section README structure standard and how to apply it
- When to use learning artifacts (notebooks) vs production modules
- Demo creation tool selection for different use cases
- LinkedIn algorithm priorities (2026) and optimal post structure
- GitHub social preview optimization (1280x640px)
- Badge selection (3-4 essential badges only)
- Cross-posting strategy (DEV.to-first, platform adaptation)
- The distinction between documentation and implementation as deliverables

### Day 7 Learnings Summary

The core lesson: Documentation itself is a deliverable. Day 7 completes the course by documenting how to present work effectively, demonstrating that portfolio presentation creates value through clarity, not code. This reflects professional judgment about what to build vs what to document.

## Next Steps

After completing all seven notebooks:
1. Review project/owasp_homework.ipynb for production implementation (Days 1-4)
2. Review project/src/aihero/ modules for production evaluation system (Day 5)
3. **Try the deployed agent**: https://aihero-nbzqjktqedjuiq6bqjbjwn.streamlit.app/
4. **Review app/ modules** for production deployment patterns (Day 6)
5. Explore docs/diagrams/ for visual flowcharts of all phases
6. Experiment with different queries to understand search method trade-offs
7. Run CLI locally: `cd app && python main.py`

---

**Note:** This is course-quality code focused on learning concepts, not production engineering standards. See `../project/` for a version with full engineering rigor (type hints, docstrings, pre-commit hooks, 10/10 test coverage).
