import pandas as pd
import streamlit as st
from requests import Session

from config.client import backend_url


def popular_movies(session: Session = Session()):
    st.title("Popular Movies")

    @st.cache_data
    def get_all_genres():
        genre_url = f"{backend_url}/genre/all"
        return session.get(genre_url).json()

    def request_recommend():
        if st.session_state["genre"] == "All":
            genre = None
        else:
            genre = st.session_state["genre"]

        url = f"{backend_url}/rec/movie/popular"
        params = {"genre": genre, "size": 10}

        response = session.get(url, params=params)

        if response.status_code == 200:
            data = response.json()
        else:
            data = None
        return data

    col1, _ = st.columns([2, 8])

    with col1:
        st.selectbox("👇 Choose a genre", ["All"] + get_all_genres(), key="genre")

    result = request_recommend()

    if result is None:
        st.stop()
        return

    col1, col2 = st.columns([1, 1])

    with col1:
        fields = ["id", "title", "year", "view"]

        st.subheader("[Most Viewed Movies]")
        st.data_editor(
            pd.DataFrame(result["view"])[fields],
            column_config={
                "id": st.column_config.Column(
                    "Movie ID",
                    help="ID of movie",
                    width="small",
                    required=True,
                ),
                "title": st.column_config.Column(
                    "Title",
                    help="Title of movie",
                    width="medium",
                ),
                "year": st.column_config.TextColumn(
                    "Release",
                    help="Movie release year",
                    width="small",
                    max_chars=4,
                    validate=r"^\d{4}$",
                ),
                "view": st.column_config.ProgressColumn(
                    "View Count",
                    help="Count of total view",
                    width="medium",
                    format="%f",
                    min_value=0,
                    max_value=result["view"][0]["view"],
                ),
            },
            disabled=fields,
            hide_index=True,
            width=800,
            key="view"
        )

    with col2:
        fields = ["id", "title", "year", "rating"]

        st.subheader("[High Rated Movies]")
        st.data_editor(
            pd.DataFrame(result["rating"])[fields],
            column_config={
                "id": st.column_config.Column(
                    "Movie ID",
                    help="ID of movie",
                    width="small",
                    required=True,
                ),
                "title": st.column_config.Column(
                    "Title",
                    help="Title of movie",
                    width="medium",
                ),
                "year": st.column_config.TextColumn(
                    "Release",
                    help="Movie release year",
                    width="small",
                    max_chars=4,
                    validate=r"^\d{4}$",
                ),
                "rating": st.column_config.ProgressColumn(
                    "Avg Rating",
                    help="Average of rating",
                    width="medium",
                    format="%.2f",
                    min_value=0.0,
                    max_value=5.0,
                ),
            },
            disabled=fields,
            hide_index=True,
            width=800,
            key="rating"
        )
