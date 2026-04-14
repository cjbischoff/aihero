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
