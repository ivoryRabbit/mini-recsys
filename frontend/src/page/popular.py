import os

import pandas as pd
import streamlit as st
from requests import Session

backend_url = "http://backend:8080" if os.environ.get("is_docker") else "http://localhost:8080"


def popular_movies(session: Session = Session()):
    @st.cache_data
    def get_all_genres():
        genre_url = f"{backend_url}/genre/all"
        return session.get(genre_url).json()

    st.title("Popular Movies")

    genre = st.selectbox("Choose a genre", ["All"] + get_all_genres())

    if genre == "All":
        url = f"{backend_url}/rec/movie/popular?size=10"
    else:
        url = f"{backend_url}/rec/movie/popular?genre={genre}&size=10"

    response = session.get(url)

    if response.status_code == 200:
        data = response.json()
    else:
        st.stop()
        return

    col1, col2 = st.columns([1, 1])

    with col1:
        fields = ["id", "title", "year", "view"]

        st.subheader("[Most Viewed Movies]")
        st.data_editor(
            pd.DataFrame(data["view"])[fields],
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
                    max_chars=4,
                    validate=r"^\d{4}$",
                ),
                "view": st.column_config.ProgressColumn(
                    "View Count",
                    help="Count of total view",
                    width="medium",
                    format="%f",
                    min_value=0,
                    max_value=data["view"][0]["view"],
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
            pd.DataFrame(data["rating"])[fields],
            column_config={
                "id": st.column_config.Column(
                    "Movie ID",
                    help="ID of movie",
                    width="small",
                    required=True,
                ),
                "title": "Title",
                "year": st.column_config.TextColumn(
                    "Release",
                    help="Movie release year",
                    max_chars=4,
                    validate=r"^\d{4}$",
                ),
                "rating": st.column_config.ProgressColumn(
                    "Avg Rating",
                    help="Average of rating",
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


def personalized_movies(session: Session = Session()):
    st.title("Personalized Movies")

    if "response" not in st.session_state:
        st.session_state.response = None

    def request_recommend(user_id_str: str) -> None:
        if st.session_state.random or not user_id.isnumeric():
            url = f"{backend_url}/rec/movie/personalized?size=10&is_random=true"
        else:
            url = f"{backend_url}/rec/movie/personalized?user_id={user_id}&size=10"

        st.session_state.response = session.get(url).json()

    st.checkbox("Enable random input only", value=True, key="random")
    with st.form(key="form"):
        user_id = st.text_input(
            label="👇 Enter user ID",
            value="",
            placeholder="User ID",
            disabled=st.session_state.random,
        )
        st.form_submit_button(label="Input", on_click=request_recommend, args=(user_id, ))

    if st.session_state.response is None:
        return st.markdown("No")

    response = st.session_state.response

    col1, col2 = st.columns([1, 1])

    with col1:
        fields = ["id", "title", "genres", "year"]

        st.subheader("[Seed Movies]")
        st.data_editor(
            pd.DataFrame(response["seed"])[fields],
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
                "genres": st.column_config.Column(
                    "Genres",
                    help="Genres of movie",
                    width="medium",
                ),
                "year": st.column_config.TextColumn(
                    "Release",
                    help="Movie release year",
                    max_chars=4,
                    validate=r"^\d{4}$",
                ),
            },
            disabled=fields,
            hide_index=True,
            width=800,
            key="seed"
        )

    with col2:
        fields = ["id", "title", "genres", "year"]

        st.subheader("[Recommended Movies]")
        st.data_editor(
            pd.DataFrame(response["rec"])[fields],
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
                "genres": st.column_config.Column(
                    "Genres",
                    help="Genres of movie",
                    width="medium",
                ),
                "year": st.column_config.TextColumn(
                    "Release",
                    help="Movie release year",
                    max_chars=4,
                    validate=r"^\d{4}$",
                ),
            },
            disabled=fields,
            hide_index=True,
            width=800,
            key="rec"
        )
