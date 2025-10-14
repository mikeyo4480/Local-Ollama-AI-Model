# Local LLM Assistant

This repository contains a local Python-based assistant that supports multi-model chat, file uploads, and a simple web interface using Gradio.

> Note: Do not commit any `.env` files with API keys or other secrets. The `.gitignore` file is included to prevent accidental commits.

---

## Repository Contents

- `.gitignore` – ignores unnecessary and sensitive files such as virtual environments and secrets.  
- `docker-compose.yml` – optional setup for running the assistant in Docker.  
- `example.txt` – example input file for testing file uploads.  
- `index.html` – optional frontend file.  
- `rag_basic.py` – main Python script for the assistant.

---

## Prerequisites

1. Python 3.11 or higher  
2. Pip package manager  
3. Ollama installed and running locally for the LLM models  
4. Optional: Docker for running via `docker-compose`

---

## Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name

2. Create and activate a virtual environment

# Windows
python -m venv venv
.\venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate

3. Install dependencies

pip install gradio PyMuPDF tiktoken pandas python-docx requests python-dotenv

4. Pull LLM models in Ollama

ollama pull llama3
ollama pull mdq100/Gemma3-Instruct-Abliterated:12b

5. Run the assistant

python rag_basic.py


