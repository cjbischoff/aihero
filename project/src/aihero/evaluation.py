"""LLM-as-a-Judge evaluation schemas with chain-of-thought reasoning.

Implements structured output for evaluation agents with field ordering
that enforces reasoning before verdict (reduces evaluation variance by 10-15%).

Based on Pydantic AI best practices:
https://pydantic.dev/docs/ai/evals/evaluators/llm-judge/
"""

import json
from datetime import datetime
from pathlib import Path
from typing import TypedDict

from pydantic import BaseModel, Field
from pydantic_ai import Agent
from pydantic_ai.models import ModelSettings


class EvaluationCheck(BaseModel):
    """Single evaluation dimension with chain-of-thought reasoning.

    Chain-of-thought pattern: justification field BEFORE check_pass field
    in schema definition ensures LLM generates reasoning before verdict,
    reducing evaluation variance by 10-15% (Pydantic AI best practice).

    Field order is CRITICAL - do not reorder without understanding impact
    on LLM evaluation quality.

    Attributes:
        dimension: Evaluation dimension name (e.g., 'answer_relevant',
            'answer_citations', 'instructions_follow')
        justification: Chain-of-thought reasoning explaining the verdict.
            Must analyze specific evidence from the response before
            reaching conclusion. LLM judge fills this FIRST.
        check_pass: Boolean verdict based on justification. True if
            response passes this dimension's rubric criteria, False otherwise.
            LLM judge fills this SECOND (after justification).

    Example:
        >>> check = EvaluationCheck(
        ...     dimension="answer_relevant",
        ...     justification="The response directly addresses Docker by explaining...",
        ...     check_pass=True
        ... )
        >>> check.check_pass
        True
    """

    dimension: str = Field(
        ...,
        description=(
            "Evaluation dimension name (e.g., 'answer_relevant', "
            "'answer_citations', 'instructions_follow')"
        ),
    )

    justification: str = Field(
        ...,
        description=(
            "Chain-of-thought reasoning explaining the verdict. "
            "Analyze specific evidence from the response, cite examples, "
            "and explain how the response meets or fails rubric criteria. "
            "Be thorough and specific."
        ),
    )

    check_pass: bool = Field(
        ...,
        description=(
            "Verdict based on justification. "
            "True if response passes this dimension's rubric criteria, "
            "False if it fails any requirement."
        ),
    )


class EvaluationChecklist(BaseModel):
    """Complete multi-dimensional evaluation result.

    Contains evaluation checks for all dimensions plus overall verdict.
    Overall pass requires ALL individual checks to pass (strict evaluation).

    Attributes:
        checks: List of evaluation checks, one per dimension evaluated
        overall_pass: Overall verdict - True if ALL checks passed,
            False if ANY check failed
        evaluated_at: ISO 8601 timestamp when evaluation was performed
        judge_model: Model identifier used for evaluation
            (e.g., 'openai:gpt-4o-mini')

    Example:
        >>> from datetime import datetime
        >>> checks = [
        ...     EvaluationCheck(
        ...         dimension="answer_relevant",
        ...         justification="Response addresses question...",
        ...         check_pass=True
        ...     ),
        ...     EvaluationCheck(
        ...         dimension="answer_citations",
        ...         justification="Citations are accurate...",
        ...         check_pass=True
        ...     )
        ... ]
        >>> checklist = EvaluationChecklist(
        ...     checks=checks,
        ...     overall_pass=all(c.check_pass for c in checks),
        ...     evaluated_at=datetime.now().isoformat(),
        ...     judge_model="openai:gpt-4o-mini"
        ... )
        >>> checklist.overall_pass
        True
        >>> json_str = checklist.model_dump_json()
        >>> isinstance(json_str, str)
        True
    """

    checks: list[EvaluationCheck] = Field(
        ...,
        description="List of evaluation checks, one per dimension evaluated",
    )

    overall_pass: bool = Field(
        ...,
        description=(
            "Overall verdict. True if ALL checks passed, False if ANY check failed. "
            "Calculated as: all(check.check_pass for check in checks)"
        ),
    )

    evaluated_at: str = Field(
        ...,
        description="ISO 8601 timestamp when evaluation was performed",
    )

    judge_model: str = Field(
        ...,
        description="Model used for evaluation (e.g., 'openai:gpt-4o-mini')",
    )


# Seven-Dimension Evaluation Rubrics (EVAL-02, EVAL-06)
# Based on RAGAS, Evidently AI, and Pydantic Evals best practices
# Source: https://docs.ragas.io/, https://www.evidentlyai.com/llm-guide/rag-evaluation

