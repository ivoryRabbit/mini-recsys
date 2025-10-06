import streamlit as st


def home():
    st.title("Welcome to Mini-RecSys 👋")

    st.markdown(
        """
        Mini-RecSys is a random-walk based recommendation system with Python.

        **👈 Select a demo from the menu on the left**

        ### Dependency
        - FastAPI
        - Streamlit
        - NetworkX
        - DuckDB

        ### Reference
        - [Pixie: A System for Recommending 3+ Billion Items to 200+ Million Users in Real-Time](https://arxiv.org/pdf/1711.07601.pdf)
        """
    )
