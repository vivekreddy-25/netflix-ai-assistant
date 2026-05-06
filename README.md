#  Netflix AI Assistant

Netflix AI Assistant is a hybrid AI-powered movie retrieval system that allows users to search movies using natural language queries.

The system combines:

-  Fast structured filtering using Pandas
-  Semantic retrieval using RAG (FAISS + embeddings)

---

#  Features

- Search movies by:
  - Genre
  - Year
  - Country
  - Actor
  - Director

- Natural language query support
- Exact year filtering
- Smart actor/director matching
- Evaluation dashboard
- Fast response time
- RAG-ready architecture

---

#  System Architecture

```text
User Query
    ↓
Parser
    ↓
Structured Parameters
    ↓
Query Engine
    ↓
Movie Results
```

Optional semantic queries use:

```text
Embeddings → FAISS → RAG Retrieval
```

---

#  Project Structure

```text
netflixagent/
│
├── data/
├── evaluation/
├── src/
│   ├── core/
│   ├── rag/
│   └── utils/
│
├── web_app.py
├── requirements.txt
├── Dockerfile
├── README.md
└── pyproject.toml
```

---

#  Installation

Install dependencies:

```bash
pip install -r requirements.txt
```

Run Streamlit app:

```bash
streamlit run web_app.py
```

---

#  Evaluation

The project includes an evaluation dashboard to measure:

- Accuracy
- Query success rate
- Average response time

---

#  Technologies Used

- Python
- Streamlit
- Pandas
- FAISS
- Sentence Transformers
- Ollama

---

#  Example Queries

```text
top 5 horror movies in 2022
romantic movies from france
movies with tom cruise
movies with christopher nolan in 2023
```

---

# Author
Vivek Macharla