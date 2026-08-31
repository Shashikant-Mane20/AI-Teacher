# # AI Teacher Backend

# This is the initial FastAPI backend for the AI Teacher challenge project.

# ## Features included

# - FastAPI app structure

# - API for documents, lessons, students, assessments

# - WebSocket lesson channel

# - Initial schemas and service layer

# - Project structure for future RAG, LLM, video, and voice modules

# ## Run locally

# Use Python 3.11 or 3.12 for best compatibility on Windows. Avoid Python 3.14 for this setup.

# ```bash

# cd backend

# py -3.11 -m venv .venv

# .venv\Scripts\activate

# pip install --upgrade pip

# pip install -r requirements.txt

# uvicorn app.main:app --reload

# ```

# ## API base URL

# ```text

# http://localhost:8000

# ```

# ## Health check

# ```bash

# curl http://localhost:8000/health

# ```
