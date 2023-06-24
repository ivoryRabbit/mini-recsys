import os

import pandas as pd
import streamlit as st
from requests import Session

backend_url = "http://backend:8080" if os.environ.get("is_docker") else "http://localhost:8080"


def related_movies(session: Session = Session()):
    st.title("Related Movies")

    with st.form(key="form"):
        movie_id = st.text_input(
            label="Enter movie ID 👇. Random if no value is entered",
            placeholder="Movie ID",
            value=""
        )
        st.form_submit_button(label="Input")

    if movie_id == "":
        url = f"{backend_url}/rec/movie/related?size=10&is_random=true"
    else:
        url = f"{backend_url}/rec/movie/related?item_id={movie_id}&size=10"

    response = session.get(url).json()

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
