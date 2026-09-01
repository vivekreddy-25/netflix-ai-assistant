from src.core.pipeline import run_pipeline
import pandas as pd

def main():
    print("Netflix AI Recommender (type 'exit' to quit)\n")

    while True:
        query = input("Enter your query: ")

        if query.lower() == "exit":
            break

        results = run_pipeline(query)

        print("\n Results:\n")

        #  If it's a DataFrame
        if isinstance(results, pd.DataFrame):
            if results.empty:
                print(" No results found.\n")
            else:
                for _, row in results.iterrows():
                    print(f"- {row['title']} ({int(row['release_year'])}) | {row['genres']}")
                print()

        # If it's a string (RAG output)
        else:
            print(results)
            print()


if __name__ == "__main__":
    main()