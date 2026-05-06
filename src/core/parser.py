import re

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

    # -------- GENRE --------
    if "horror" in query:
        data["genre"] = "horror"

    elif "romance" in query or "romantic" in query:
        data["genre"] = "romance"

    elif "comedy" in query:
        data["genre"] = "comedy"

    elif "action" in query:
        data["genre"] = "action"

    elif "drama" in query:
        data["genre"] = "drama"

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

    # -------- LIMIT --------
    limit_match = re.search(
        r"(top|show me|give me)\s+(\d+)",
        query
    )

    if limit_match:
        data["limit"] = int(limit_match.group(2))

    return data