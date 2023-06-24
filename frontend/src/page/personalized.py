import os

import pandas as pd
import streamlit as st
from requests import Session

backend_url = "http://backend:8080" if os.environ.get("is_docker") else "http://localhost:8080"


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