RUBRICS: dict[str, str] = {
    "instructions_follow": """
    The response MUST follow all system prompt constraints.

    Criteria:
    1. Adheres to required output format (if specified)
    2. Includes mandatory elements (disclaimers, caveats)
    3. Respects length, tone, or style guidelines
    4. Demonstrates clear understanding of system instructions

    Pass if response shows consistent adherence to instructions.
    """,
    "instructions_avoid": """
    The response MUST NOT violate explicit prohibitions.

    Criteria:
    1. Does not answer questions marked as out-of-scope
    2. Avoids prohibited content categories
    3. Respects safety guardrails and refusal instructions
    4. Does not perform actions explicitly forbidden

    Pass if response correctly refuses or avoids prohibited behaviors.
    """,
    "answer_relevant": """
    The response MUST directly address the user's question.

    Criteria:
    1. Answers the specific query asked, not a related question
    2. Stays on-topic throughout the response
    3. Provides information that resolves the user's actual need
    4. Does not drift into tangential topics

    Pass if response is clearly relevant to the question.
    Minor tangents acceptable if core query is addressed.
    """,
    "answer_clear": """
    The response MUST be understandable and well-structured.

    Criteria:
    1. Uses clear, accessible language
    2. Structures information logically
    3. Explains necessary jargon or technical terms
    4. Is readable by the target audience

    Pass if typical user can understand without confusion.
    Technical content acceptable if appropriate for domain.
    """,
    "answer_citations": """
    The response MUST cite sources accurately.

    Criteria:
    1. Cites sources for factual claims when sources are available
    2. Uses accurate source references (file names, document IDs)
    3. Does NOT fabricate or hallucinate citations
    4. Attributes claims to the correct documents

    Pass if citations are present, accurate, and properly attributed.
    FAIL if response fabricates citations or misattributes sources.
    """,
    "completeness": """
    The response MUST comprehensively address the question.

    Criteria:
    1. Addresses all aspects of the user's question
    2. Provides sufficient detail for the user's need
    3. Does not leave obvious gaps or unanswered sub-questions
    4. Covers the breadth of the query comprehensively

    Pass if response is complete enough to satisfy user's need.
    Brevity acceptable for simple questions, detail required for complex queries.
    """,
    "tool_call_search": """
    The response MUST use search tools appropriately.

    Criteria:
    1. Uses search tools when information retrieval is needed
    2. Searches for relevant context before answering factual questions
    3. Leverages retrieved documents in the response
    4. Does not hallucinate when search could provide grounding

    Pass if agent correctly used search tools when appropriate.
    FAIL if agent answered from memory when retrieval was needed.
    """,
}


# OWASP Security-Specific Rubrics (EVAL-05, EVAL-10)
# Extends base RUBRICS with domain-specific security dimensions
# Source: OWASP LLM Top 10, RAG security evaluation best practices

OWASP_RUBRICS: dict[str, str] = {
    **RUBRICS,  # Include all seven base dimensions
    "security_correctness": """
    The response MUST provide factually accurate security information.

    Criteria:
    1. Correctly identifies vulnerabilities and their OWASP category (LLM01-LLM10)
    2. Provides accurate descriptions of attack vectors and impacts
    3. Recommends valid mitigation techniques from OWASP guidance
    4. Does NOT suggest dangerous or ineffective security practices

    Pass if security advice is accurate and aligned with OWASP best practices.
    FAIL if response contains security misinformation or dangerous recommendations.

    Examples of FAIL:
    - Recommending sanitization alone for SQL injection (inadequate - use prepared statements)
    - Suggesting client-side input validation as sufficient (server-side required)
    - Misidentifying LLM vulnerability categories (e.g., calling prompt injection LLM02 instead of LLM01)
    """,
    "cve_citation_accuracy": """
    The response MUST cite CVE identifiers accurately.

    Criteria:
    1. CVE identifiers match correct vulnerability descriptions
    2. CVSS scores or severity ratings are accurate
    3. CVE references are verifiable (not fabricated)
    4. CVE details correctly attributed to the described vulnerability

    Pass if all CVE citations are accurate and verifiable.
    FAIL if response fabricates CVEs or misrepresents CVE details.

    Examples of FAIL:
    - Citing CVE-2023-12345 for a vulnerability with no such CVE
    - Mismatching CVE description (citing XSS CVE for SQLi vulnerability)
    - Incorrect CVSS score (claiming 9.8 critical when actual is 5.3 medium)
    """,
}


