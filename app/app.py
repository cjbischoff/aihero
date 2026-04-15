"""Streamlit entry point for FAQ agent.

This module provides web interface for the FAQ agent.
Full UI implementation in Phase 33.

Usage:
    streamlit run app.py
"""

import streamlit as st


# D-11, D-12: Default repository (same as main.py)
DEFAULT_REPO_OWNER = "DataTalksClub"
DEFAULT_REPO_NAME = "faq"


def main() -> None:
    """Streamlit application entry point.

    Phase 33 will implement full UI with:
    - st.session_state for conversation history
    - st.chat_message for message display
    - run_stream() for streaming responses
    - @st.cache_resource for agent initialization

    For now, this is a placeholder stub.
    """
    st.set_page_config(
        page_title="FAQ Agent",
        page_icon="🤖",
        layout="centered",
    )

    st.title("FAQ Agent")
    st.write(f"Repository: {DEFAULT_REPO_OWNER}/{DEFAULT_REPO_NAME}")
    st.info("Full Streamlit UI implementation in Phase 33")

    # Phase 33 will add:
    # - @st.cache_resource for agent initialization
    # - st.session_state for conversation history
    # - st.chat_input for user questions
    # - st.chat_message for displaying conversation
    # - Streaming responses with agent.run_stream()


if __name__ == "__main__":
    main()
