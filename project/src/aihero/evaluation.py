"""LLM-as-a-Judge evaluation schemas with chain-of-thought reasoning.

Implements structured output for evaluation agents with field ordering
that enforces reasoning before verdict (reduces evaluation variance by 10-15%).

Based on Pydantic AI best practices:
https://pydantic.dev/docs/ai/evals/evaluators/llm-judge/
"""

from pydantic import BaseModel, Field


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
