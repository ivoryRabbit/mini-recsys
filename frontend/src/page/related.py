import os

import pandas as pd
import streamlit as st
from requests import Session

backend_url = "http://backend:8080" if os.environ.get("is_docker") else "http://localhost:8080"


def related_movies(session: Session = Session()):
    st.title("Related Movies")

    if "is_random" not in st.session_state:
        st.session_state.is_random = False

    def set_use_random(is_random: bool) -> None:
        st.session_state.is_random = is_random

    with st.form(key="form"):
        placeholder = st.empty()

        item_id = placeholder.text_input(
            label="👇 Enter movie ID",
            value="",
            placeholder="Movie ID",
        )

        col1, col2, _ = st.columns([1, 1, 8])

        with col1:
            st.form_submit_button(
                label="Input",
                use_container_width=True,
                on_click=set_use_random,
                args=(False, ),
            )
        with col2:
            st.form_submit_button(
                label="Random",
                use_container_width=True,
                on_click=set_use_random,
                args=(True, ),
            )

    if st.session_state.is_random is True:
        url = f"{backend_url}/rec/movie/related?is_random=true&size=10"
    elif item_id.isnumeric():
        url = f"{backend_url}/rec/movie/related?item_id={item_id}&size=10"
    else:
        st.stop()
        return

    response = session.get(url)

    if response.status_code == 200:
        data = response.json()
    else:
        st.stop()
        return

    item_id = data["item_id"]
    st.text(f"item_id = {item_id}")

    col1, col2 = st.columns([1, 1])

    with col1:
        fields = ["id", "title", "genres", "year"]

        st.subheader("[Seed Movies]")
        st.data_editor(
            pd.DataFrame(data["seed"])[fields],
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
        if len(data["rec"]) == 0:
            st.stop()

        fields = ["id", "title", "genres", "year"]

        st.subheader("[Recommended Movies]")
        st.data_editor(
            pd.DataFrame(data["rec"])[fields],
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
