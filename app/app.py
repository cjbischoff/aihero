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
        with st.chat_message("assistant"):
            # Create placeholder for streaming text
            message_placeholder = st.empty()
            full_response = ""

            # Stream response chunks (stream_text returns cumulative text, not deltas)
            result = agent.run_stream_sync(user_prompt=prompt)
            for chunk in result.stream_text(debounce_by=0.01):
                full_response = chunk  # chunk is cumulative, not delta
                message_placeholder.markdown(full_response + "▌")

            # Final update without cursor
            message_placeholder.markdown(full_response)

        # Add assistant message to history
        st.session_state.messages.append({"role": "assistant", "content": full_response})

        # Log interaction (supports both streaming and non-streaming results)
        log_interaction_to_file(agent, result, source="user")


if __name__ == "__main__":
    main()
