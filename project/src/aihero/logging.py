"""Agent interaction logging for evaluation.

This module provides JSON-based logging of Pydantic AI agent interactions
for downstream evaluation. Each agent.run() invocation produces a single
JSON log file containing the complete interaction state.

Typical usage:
    from aihero.logging import log_interaction_to_file

    result = await agent.run(question)
    log_file = log_interaction_to_file(agent, result, source="user")
    print(f"Logged to: {log_file}")
"""

import json
import secrets
from datetime import datetime
from pathlib import Path
from typing import Any

from pydantic_ai import Agent, AgentRunResult
from pydantic_ai.messages import ModelMessagesTypeAdapter

# LOG-07: Create logs directory structure
LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)


def datetime_serializer(obj: Any) -> str:
    """Custom JSON serializer for datetime objects.

    Converts datetime objects to ISO 8601 format strings for JSON serialization.
    Used as the `default` parameter in json.dump() calls.

    Args:
        obj: Object to serialize (expected to be datetime).

    Returns:
        ISO 8601 formatted string (e.g., "2026-04-10T14:30:52.123456").

    Raises:
        TypeError: If obj is not a datetime object.

    Example:
        >>> import json
        >>> from datetime import datetime
        >>> data = {"timestamp": datetime.now()}
        >>> json.dumps(data, default=datetime_serializer)
        '{"timestamp": "2026-04-10T14:30:52.123456"}'
    """
    # LOG-05: Datetime serialization for ISO format timestamps
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError(f"Type {type(obj)} not serializable")


def generate_log_filename(agent_name: str) -> str:
    """Generate unique timestamped filename with collision resistance.

    Creates filenames in format: {agent_name}_{YYYYMMDD_HHMMSS}_{hex}.json
    The 4-character hex suffix provides 65K uniqueness per second.

    Args:
        agent_name: Name of the agent (e.g., "faq_agent", "owasp_agent").

    Returns:
        Filename string (not full path).

    Example:
        >>> generate_log_filename("faq_agent")
        'faq_agent_20260410_143052_a3f2.json'
    """
    # LOG-06: Unique timestamped filenames with random hex
    # D-25: Use datetime.now() for timestamp generation
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    # D-13: Generate 4-character hex suffix via secrets.token_hex(2)
    random_suffix = secrets.token_hex(2)
    return f"{agent_name}_{timestamp}_{random_suffix}.json"


def log_interaction_to_file(
    agent: Agent[Any, Any],
    result: AgentRunResult[Any],
    source: str = "user",
) -> Path:
    """Log agent interaction to JSON file.

    Captures complete agent configuration, message history, and metadata
    for evaluation and debugging. Each call creates a single JSON file
    in the LOG_DIR directory.

    Args:
        agent: Pydantic AI agent instance with name, model, system_prompt,
            and toolsets attributes.
        result: AgentRunResult from agent.run() containing output and new_messages().
        source: Query source - "user" (default) or "ai-generated" for synthetic
            test questions.

    Returns:
        Path to the created log file (e.g., logs/faq_agent_20260410_143052_a3f2.json).

    Raises:
        IOError: If log directory cannot be created or file cannot be written.
        AttributeError: If agent lacks required attributes (name, model, toolsets).

    Example:
        >>> result = await faq_agent.run("What is RAG?")
        >>> log_file = log_interaction_to_file(faq_agent, result, source="user")
        >>> print(f"Logged to: {log_file}")
        Logged to: logs/faq_agent_20260410_143052_a3f2.json

    Log file structure:
        {
            "timestamp": "2026-04-10T14:30:52.123456",
            "agent_name": "faq_agent",
            "model": "openai:gpt-4o-mini",
            "system_prompt": "You are a helpful FAQ assistant...",
            "tools": ["text_search", "hybrid_search"],
            "source": "user",
            "messages": [...],
            "response": "RAG stands for..."
        }
    """
    # LOG-03: Extract tools from agent.toolsets
    tools_list: list[str] = []
    for toolset in agent.toolsets:
        tools_list.extend(toolset.keys())  # type: ignore[attr-defined]

    # LOG-02, LOG-08: Capture message history using ModelMessagesTypeAdapter
    messages_dict = ModelMessagesTypeAdapter.dump_python(
        result.new_messages()
    )

    # LOG-01: Build log entry with agent configuration
    # D-14 through D-21: Complete log content structure
    log_entry: dict[str, Any] = {
        "timestamp": datetime.now(),  # Serialized via datetime_serializer
        "agent_name": agent.name,
        "model": str(agent.model),
        "system_prompt": agent.system_prompt,
        "tools": tools_list,
        "source": source,  # LOG-04: Track query source
        "messages": messages_dict,
        "response": result.output,
    }

    # D-11, D-12: Generate unique filename and write to LOG_DIR
    agent_name = agent.name or "unknown_agent"
    filename = generate_log_filename(agent_name)
    log_file = LOG_DIR / filename

    # D-20: Store complete log entry as single JSON file
    with open(log_file, "w") as f:
        json.dump(log_entry, f, indent=2, default=datetime_serializer)

    return log_file
