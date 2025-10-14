import os
import json
import requests
import gradio as gr
import fitz  # PyMuPDF
import tiktoken
import pandas as pd
from docx import Document

OLLAMA_API = "http://localhost:11434/api/generate"
MAX_TOKENS = 1000  # limit context for speed

# --- Read file safely ---
def read_file(file):
    try:
        ext = os.path.splitext(file.name)[1].lower()
        if ext in [".txt", ".md", ".py"]:
            with open(file.name, "r", encoding="utf-8", errors="ignore") as f:
                return f.read()
        elif ext == ".pdf":
            text = ""
            doc = fitz.open(file.name)
            for page in doc:
                text += page.get_text()
            return text
        elif ext == ".docx":
            doc = Document(file.name)
            text = "\n".join([p.text for p in doc.paragraphs])
            return text
        elif ext == ".csv":
            df = pd.read_csv(file.name)
            return df.to_string(index=False)
        else:
            return f"⚠️ Unsupported file type: {ext}"
    except Exception as e:
        return f"❌ Error reading file: {e}"

# --- Truncate large text ---
def truncate_text(text, max_tokens=MAX_TOKENS):
    tokenizer = tiktoken.get_encoding("cl100k_base")
    tokens = tokenizer.encode(text)
    return tokenizer.decode(tokens[:max_tokens])

# --- LLM query with streaming ---
def ask_llm(message, chat_history, file, selected_model):
    context = ""
    if file is not None:
        content = read_file(file)
        if content.startswith("❌") or content.startswith("⚠️"):
            chat_history.append(("User", message))
            chat_history.append(("Assistant", content))
            yield "", chat_history
            return
        context = truncate_text(content) + "\n\n"

    prompt = context + message
    chat_history.append(("User", message))
    chat_history.append(("Assistant", ""))  # placeholder
    result_text = ""

    try:
        with requests.post(
            OLLAMA_API,
            json={"model": selected_model, "prompt": prompt, "stream": True},
            stream=True
        ) as r:
            if r.status_code != 200:
                err = f"❌ Request failed: {r.status_code} {r.text}"
                chat_history[-1] = ("Assistant", err)
                yield "", chat_history
                return

            for line in r.iter_lines():
                if line:
                    s = line.decode("utf-8")
                    if s.startswith("{") and '"response"' in s:
                        try:
                            chunk = json.loads(s)["response"]
                            if chunk:
                                result_text += chunk
                                chat_history[-1] = ("Assistant", result_text)
                                yield "", chat_history
                        except Exception:
                            continue
        if result_text:
            chat_history[-1] = ("Assistant", result_text)
            yield "", chat_history
    except Exception as e:
        chat_history[-1] = ("Assistant", f"❌ Unexpected error: {e}")
        yield "", chat_history

# --- Gradio Chat UI with styling ---
with gr.Blocks(css="""
    body { background-color: #f0f2f5; }
    .chatbot_message.user { background-color: #4a90e2; color: white; border-radius: 12px; padding: 8px; }
    .chatbot_message.assistant { background-color: #e5e5ea; color: black; border-radius: 12px; padding: 8px; }
    #user-input { font-size: 18px; padding: 10px; }
    #send-btn { width: 36px; height: 36px; min-width: 36px; min-height: 36px; padding: 0; }
""") as demo:

    gr.Markdown("## 🧠 Local Multi-Model Chat Assistant", elem_id="header")
    
    with gr.Row():
        file_input = gr.File(label="📄 Upload a file (optional)")
        model_selector = gr.Dropdown(
            label="Choose Model",
            choices=["llama3", "mdq100/Gemma3-Instruct-Abliterated:12b"],
            value="llama3"
        )
    
    chat = gr.Chatbot(label="Conversation")
    
    with gr.Row():
        msg = gr.Textbox(
            placeholder="Type your message here...",
            elem_id="user-input",
            show_label=False
        )
        send = gr.Button("➤", elem_id="send-btn")
    
    send.click(
        ask_llm,
        inputs=[msg, chat, file_input, model_selector],
        outputs=[msg, chat]
    )

if __name__ == "__main__":
    demo.launch()
