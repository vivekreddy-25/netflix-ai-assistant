import pandas as pd

def load_data():
    df = pd.read_csv("data/Movies dataset.csv")

    # -------- YEAR CLEAN --------
    df['release_year'] = pd.to_numeric(df['release_year'], errors='coerce')
    df = df[df['release_year'].notna()]
    df['release_year'] = df['release_year'].astype(int)

    # -------- TEXT CLEAN --------
    df['genres'] = df['genres'].fillna("").str.lower()
    df['cast'] = df['cast'].fillna("").str.lower()
    df['director'] = df['director'].fillna("").str.lower()

    # -------- COUNTRY → LIST --------
    df['country'] = df['country'].fillna("").apply(
        lambda x: [c.strip().lower() for c in x.split(",") if c.strip()]
    )

    return df