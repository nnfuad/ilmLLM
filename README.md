# ilmLLM

ilmLLM is a locally scalable, industry-level chatbot designed to be integrable into any software system. It uses an API-first approach (FastAPI) allowing any client to communicate with the core LangChain/LangGraph logic. The project is designed to run language models locally (via Ollama) ensuring data privacy and zero API costs.

## Architecture
- **Backend**: FastAPI (Python)
- **AI Orchestration**: LangChain & LangGraph
- **Local Model Provider**: Ollama
- **Database / Memory**: SQLite (via SQLAlchemy and LangChain abstractions)
- **Frontend / Testing UI**: Streamlit

## How to Run

### 1. Prerequisites
1. **Python 3.10+**: Ensure Python is installed.
2. **Ollama**: Download and install Ollama from [ollama.com](https://ollama.com/).
3. Pull a model via Ollama (e.g., Llama 3):
   ```bash
   ollama run llama3
   ```

### 2. Setup the Environment
Clone the repository and install dependencies:
```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
pip install -r requirements.txt
```

### 3. Run the Backend API
Start the FastAPI server:
```bash
uvicorn backend.main:app --reload
```
The API will be available at `http://localhost:8000`. You can view the Swagger documentation at `http://localhost:8000/docs`.

### 4. Run the Testing Frontend
In a new terminal (with the virtual environment activated), run the Streamlit app:
```bash
streamlit run frontend/app.py
```

## Tools You Should Know to Build This From Scratch
If you want to build this on your own, here is a list of tools/frameworks you should be familiar with:
- Python (Programming Language)
- FastAPI (REST API Framework)
- Uvicorn (ASGI Web Server)
- LangChain (LLM Application Framework)
- LangGraph (Agentic Workflow Framework)
- Ollama (Local LLM Runner)
- Streamlit (Rapid UI Prototyping)
- SQLite / SQLAlchemy (Database & ORM)
- Git & GitHub (Version Control)
