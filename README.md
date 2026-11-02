#  Netflix AI Assistant

Netflix AI Assistant is a hybrid AI-powered movie retrieval system that allows users to search movies using natural language queries.

The system combines:

-  Fast structured filtering using Pandas
-  Semantic retrieval for free-form queries using RAG (FAISS + embeddings)

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
- Semantic fallback for queries without structured filters

---

#  System Architecture

```text
User Query
    ↓
Parser
    ├── Structured parameters → Pandas query engine → Movie results
    └── No structured parameters → FAISS semantic retrieval → Text matches
```

The first semantic query builds a FAISS index over the full dataset and saves it
under `vectorstore/`. Indexing can take several minutes depending on hardware;
later queries reuse the local index.

---

#  Project Structure

```text
netflix-ai-assistant/
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
├── README.md
└── pyproject.toml
```

---

# Dataset

The [Movies_dataset.csv](https://raw.githubusercontent.com/vivekreddy-25/netflix-ai-assistant/main/data/Movies_dataset.csv)
file is about 7.8 MB and can be downloaded directly. The repository does not
record the dataset's upstream source or license, so its redistribution terms
could not be verified. Check the original source's terms before reusing or
redistributing the data.

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

Cases are read from `evaluation/test_cases.json`; each evaluation run writes its
summary and per-query results to `evaluation/results.json`.

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