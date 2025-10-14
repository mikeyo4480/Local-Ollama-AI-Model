# Local LLM Assistant

This repository contains a local Python-based assistant that supports multi-model chat, file uploads, and a simple web interface using Gradio.

> **Note:** Do not commit any `.env` files with API keys or other secrets. The `.gitignore` file is included to prevent accidental commits.

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
Windows:

bash
Copy code
python -m venv venv
.\venv\Scripts\activate
macOS / Linux:

bash
Copy code
python3 -m venv venv
source venv/bin/activate
3. Install dependencies
bash
Copy code
pip install gradio PyMuPDF tiktoken pandas python-docx requests python-dotenv
4. Pull LLM models in Ollama
bash
Copy code
ollama pull llama3
ollama pull mdq100/Gemma3-Instruct-Abliterated:12b
Adjust these commands if you want to use different models.

5. Run the assistant
bash
Copy code
python rag_basic.py
The Gradio interface will provide a local URL (e.g., http://127.0.0.1:7860) that you can open in a browser.

You can upload files (TXT, MD, PY, PDF, DOCX, CSV) and chat with the models.

Security Notes
Keep .env files local and do not commit them.

Do not push large model files or virtual environment directories.

Use .gitignore to prevent sensitive or unnecessary files from being pushed.

Consider using a private repository for sensitive projects.

Optional Docker Setup
You can run the assistant with Docker:

bash
Copy code
docker-compose up
Ensure the ports in docker-compose.yml match the Gradio script (default is 7860).

Docker allows running the assistant without setting up Python locally.

Example Usage
Upload a file in the interface (for example, example.txt).

Type a message in the chat box.

Select a model.

Click send. The response will appear in the chat window.

Managing API Keys (Optional)
If you plan to integrate APIs in the future:

Create a .env file (do not commit it).

Add your keys, for example:

env
Copy code
OPENAI_API_KEY=your_key_here
Load the keys in Python:

python
Copy code
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
This ensures secrets are never exposed in the repository.

yaml
Copy code

---

I can also make a **matching `.gitignore`** that’s ready to go, ignoring `.env`, virtual environments, model files, and Docker data volumes. That way your GitHub repo stays completely safe.  

Do you want me to create that `.gitignore` next?
