import streamlit as st
import pandas as pd

from src.core.pipeline import run_pipeline
from evaluation.evaluate import evaluate

st.set_page_config(layout="wide")

st.title("🎬 Netflix AI Assistant")

tab1, tab2 = st.tabs(["🔍 Search", "📊 Evaluation"])

# -----------------------------
# SEARCH TAB
# -----------------------------
with tab1:

    query = st.text_input("Ask about movies:")

    if st.button("Search"):

        with st.spinner("Searching..."):
            result = run_pipeline(query)

        if isinstance(result, pd.DataFrame):
            if result.empty:
                st.warning("No results found.")
            else:
                st.success(f"Found {len(result)} movies")
                st.dataframe(result)
        else:
            st.write(result)

# -----------------------------
# EVALUATION TAB
# -----------------------------
with tab2:

    st.subheader("📊 Evaluation Dashboard")

    if st.button("Run Evaluation"):

        with st.spinner("Running tests..."):
            results, accuracy = evaluate()

        df = pd.DataFrame(results)

        st.dataframe(df)

        st.metric("Accuracy (%)", accuracy)
        st.metric("Avg Time (sec)", round(df["time_sec"].mean(), 3))