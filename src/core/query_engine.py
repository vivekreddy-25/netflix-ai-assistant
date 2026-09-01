def query_movies(
    df,
    genre=None,
    year=None,
    year_filter="exact",
    country=None,
    actor=None,
    director=None,
    limit=5
):
    results = df.copy()

    # -------- YEAR --------
    if year is not None:

        if year_filter == "after":
            results = results[results['release_year'] > year]

        elif year_filter == "before":
            results = results[results['release_year'] < year]

        else:
            results = results[results['release_year'] == year]

    # -------- GENRE --------
    if genre:
        results = results[
            results['genres'].str.contains(genre)
        ]

    # -------- COUNTRY --------
    if country:
        results = results[
            results['country'].apply(lambda x: country in x)
        ]

    # -------- PERSON SEARCH (ACTOR OR DIRECTOR) --------
    if actor:
        results = results[
            results['cast'].str.contains(actor) |
            results['director'].str.contains(actor)
        ]

    # -------- DIRECTOR --------
    if director:
        results = results[
            results['director'].str.contains(director)
        ]

    return results.head(limit)