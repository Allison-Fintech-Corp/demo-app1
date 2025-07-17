"""
Allison Chat – Streamlit front‑end + Gemini 2.5 + MCP stub
Launch with:  streamlit run allison_chat.py
"""
import os, re, json, requests, streamlit as st
import google.generativeai as genai

# ---------------------------------------------------------------------
# CONFIG
# ---------------------------------------------------------------------
GEMINI_MODEL  = "gemini-2.5-pro"
MCP_BALANCE   = "http://localhost:8001/balance"   # stub endpoint
LOGO_PATH     = "static/allison_logo.png"         # drop your PNG here
ALLY_BLUE     = "#0041ff"                         # branding accent

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# ---------------------------------------------------------------------
# PAGE STYLES
# ---------------------------------------------------------------------
st.set_page_config(page_title="Allison Chat", layout="centered")
st.markdown(
    f"""
    <style>
      .stChatMessage.user {{background-color:#f0f2f6}}
      .stChatMessage.assistant {{background-color:{ALLY_BLUE}20}}
      .stChatMessage .content {{font-size:15px; line-height:1.6}}
      footer {{visibility:hidden}}
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------------------
with st.sidebar:
    if os.path.exists(LOGO_PATH):
        st.image(LOGO_PATH, use_column_width=True)
    st.markdown("### Axiom Bank × Allison demo")
    st.markdown(
        """
        **Try these prompts**  
        • *What’s the balance of account 123?*  
        • *Show yesterday’s total overdraft exposure.*  
        """
    )

# ---------------------------------------------------------------------
# CHAT MEMORY
# ---------------------------------------------------------------------
if "history" not in st.session_state:
    st.session_state.history = []

for role, msg in st.session_state.history:
    with st.chat_message(role):
        st.markdown(msg)

# ---------------------------------------------------------------------
# USER INPUT
# ---------------------------------------------------------------------
prompt = st.chat_input("Ask me anything about your bank…")
if prompt:
    st.session_state.history.append(("user", prompt))
    with st.chat_message("user"):
        st.markdown(prompt)

    # ---------- TOOL CALL (balance) ----------
    tool_result = {}
    if re.search(r"\b(balance|account)\b", prompt, re.I):
        acct_match = re.search(r"\b\d+\b", prompt)
        acct = acct_match.group() if acct_match else "123"
        try:
            tool_result = requests.post(MCP_BALANCE, json={"account": acct}).json()
        except requests.exceptions.ConnectionError:
            tool_result = {"error": "core service offline"}

    # ---------- GEMINI CALL ----------
    system_msg = (
        "You are Allison, a banking copilot. "
        "If 'tool_result' is provided, include it in your answer.\n\n"
        f"tool_result:\n{json.dumps(tool_result)}"
    )

    model = genai.GenerativeModel(GEMINI_MODEL)
    chat = model.start_chat(history=[{"role": "system", "parts": [system_msg]}])
    response = chat.send_message(prompt).text

    # ---------- SHOW ASSISTANT ----------
    st.session_state.history.append(("assistant", response))
    with st.chat_message("assistant"):
        st.markdown(response)
