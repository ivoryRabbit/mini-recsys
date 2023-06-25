import pandas as pd
import streamlit as st
from requests import Session

from config.client import backend_url


def related_movies(session: Session = Session()):
    st.title("Related Movies")

    if "related_movies" not in st.session_state:
        st.session_state["related_movies"] = None

    def request_recommend(is_random: bool):
        if is_random is True:
            item_id = None
        else:
            item_id = str(st.session_state["item_id"])

        url = f"{backend_url}/rec/movie/related"
        params = {"item_id": item_id, "is_random": is_random, "size": 10}

        response = session.get(url, params=params)

        if response.status_code == 200:
            data = response.json()
            st.session_state["item_id"] = str(data["item_id"])
        else:
            data = None

        st.session_state["related_movies"] = data

    with st.form(key="form"):
        st.text_input("👇 Enter movie ID", placeholder="Movie ID", key="item_id")
        col1, col2, _ = st.columns([1, 1, 8])

        with col1:
            st.form_submit_button(
                "Input",
                use_container_width=True,
                on_click=request_recommend,
                args=(False,)
            )
        with col2:
            st.form_submit_button(
                "Random",
                use_container_width=True,
                on_click=request_recommend,
                args=(True, )
            )

    result = st.session_state["related_movies"]

    if result is None:
        st.stop()
        return

    col1, col2 = st.columns([1, 1])
    fields = ["id", "title", "genres", "year"]

    with col1:
        st.subheader("[Seed Movies]")
        st.data_editor(
            pd.DataFrame(result["seed"])[fields],
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
        st.subheader("[Recommended Movies]")

        if len(result["rec"]) == 0:
            st.stop()

        st.data_editor(
            pd.DataFrame(result["rec"])[fields],
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
