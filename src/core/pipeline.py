from functools import lru_cache

from src.core.ingest import load_data
from src.core.query_engine import query_movies
from src.core.parser import parse_query

# -----------------------------
# LOAD DATA (module-level, loaded once on import)
# -----------------------------
df = load_data()

# -----------------------------
# EXTRACT COUNTRIES
# -----------------------------
all_countries = set()

for country_list in df['country']:
    all_countries.update(country_list)

# -----------------------------
# MAIN PIPELINE
# -----------------------------
@lru_cache(maxsize=1)
def _load_rag_index():
    from src.rag.retriever import build_index, load_index

    index, texts = load_index()
    if index is None:
        index, texts = build_index(df)

    return index, texts


def run_pipeline(user_query):
    params = parse_query(user_query, all_countries)

    if not any(
        params.get(key)
        for key in ("genre", "year", "country", "actor", "director")
    ):
        from src.rag.retriever import retrieve

        index, texts = _load_rag_index()
        return "\n".join(retrieve(index, texts, user_query, k=5))

    results = query_movies(
        df,
        genre=params.get("genre"),
        year=params.get("year"),
        year_filter=params.get("year_filter"),
        country=params.get("country"),
        actor=params.get("actor"),
        director=params.get("director"),
        limit=params.get("limit", 5)
    )

    if results.empty:
        if params.get("year"):
            return f" No movies found for year {params['year']}."
        return " No matching movies found."

    return results