# LLMJudge Agent (EVAL-04, EVAL-09)
# Separate judge model prevents self-evaluation bias
# temperature=0.0 ensures deterministic, consistent evaluation
judge_agent = Agent(
    "openai:gpt-4o-mini",
    output_type=EvaluationChecklist,
    model_settings=ModelSettings(temperature=0.0),
    system_prompt="""You are an expert evaluator for RAG agent responses.

Your task: Assess response quality across multiple dimensions using explicit rubrics.

For EACH dimension:
1. Read the rubric criteria carefully
2. Analyze the response against EACH numbered criterion
3. Cite specific evidence from the response (quote relevant parts)
4. Provide detailed justification explaining your reasoning
5. Give final verdict (pass/fail) based on justification

Be thorough but fair. Minor imperfections are acceptable if core criteria are met.
Focus on whether the response serves the user's actual need, not perfection.

Chain-of-thought is REQUIRED: always justify before concluding.""",
)


class TestTriplet(TypedDict):
    """Test triplet structure from Phase 26.

    Re-defined here for type hint clarity (avoid circular import).
    Actual implementation in aihero.test_data module.
    """

    question: str
    expected_answer: str
    source_files: list[str]
    source: str


async def evaluate_response(
    log_file: Path,
    triplet: TestTriplet,
    rubrics: dict[str, str] | None = None,
) -> EvaluationChecklist:
    """Evaluate agent response using LLM-as-a-Judge.

    Implements EVAL-08: interface accepting log file + test triplet,
    returning evaluation checklist for downstream metrics analysis.

    Integrates:
    - Phase 25: Loads interaction log from log_file
    - Phase 26: Uses test triplet for ground truth comparison
    - Phase 27: Evaluates with judge_agent and RUBRICS

    Args:
        log_file: Path to JSON log from Phase 25 logging.py
        triplet: Test triplet from Phase 26 test_data.py with question,
            expected_answer, and source_files
        rubrics: Evaluation rubrics dict (default: RUBRICS for base dimensions,
            or OWASP_RUBRICS for security-specific evaluation)

    Returns:
        EvaluationChecklist with per-dimension checks and overall verdict

    Raises:
        FileNotFoundError: If log_file does not exist
        json.JSONDecodeError: If log_file is not valid JSON
        KeyError: If log_file missing required fields (response, system_prompt, etc.)

    Example:
        >>> from pathlib import Path
        >>> log = Path("logs/faq_agent_20260414_143052_a3f2.json")
        >>> triplet = {
        ...     "question": "What is RAG?",
        ...     "expected_answer": "Retrieval Augmented Generation...",
        ...     "source_files": ["rag-overview.md"],
        ...     "source": "user"
        ... }
        >>> checklist = await evaluate_response(log, triplet)
        >>> print(f"Overall: {'PASS' if checklist.overall_pass else 'FAIL'}")
        Overall: PASS
        >>> for check in checklist.checks:
        ...     print(f"{check.dimension}: {check.check_pass}")
        answer_relevant: True
        answer_clear: True
        ...
    """
    # Default to base RUBRICS if not specified
    if rubrics is None:
        rubrics = RUBRICS

    # EVAL-08: Load Phase 25 interaction log
    with open(log_file) as f:
        log_data = json.load(f)

    # Build evaluation context for judge agent
    evaluation_context = f"""
Question: {triplet['question']}

Expected Answer: {triplet['expected_answer']}

Actual Response: {log_data['response']}

System Prompt: {log_data['system_prompt']}

Tools Available: {', '.join(log_data['tools'])}

Retrieved Messages: {json.dumps(log_data.get('messages', []), indent=2)}
"""

    # Evaluate each dimension
    checks: list[EvaluationCheck] = []
    for dimension, rubric in rubrics.items():
        dimension_prompt = f"""
Dimension: {dimension}

Rubric:
{rubric}

Context:
{evaluation_context}

Evaluate the actual response against the rubric criteria.
Provide specific justification citing evidence from the response.
Give final verdict (pass/fail) based on your analysis.
"""

        # Run judge agent for this dimension
        # Note: Simplified single-dimension evaluation
        # Production could batch all dimensions in one call for efficiency
        result = await judge_agent.run(dimension_prompt)

        # Extract check from result
        # Judge agent returns EvaluationChecklist, we extract first check
        # (In production, customize output_type per dimension for cleaner extraction)
        check = EvaluationCheck(
            dimension=dimension,
            justification=result.output.checks[0].justification
            if result.output.checks
            else "No justification provided",
            check_pass=result.output.checks[0].check_pass
            if result.output.checks
            else False,
        )
        checks.append(check)

    # EVAL-07: Overall verdict (all checks must pass)
    overall_pass = all(check.check_pass for check in checks)

    return EvaluationChecklist(
        checks=checks,
        overall_pass=overall_pass,
        evaluated_at=datetime.now().isoformat(),
        judge_model="openai:gpt-4o-mini",
    )
