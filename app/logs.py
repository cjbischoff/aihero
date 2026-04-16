"""Agent interaction logging with environment-based configuration.

This module provides JSON-based logging of Pydantic AI agent interactions
with configuration loaded from environment variables. Each agent.run()
invocation produces a single JSON log file containing the complete
interaction state.

Environment Variables:
    OPENAI_API_KEY: Required - OpenAI API key for agent execution
    LOGS_DIRECTORY: Optional - Log directory path (defaults to 'logs')

Typical usage:
    from logs import log_interaction_to_file, LOG_DIR

    result = await agent.run(question)
    log_file = log_interaction_to_file(agent, result, source="user")
    print(f"Logged to: {log_file}")
"""

import json
import os
import secrets
from datetime import datetime
from pathlib import Path
from typing import Any

from typing import Union

from pydantic_ai import Agent, AgentRunResult
from pydantic_ai.messages import ModelMessagesTypeAdapter
from pydantic_ai.result import StreamedRunResultSync

# Environment variable loading per D-13, D-14, D-15

# REFACTOR-10: Required, no default
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
if not OPENAI_API_KEY:
    raise ValueError(
        "OPENAI_API_KEY environment variable required. "
        "Set in .env file or export in shell."
    )

# REFACTOR-09: Optional with default
LOG_DIR = Path(os.getenv('LOGS_DIRECTORY', 'logs'))
LOG_DIR.mkdir(exist_ok=True)


def serializer(obj: Any) -> str:
    """Custom JSON serializer for datetime objects.

    Converts datetime objects to ISO 8601 format strings for JSON serialization.
    Used as the `default` parameter in json.dump() calls.

    Args:
        obj: Object to serialize (expected to be datetime).

    Returns:
        ISO 8601 formatted string (e.g., "2026-04-15T14:30:52.123456").

    Raises:
        TypeError: If obj is not a datetime object.

    Example:
        >>> import json
        >>> from datetime import datetime
        >>> data = {"timestamp": datetime.now()}
        >>> json.dumps(data, default=serializer)
        '{"timestamp": "2026-04-15T14:30:52.123456"}'
    """
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError(f"Type {type(obj)} not serializable")


def generate_log_filename(agent_name: str) -> str:
    """Generate unique timestamped filename with collision resistance.

    Creates filenames in format: {agent_name}_{YYYYMMDD_HHMMSS}_{hex}.json
    The 4-character hex suffix provides 65K uniqueness per second.

    Args:
        agent_name: Name of the agent (e.g., "faq_agent").

    Returns:
        Filename string (not full path).

    Example:
        >>> generate_log_filename("faq_agent")
        'faq_agent_20260415_143052_a3f2.json'
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    random_suffix = secrets.token_hex(2)
    return f"{agent_name}_{timestamp}_{random_suffix}.json"


def log_interaction_to_file(
    agent: Agent[Any, Any],
    result: Union[AgentRunResult[Any], StreamedRunResultSync[Any]],
    source: str = "user",
) -> Path:
    """Log agent interaction to JSON file.

    Captures complete agent configuration, message history, and metadata
    for evaluation and debugging. Each call creates a single JSON file
    in the LOG_DIR directory.

    Supports both streaming and non-streaming results:
    - AgentRunResult from agent.run() - has .output attribute
    - StreamedRunResultSync from agent.run_stream_sync() - has .get_output() method

    Args:
        agent: Pydantic AI agent instance with name, model, system_prompt,
            and toolsets attributes.
        result: AgentRunResult from agent.run() or StreamedRunResultSync from
            agent.run_stream_sync(), containing output and new_messages().
        source: Query source - "user" (default) or "ai-generated" for synthetic
            test questions.

    Returns:
        Path to the created log file (e.g., logs/faq_agent_20260415_143052_a3f2.json).

    Raises:
        IOError: If log directory cannot be created or file cannot be written.
        AttributeError: If agent lacks required attributes (name, model, toolsets).

    Example:
        >>> # Non-streaming usage
        >>> result = await faq_agent.run("What is RAG?")
        >>> log_file = log_interaction_to_file(faq_agent, result, source="user")
        >>> print(f"Logged to: {log_file}")
        Logged to: logs/faq_agent_20260415_143052_a3f2.json

        >>> # Streaming usage
        >>> result = faq_agent.run_stream_sync(user_prompt="What is RAG?")
        >>> for chunk in result.stream_text():
        ...     print(chunk, end="", flush=True)
        >>> log_file = log_interaction_to_file(faq_agent, result, source="user")

    Log file structure:
        {
            "timestamp": "2026-04-15T14:30:52.123456",
            "agent_name": "faq_agent",
            "model": "openai:gpt-4o-mini",
            "system_prompt": "You are a helpful FAQ assistant...",
            "tools": ["search"],
            "source": "user",
            "messages": [...],
            "response": "RAG stands for..."
        }
    """
    # Extract tools from agent.toolsets
    tools_list: list[str] = []
    for toolset in agent.toolsets:
        # Toolset has function_tools dict attribute
        if hasattr(toolset, 'function_tools'):
            tools_list.extend(toolset.function_tools.keys())
        # Fallback: try to get tool names from functions attribute
        elif hasattr(toolset, 'functions'):
            tools_list.extend(f.name for f in toolset.functions)

    # Capture message history using ModelMessagesTypeAdapter
    messages_dict = ModelMessagesTypeAdapter.dump_python(
        result.new_messages()
    )

    # Extract response text based on result type
    # AgentRunResult has .output attribute, StreamedRunResultSync has .get_output() method
    response_text = result.output if hasattr(result, 'output') else result.get_output()

    # Extract system prompt - agent.system_prompt is a method, actual prompt in _system_prompts
    system_prompt_text = (
        agent._system_prompts[0] if agent._system_prompts else "<dynamic>"
    )

    # Build log entry with agent configuration
    log_entry: dict[str, Any] = {
        "timestamp": datetime.now(),  # Serialized via serializer
        "agent_name": agent.name,
        "model": str(agent.model),
        "system_prompt": system_prompt_text,
        "tools": tools_list,
        "source": source,
        "messages": messages_dict,
        "response": response_text,
    }

    # Generate unique filename and write to LOG_DIR
    agent_name = agent.name or "unknown_agent"
    filename = generate_log_filename(agent_name)
    log_file = LOG_DIR / filename

    # Store complete log entry as single JSON file
    with open(log_file, "w") as f:
        json.dump(log_entry, f, indent=2, default=serializer)

    return log_file
