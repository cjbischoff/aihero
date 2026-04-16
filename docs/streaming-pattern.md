# Pydantic AI Streaming Pattern Documentation

**Date:** 2026-04-16
**Context:** Phase 34 - Streamlit Cloud Deployment
**Purpose:** Document correct streaming patterns and API differences

---

## Overview

Pydantic AI provides two execution patterns with different result types:

1. **Non-streaming** (`agent.run()`) → Returns `AgentRunResult`
2. **Streaming** (`agent.run_stream_sync()`) → Returns `StreamedRunResultSync`

These result types have **incompatible APIs** that require defensive handling in shared code.

---

## API Differences

### AgentRunResult (Non-Streaming)

```python
result = await agent.run(user_prompt="What is RAG?")

# Access final output
response = result.output  # ✓ Attribute access

# Access messages
messages = result.new_messages()  # ✓ Same as streaming
```

### StreamedRunResultSync (Streaming)

```python
result = agent.run_stream_sync(user_prompt="What is RAG?")

# Must consume stream first
for chunk in result.stream_text(debounce_by=0.01):
    print(chunk, end="", flush=True)

# Access final output AFTER streaming completes
response = result.get_output()  # ✓ Method call (not .output attribute)

# Access messages
messages = result.new_messages()  # ✓ Same as non-streaming
```

**Key Difference:** `.output` (attribute) vs `.get_output()` (method)

---

## Correct Streaming Pattern

### Cumulative vs Delta Chunks

**CRITICAL:** `stream_text()` returns **cumulative text**, not deltas.

```python
# ✗ WRONG - Accumulates duplicates
full_response = ""
for chunk in result.stream_text():
    full_response += chunk  # Each chunk already contains full text!

# ✓ CORRECT - Assign, don't accumulate
full_response = ""
for chunk in result.stream_text():
    full_response = chunk  # chunk IS the cumulative text
```

### Complete Streamlit Example

```python
import streamlit as st
from pydantic_ai import Agent

agent = Agent(model="openai:gpt-4o-mini", system_prompt="You are helpful")

# Create placeholder for streaming updates
message_placeholder = st.empty()
full_response = ""

# Run streaming agent
result = agent.run_stream_sync(user_prompt=prompt)

# Display with typewriter effect
for chunk in result.stream_text(debounce_by=0.01):
    full_response = chunk  # Assign cumulative text
    message_placeholder.markdown(full_response + "▌")  # Blinking cursor

# Final update without cursor
message_placeholder.markdown(full_response)

# Add to history
st.session_state.messages.append({"role": "assistant", "content": full_response})
```

---

## Defensive Coding for Shared Functions

When writing functions that accept **both** result types:

### Type Hint

```python
from typing import Union
from pydantic_ai import AgentRunResult
from pydantic_ai.result import StreamedRunResultSync

def log_interaction(
    agent: Agent,
    result: Union[AgentRunResult[Any], StreamedRunResultSync[Any]],
) -> None:
    ...
```

### Response Extraction

```python
# Check which type and extract accordingly
response = result.output if hasattr(result, 'output') else result.get_output()
```

### System Prompt Extraction

**GOTCHA:** `agent.system_prompt` is a **method**, not an attribute!

```python
# ✗ WRONG - Tries to serialize method object
log_entry = {
    "system_prompt": agent.system_prompt,  # <method> - NOT serializable!
}

# ✓ CORRECT - Access private attribute with fallback
system_prompt_text = (
    agent._system_prompts[0] if agent._system_prompts else "<dynamic>"
)
log_entry = {
    "system_prompt": system_prompt_text,  # String - serializable
}
```

---

## Testing Strategy

### Local Testing BEFORE Production

**Never use production as testing environment!**

1. **Create test script:**
   ```python
   # test_streaming.py
   from main import initialize_index, initialize_agent
   from logs import log_interaction_to_file

   index = initialize_index()
   agent = initialize_agent(index)

   # Test streaming
   result = agent.run_stream_sync(user_prompt="Test question")
   for chunk in result.stream_text():
       pass

   # Test logging
   log_file = log_interaction_to_file(agent, result, source="test")
   print(f"✓ Logged to: {log_file}")
   ```

2. **Run locally:**
   ```bash
   export OPENAI_API_KEY="sk-..."
   python test_streaming.py
   ```

3. **Verify log created:**
   ```bash
   ls -lh logs/*.json | tail -1
   cat logs/agent_*.json | jq '.response'
   ```

4. **Test Streamlit locally:**
   ```bash
   streamlit run app.py
   ```

5. **Only push after all tests pass locally**

---

## Common Pitfalls

### Pitfall 1: Using Production as Test Environment
- **Problem:** 6 deployment cycles to fix issues catchable locally
- **Solution:** Test locally with `streamlit run` before pushing

### Pitfall 2: Accumulating Chunks
- **Problem:** Duplicated output (each chunk contains full text)
- **Solution:** Assign chunks, don't accumulate (`=` not `+=`)

### Pitfall 3: Calling .output on Streaming Result
- **Problem:** `AttributeError: 'StreamedRunResultSync' has no .output`
- **Solution:** Use `.get_output()` method for streaming results

### Pitfall 4: Serializing agent.system_prompt
- **Problem:** `TypeError: method not serializable`
- **Solution:** Access `agent._system_prompts[0]` for actual string

### Pitfall 5: Logging Before Stream Consumption
- **Problem:** Output incomplete if logged mid-stream
- **Solution:** Consume entire stream before calling `.get_output()`

---

## Verification Checklist

Before marking streaming implementation complete:

- [ ] Streaming displays correctly (no duplicates)
- [ ] Blinking cursor shows during streaming
- [ ] Final text displayed without cursor
- [ ] Logging creates valid JSON files
- [ ] Log contains correct response text
- [ ] Log contains message history
- [ ] All tested **locally** before production push
- [ ] No errors in Streamlit Cloud logs

---

## References

- **Pydantic AI Docs:** https://ai.pydantic.dev/
- **Issue Context:** Phase 34 execution (6 production deployments to fix streaming bugs)
- **Test Script:** Created `test_streaming_log.py` for local verification
- **Files Modified:** `app.py`, `logs.py`

---

## Lessons Learned

1. **Research First:** Should have read pydantic-ai docs before implementing
2. **Test Locally:** Never use production as testing environment
3. **TDD Approach:** Write tests, verify locally, then deploy
4. **API Assumptions:** Don't assume APIs work like you expect - verify first
5. **Defensive Coding:** Use `hasattr()` for compatibility with multiple types
