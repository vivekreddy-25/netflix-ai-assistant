import re


GENRES = {
    "horror": "horror",
    "romantic": "romance",
    "romance": "romance",
    "comedy": "comedy",
    "action": "action",
    "drama": "drama",
    "thriller": "thriller",
    "sci-fi": "science fiction",
    "science fiction": "science fiction",
    "animation": "animation",
    "animated": "animation",
    "adventure": "adventure",
    "crime": "crime",
    "documentary": "documentary",
    "family": "family",
    "fantasy": "fantasy",
    "history": "history",
    "music": "music",
    "mystery": "mystery",
    "tv movie": "tv movie",
    "tv movies": "tv movie",
    "war": "war",
    "western": "western",
}


def parse_query(user_query, all_countries):

    query = user_query.lower()

    data = {
        "genre": None,
        "year": None,
        "year_filter": "exact",
        "country": None,
        "actor": None,
        "director": None,
        "limit": 5
    }

    for word, genre in GENRES.items():
        if re.search(rf"\b{re.escape(word)}\b", query):
            data["genre"] = genre
            break

    # -------- YEAR --------
    year_match = re.search(r"\b(19|20)\d{2}\b", query)

    if year_match:
        data["year"] = int(year_match.group())

    # -------- YEAR FILTER --------
    if "after" in query:
        data["year_filter"] = "after"

    elif "before" in query:
        data["year_filter"] = "before"

    # -------- COUNTRY --------
    for c in all_countries:
        if c in query:
            data["country"] = c
            break

    # -------- PERSON SEARCH --------
    person_match = re.search(
        r"(with|starring|by)\s+([a-z\s]+?)(?:\s+in|\s+from|\s+after|\s+before|$)",
        query
    )

    if person_match:
        data["actor"] = person_match.group(2).strip()

    director_match = re.search(
        r"\bdirected by\s+([a-z\s]+?)(?:\s+in\b|\s+from\b|\s+after\b|\s+before\b|[?.!,;:]|$)",
        query
    )

    if director_match:
        data["director"] = director_match.group(1).strip()
        data["actor"] = None

    # -------- LIMIT --------
    limit_match = re.search(
        r"(top|show me|give me)\s+(\d+)",
        query
    )

    if limit_match:
        data["limit"] = int(limit_match.group(2))

    return data