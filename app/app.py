"""Streamlit web interface for FAQ agent.

This module provides a chat-based web interface using Streamlit components
with streaming responses, conversation history, and cached agent initialization.

Usage:
    streamlit run app.py

Environment Variables:
    OPENAI_API_KEY: Required - Loaded automatically via logs.py import
    LOGS_DIRECTORY: Optional - Directory for interaction logs (default: 'logs')
"""

import streamlit as st
from pydantic_ai import Agent

from main import (
    initialize_index,
    initialize_agent,
    DEFAULT_REPO_OWNER,
    DEFAULT_REPO_NAME,
)
from logs import log_interaction_to_file


@st.cache_resource
def get_agent() -> Agent:
    """Initialize agent once and cache globally across all sessions.

    Uses @st.cache_resource to prevent re-initialization on every Streamlit
    rerun. The agent is stateless (conversation history stored in session_state),
    so a single cached instance can be shared across all users.

    Returns:
        Configured pydantic-ai Agent ready for run_stream_sync() calls.

    Note:
        Initialization takes 5-10 seconds (downloads FAQ repo, builds index).
        This only happens once per Streamlit server restart.
    """
    with st.spinner("Loading FAQ data and initializing agent..."):
        index = initialize_index()
        agent = initialize_agent(index)
    return agent


def main() -> None:
    """Streamlit application entry point.

    Implements:
    - Chat interface with message display and input box (UI-01)
    - Streaming responses with typewriter effect (UI-02)
    - Agent cached globally via @st.cache_resource (UI-03)
    - Conversation history persists via st.session_state (UI-04)
    - User and assistant messages styled correctly (UI-05)
    - History persists across interactions (UI-06)
    - Loading spinner during initialization (UI-07)
    - Fresh session handling with empty state (UI-08)
    """
    # Page configuration (UI-01)
    st.set_page_config(
        page_title="FAQ Agent",
        page_icon="🤖",
        layout="centered",
    )

    # Title and repository info
    st.title("FAQ Agent")
    st.caption(f"Repository: {DEFAULT_REPO_OWNER}/{DEFAULT_REPO_NAME}")

    # Initialize agent once (UI-03, UI-07)
    agent = get_agent()

    # Initialize session state for conversation history (UI-04, UI-08)
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display message history (UI-05, UI-06)
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # User input and streaming response (UI-01, UI-02)
    if prompt := st.chat_input("Ask a question about the course"):
        # Add user message to history
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)

        # Stream assistant response with logging
        # Use nonlocal to capture final result for logging after streaming
        final_result = None

        def stream_and_log():
            """Stream agent response and capture final result for logging.

            Yields text chunks for st.write_stream() display with smooth
            typewriter effect (debounce_by=0.01 for 10ms updates).

            The final AgentRunResult is captured via nonlocal after streaming
            completes, enabling log_interaction_to_file() call outside generator.
            """
            nonlocal final_result
            with agent.run_stream_sync(user_prompt=prompt) as result:
                for chunk in result.stream_text(debounce_by=0.01):
                    yield chunk
                # After streaming completes, get final result for logging
                final_result = result.get_result_sync()

        # Display streaming response
        with st.chat_message("assistant"):
            response = st.write_stream(stream_and_log())

        # Add assistant message to history
        st.session_state.messages.append({"role": "assistant", "content": response})

        # Log interaction if final result captured
        if final_result:
            log_interaction_to_file(agent, final_result, source="user")


if __name__ == "__main__":
    main()
