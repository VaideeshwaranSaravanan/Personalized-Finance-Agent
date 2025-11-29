import streamlit as st
import asyncio
import nest_asyncio
nest_asyncio.apply()

from MainAgent import FinanceMainAgent

# -------------------------------------------------
# Light Theme Styling
# -------------------------------------------------
LIGHT_CSS = """
<style>

html, body, .stApp {
    background-color: #FAFAFA !important;
    color: #1B1B1B !important;
    font-family: 'Inter', sans-serif;
}

/* Title */
.title {
    font-size: 34px !important;
    color: #1A73E8 !important;
    font-weight: 800 !important;
    text-align: center;
    margin-bottom: -5px;
}

.subtitle {
    font-size: 16px !important;
    color: #5f6368 !important;
    text-align: center;
    margin-bottom: 25px;
}

/* Chat container */
.chat-container {
    display: flex;
    flex-direction: column;
    padding: 20px 40px;
}

/* User bubble */
.user-msg {
    background-color: #E8F0FE;
    color: #1B1B1B;
    padding: 12px 16px;
    border-radius: 18px;
    margin: 8px 0;
    max-width: 100%;
    align-self: flex-end;
    box-shadow: 0 1px 3px rgba(0,0,0,0.08);
}

/* Bot bubble */
.bot-msg {
    background-color: #FFFFFF;
    color: #1B1B1B;
    padding: 12px 16px;
    border-radius: 18px;
    margin: 8px 0;
    max-width: 100%;
    align-self: flex-start;
    border: 1px solid #E5E5E5;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05);
}

</style>
"""

# Inject CSS
st.markdown(LIGHT_CSS, unsafe_allow_html=True)

# -------------------------------------------------
# Title
# -------------------------------------------------
st.markdown("<h1 class='title'>AI Financial Assistant</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Multi-Agent Orchestrated Finance Intelligence</p>", unsafe_allow_html=True)


# -------------------------------------------------
# Initialize agent & chat history
# -------------------------------------------------
if "finance_agent" not in st.session_state:
    st.session_state.finance_agent = FinanceMainAgent()

if "messages" not in st.session_state:
    st.session_state.messages = []


# -------------------------------------------------
# Chat display area
# -------------------------------------------------
chat_box = st.container()

with chat_box:
    st.markdown("<div class='chat-container'>", unsafe_allow_html=True)

    # Render chat so far
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(
                f"<div class='user-msg'>🧑‍💼 {msg['text']}</div>",
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f"<div class='bot-msg'>🤖 {msg['text']}</div>",
                unsafe_allow_html=True,
            )

    st.markdown("</div>", unsafe_allow_html=True)



# -------------------------------------------------
# Chat input
# -------------------------------------------------
user_input = st.chat_input("Ask me a financial question…")


if user_input:

    # 1️⃣ Immediately show the user message
    st.session_state.messages.append({"role": "user", "text": user_input})

    # Re-render chat so user message appears above the loader
    st.rerun()


# -------------------------------------------------
# Handle the thinking loader AFTER rerun
# -------------------------------------------------
if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":

    last_user_msg = st.session_state.messages[-1]["text"]

    # 2️⃣ Create placeholder UNDER the user message
    loader_placeholder = st.empty()
    loader_placeholder.markdown(
        "<div class='bot-msg'><i>🤖 Thinking…</i></div>",
        unsafe_allow_html=True,
    )

    # 3️⃣ Call backend async agent
    async def get_finance_response(query):
        agent = st.session_state.finance_agent
        buffer = []

        async def capture():
            import sys
            from io import StringIO

            backup = sys.stdout
            sys.stdout = temp = StringIO()

            await agent.run_session(
                user_queries=query,
                session_name="stateful-finance-session"
            )

            sys.stdout = backup
            buffer.append(temp.getvalue().strip())

        await capture()
        return buffer[0]

    # Process the model response
    model_raw_output = asyncio.run(get_finance_response(last_user_msg))
    cleaned_response = model_raw_output.split(">")[-1].strip()

    # 4️⃣ Replace loader with final answer
    loader_placeholder.markdown(
        f"<div class='bot-msg'>🤖 {cleaned_response}</div>",
        unsafe_allow_html=True,
    )

    # 5️⃣ Save to full chat history
    st.session_state.messages.append({"role": "bot", "text": cleaned_response})

    # 6️⃣ Rerender UI cleanly
    st.rerun()