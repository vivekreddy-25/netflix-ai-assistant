import json
import time
from pathlib import Path

import pandas as pd

from src.core.pipeline import run_pipeline


def evaluate():
    evaluation_dir = Path(__file__).resolve().parent

    with (evaluation_dir / "test_cases.json").open(encoding="utf-8") as f:
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
                    case=False,
                    na=False,
                    regex=False
                ).all():
                    success = False

            # -------- COUNTRY --------
            if "country" in expected:
                def check_country(country_list):
                    return expected["country"].lower() in country_list

                if not result["country"].apply(check_country).all():
                    success = False

            # -------- YEAR --------
            if "year" in expected:
                year = expected["year"]
                year_filter = expected.get("year_filter", "exact")
                if year_filter == "after":
                    year_matches = result["release_year"] > year
                elif year_filter == "before":
                    year_matches = result["release_year"] < year
                else:
                    year_matches = result["release_year"] == year

                if not year_matches.all():
                    success = False

            # -------- PERSON --------
            if "person" in expected:
                found = (
                    result["cast"].str.contains(
                        expected["person"],
                        case=False,
                        na=False,
                        regex=False
                    ) |
                    result["director"].str.contains(
                        expected["person"],
                        case=False,
                        na=False,
                        regex=False
                    )
                )

                if not found.all():
                    success = False

            # -------- DIRECTOR --------
            if "director" in expected:
                if not result["director"].str.contains(
                    expected["director"],
                    case=False,
                    na=False,
                    regex=False
                ).all():
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

    accuracy = round((passed / total) * 100, 2) if total else 0.0

    print(f"\nFINAL SCORE: {passed}/{total}")
    print(f"Accuracy: {accuracy}%")

    with (evaluation_dir / "results.json").open("w", encoding="utf-8") as f:
        json.dump(
            {
                "accuracy": accuracy,
                "passed": passed,
                "total": total,
                "results": rows
            },
            f,
            indent=2
        )

    return pd.DataFrame(rows), accuracy