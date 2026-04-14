"""Unit tests for Phase 27 LLM-as-a-Judge evaluation.

Tests cover EVAL-01 through EVAL-10 requirements with wave attribution.
All stubs will pass once corresponding waves are implemented.

Wave 0 Status: ✅ Test infrastructure complete
- 10 test stubs created (EVAL-01 through EVAL-10)
- All stubs fail predictably with ImportError (expected)
- Wave 1+ implementation will make tests pass incrementally

Run: pytest project/tests/test_evaluation.py -v
Expected: 10 failed (ImportError) - this is correct for Wave 0
"""

import json
import re
from pathlib import Path
from typing import get_type_hints

import pytest


def test_evaluation_schemas(mock_evaluation_check):
    """EVAL-01: EvaluationCheck and EvaluationChecklist schemas validate correctly.

    Wave 1: Pydantic schema implementation pending.
    """
    from aihero.evaluation import EvaluationCheck, EvaluationChecklist

    # Verify EvaluationCheck instantiation
    check = EvaluationCheck(**mock_evaluation_check)
    assert check.dimension == "answer_relevant"
    assert check.check_pass is True
    assert len(check.justification) > 0

    # Verify EvaluationChecklist instantiation
    checklist = EvaluationChecklist(
        checks=[check],
        overall_pass=True,
        evaluated_at="2026-04-14T12:00:00",
        judge_model="openai:gpt-4o-mini",
    )
    assert len(checklist.checks) == 1
    assert checklist.overall_pass is True


def test_seven_dimensions():
    """EVAL-02: Seven evaluation dimensions defined in RUBRICS dict.

    Wave 2: Rubrics implementation pending.
    """
    from aihero.evaluation import RUBRICS

    expected_dimensions = {
        "instructions_follow",
        "instructions_avoid",
        "answer_relevant",
        "answer_clear",
        "answer_citations",
        "completeness",
        "tool_call_search",
    }

    assert set(RUBRICS.keys()) == expected_dimensions
    assert all(isinstance(rubric, str) for rubric in RUBRICS.values())
    assert all(len(rubric) > 50 for rubric in RUBRICS.values())  # Non-trivial rubrics


def test_chain_of_thought_order():
    """EVAL-03: justification field appears before check_pass in EvaluationCheck schema.

    Wave 1: Schema field order verification.
    """
    from aihero.evaluation import EvaluationCheck

    # Pydantic BaseModel stores field order in model_fields
    field_names = list(EvaluationCheck.model_fields.keys())

    justification_idx = field_names.index("justification")
    check_pass_idx = field_names.index("check_pass")

    assert (
        justification_idx < check_pass_idx
    ), "justification must appear before check_pass for chain-of-thought enforcement"


def test_separate_judge_model():
    """EVAL-04: Judge agent uses different model than FAQ agent.

    Wave 3: LLMJudge agent initialization.
    """
    from aihero.evaluation import judge_agent

    # Verify judge uses gpt-4o-mini (not gpt-5-nano like FAQ agent)
    assert judge_agent.model.model_id == "openai:gpt-4o-mini"

    # Verify judge != FAQ agent model
    faq_model = "openai:gpt-5-nano"  # From Phase 21
    assert judge_agent.model.model_id != faq_model


def test_owasp_rubrics():
    """EVAL-05: OWASP_RUBRICS includes security_correctness and cve_citation_accuracy.

    Wave 5: OWASP rubrics extension.
    """
    from aihero.evaluation import OWASP_RUBRICS, RUBRICS

    # Verify OWASP extends base rubrics
    assert len(OWASP_RUBRICS) == len(RUBRICS) + 2

    # Verify security-specific dimensions present
    assert "security_correctness" in OWASP_RUBRICS
    assert "cve_citation_accuracy" in OWASP_RUBRICS

    # Verify base dimensions still present
    for dimension in RUBRICS:
        assert dimension in OWASP_RUBRICS


def test_rubric_structure():
    """EVAL-06: Rubrics contain multi-part numbered criteria.

    Wave 2: Rubric content validation.
    """
    from aihero.evaluation import RUBRICS

    for dimension, rubric in RUBRICS.items():
        # Check for numbered criteria (1., 2., 3., 4.)
        numbered_criteria = re.findall(r"\d+\.", rubric)
        assert (
            len(numbered_criteria) >= 3
        ), f"{dimension} rubric must have 3+ numbered criteria, found {len(numbered_criteria)}"

        # Verify MUST/MUST NOT language for clarity
        assert "MUST" in rubric.upper(), f"{dimension} rubric missing MUST criteria"


def test_json_serialization(mock_evaluation_check):
    """EVAL-07: Evaluation results serialize to JSON via model_dump_json().

    Wave 1: Pydantic serialization.
    """
    from aihero.evaluation import EvaluationCheck, EvaluationChecklist

    check = EvaluationCheck(**mock_evaluation_check)
    checklist = EvaluationChecklist(
        checks=[check],
        overall_pass=True,
        evaluated_at="2026-04-14T12:00:00",
        judge_model="openai:gpt-4o-mini",
    )

    # Serialize to JSON string
    json_str = checklist.model_dump_json()

    # Verify valid JSON
    parsed = json.loads(json_str)
    assert parsed["overall_pass"] is True
    assert len(parsed["checks"]) == 1
    assert parsed["checks"][0]["dimension"] == "answer_relevant"


def test_evaluation_interface():
    """EVAL-08: evaluate_response function signature accepts log_file, triplet, returns checklist.

    Wave 4: Evaluation function interface.
    """
    from aihero.evaluation import evaluate_response

    # Inspect function signature via type hints
    hints = get_type_hints(evaluate_response)

    assert "log_file" in hints
    assert hints["log_file"] == Path

    assert "triplet" in hints
    # TestTriplet is TypedDict, check dict structure in runtime

    assert "return" in hints
    # Return type should be EvaluationChecklist (verified in integration test)


def test_temperature_zero():
    """EVAL-09: Judge agent ModelSettings includes temperature=0.0.

    Wave 3: Deterministic evaluation settings.
    """
    from aihero.evaluation import judge_agent

    # Access ModelSettings from agent
    model_settings = judge_agent.model_settings

    assert model_settings is not None, "ModelSettings not configured"
    assert (
        model_settings.temperature == 0.0
    ), "Judge must use temperature=0.0 for deterministic evaluation"


def test_dual_rubrics():
    """EVAL-10: Both RUBRICS and OWASP_RUBRICS available for course and project contexts.

    Wave 2 + Wave 5: Dual context support.
    """
    from aihero.evaluation import OWASP_RUBRICS, RUBRICS

    # Verify both rubric sets are dicts
    assert isinstance(RUBRICS, dict)
    assert isinstance(OWASP_RUBRICS, dict)

    # Verify non-empty
    assert len(RUBRICS) == 7  # Seven base dimensions
    assert len(OWASP_RUBRICS) == 9  # Seven base + two OWASP-specific

    # Verify independent usage (can use either)
    assert RUBRICS != OWASP_RUBRICS
