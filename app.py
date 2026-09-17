import asyncio
import streamlit as st
from agent import ask_agent


# Page configuration
st.set_page_config(
    page_title="AI News Agent",
    page_icon="🤖",
    layout="centered"
)


# Header
st.title("🤖 AI News Agent")

st.markdown(
    "AI research assistant powered by **Gemini + MCP**"
)

st.divider()


# User input
st.subheader("Ask the Agent")

question = st.text_area(
    "What would you like to know?",
    placeholder="Example: What are the latest AI developments?",
    height=100
)


# Run Agent
if st.button("🔍 Ask Agent", use_container_width=True) and question:

    with st.spinner("Agent is working..."):

        answer, activity = asyncio.run(
            ask_agent(question)
        )


    # Agent activity
    with st.expander("🔍 Agent Activity", expanded=True):

        for item in activity:
            st.write(item)


    st.divider()


    # Answer
    st.subheader("📝 AI Summary")

    st.write(answer)