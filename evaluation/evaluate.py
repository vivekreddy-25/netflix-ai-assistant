import json
import time
import pandas as pd

from src.core.pipeline import run_pipeline

def evaluate():

    with open("evaluation/results.json") as f:
        data = json.load(f)

    total = 0
    passed = 0

    rows = []

    for case in data["results"]:

        query = case["query"]
        expected = case["expected"]

        print(f"\nTesting: {query}")

        start = time.time()

        result = run_pipeline(query)

        end = time.time()

        elapsed = round(end - start, 3)

        total += 1

        success = False

        if isinstance(result, pd.DataFrame) and not result.empty:

            success = True

            # -------- GENRE --------
            if "genre" in expected:
                if not result["genres"].str.contains(
                    expected["genre"],
                    case=False
                ).any():
                    success = False

            # -------- COUNTRY --------
            if "country" in expected:

                def check_country(country_list):
                    return expected["country"].lower() in country_list

                if not result["country"].apply(check_country).any():
                    success = False

            # -------- YEAR --------
            if "year" in expected:
                if not (result["release_year"] == expected["year"]).any():
                    success = False

            # -------- PERSON --------
            if "person" in expected:

                found = (
                    result["cast"].str.contains(
                        expected["person"],
                        case=False
                    ).any()
                    or
                    result["director"].str.contains(
                        expected["person"],
                        case=False
                    ).any()
                )

                if not found:
                    success = False

        if success:
            passed += 1
            status = "PASS"
        else:
            status = "FAIL"

        rows.append({
            "query": query,
            "success": success,
            "time_sec": elapsed,
            "status": status
        })

    accuracy = round((passed / total) * 100, 2)

    print(f"\nFINAL SCORE: {passed}/{total}")
    print(f"Accuracy: {accuracy}%")

    return pd.DataFrame(rows), accuracy