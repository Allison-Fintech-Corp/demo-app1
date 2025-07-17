# Allison Chat Demo

This project is a lightweight, local-only chat demo for Axiom Bank, powered by Gemini and Streamlit.

## Setup & Launch

### 0. Set API Key
Set your Gemini API key once per shell session:
```bash
export GEMINI_API_KEY="YOUR_GEMINI_2_5_KEY"
```

### 1. Install Dependencies
Create a virtual environment and install the required packages:
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Run Backend & MCP Wrapper
In your first terminal, run the following command. This will start the fake banking API and wrap it with the MCP agent. **Leave this terminal open.**
```bash
./mcp_start.sh
```

### 3. Launch the Chat UI
In a second terminal, launch the Streamlit front-end:
```bash
streamlit run allison_chat.py
```
Now open your browser to `http://localhost:8501`.

### (Optional) Share Publicly
If you need to share the demo, you can use a tunneling service like ngrok:
```bash
ngrok http 8501
