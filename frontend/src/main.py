import pandas as pd
import requests
import streamlit as st
from streamlit_option_menu import option_menu

st.set_page_config(page_title="Mini-RecSys", page_icon="🤖", layout="wide")
backend_url = "http://backend:8080"


def home():
    st.title("Welcome to Mini-RecSys 👋")

    st.markdown(
        """
        Mini-RecSys is a graph-based recommendation system with Python.

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


def popular_movies():
    st.title("Popular Movies")

    session = requests.Session()

    @st.cache_data
    def get_all_genres():
        genre_url = f"{backend_url}/genre/all"
        return session.get(genre_url).json()

    genre = st.selectbox("Choose a genre", ["ALL"] + get_all_genres())

    if genre == "ALL":
        url = f"{backend_url}/rec/movie/popular?size=10"
    else:
        url = f"{backend_url}/rec/movie/popular?genre={genre}&size=10"

    response = session.get(url).json()

    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("[Most Viewed Movies]")
        st.data_editor(pd.DataFrame(response), key="viewed")

    with col2:
        st.subheader("[High Rated Movies]")
        st.data_editor(pd.DataFrame(response), key="rated")


def personalized_movies():
    st.title("Personalized Movies")

    session = requests.Session()

    url = f"{backend_url}/rec/movie/personalized?user_id=1&size=10"
    response = session.get(url).json()

    st.subheader("[Personalized Movies]")
    st.dataframe(response)


def related_movies():
    st.title("Related Movies")

    session = requests.Session()

    url = f"{backend_url}/rec/movie/related?item_id=1&size=10"
    response = session.get(url).json()

    st.subheader("[Related Movies]")
    st.data_editor(response)


def unused_example_1():
    import streamlit as st
    import pandas as pd
    import pydeck as pdk

    from urllib.error import URLError

    st.title("Personalized Movies")

    st.markdown(f"# {list(page_names_to_funcs.keys())[2]}")
    st.write(
        """
                This demo shows how to use
        [`st.pydeck_chart`](https://docs.streamlit.io/library/api-reference/charts/st.pydeck_chart)
        to display geospatial data.
        """
    )

    @st.cache_data
    def from_data_file(filename):
        url = (
            "http://raw.githubusercontent.com/streamlit/"
            "example-data/master/hello/v1/%s" % filename
        )
        return pd.read_json(url)

    try:
        ALL_LAYERS = {
            "Bike Rentals": pdk.Layer(
                "HexagonLayer",
                data=from_data_file("bike_rental_stats.json"),
                get_position=["lon", "lat"],
                radius=200,
                elevation_scale=4,
                elevation_range=[0, 1000],
                extruded=True,
            ),
            "Bart Stop Exits": pdk.Layer(
                "ScatterplotLayer",
                data=from_data_file("bart_stop_stats.json"),
                get_position=["lon", "lat"],
                get_color=[200, 30, 0, 160],
                get_radius="[exits]",
                radius_scale=0.05,
            ),
            "Bart Stop Names": pdk.Layer(
                "TextLayer",
                data=from_data_file("bart_stop_stats.json"),
                get_position=["lon", "lat"],
                get_text="name",
                get_color=[0, 0, 0, 200],
                get_size=15,
                get_alignment_baseline="'bottom'",
            ),
            "Outbound Flow": pdk.Layer(
                "ArcLayer",
                data=from_data_file("bart_path_stats.json"),
                get_source_position=["lon", "lat"],
                get_target_position=["lon2", "lat2"],
                get_source_color=[200, 30, 0, 160],
                get_target_color=[200, 30, 0, 160],
                auto_highlight=True,
                width_scale=0.0001,
                get_width="outbound",
                width_min_pixels=3,
                width_max_pixels=30,
            ),
        }
        st.sidebar.markdown("### Map Layers")
        selected_layers = [
            layer
            for layer_name, layer in ALL_LAYERS.items()
            if st.sidebar.checkbox(layer_name, True)
        ]
        if selected_layers:
            st.pydeck_chart(
                pdk.Deck(
                    map_style="mapbox://styles/mapbox/light-v9",
                    initial_view_state={
                        "latitude": 37.76,
                        "longitude": -122.4,
                        "zoom": 11,
                        "pitch": 50,
                    },
                    layers=selected_layers,
                )
            )
        else:
            st.error("Please choose at least one layer above.")
    except URLError as e:
        st.error(
            """
            **This demo requires internet access.**

            Connection error: %s
        """
            % e.reason
        )


def unused_example_2():
    import streamlit as st
    import time
    import numpy as np

    st.markdown(f'# {list(page_names_to_funcs.keys())[1]}')
    st.write(
        """
        This demo illustrates a combination of plotting and animation with
        Streamlit. We're generating a bunch of random numbers in a loop for around
        5 seconds. Enjoy!
        """
    )

    progress_bar = st.sidebar.progress(0)
    status_text = st.sidebar.empty()
    last_rows = np.random.randn(1, 1)
    chart = st.line_chart(last_rows)

    for i in range(1, 101):
        new_rows = last_rows[-1, :] + np.random.randn(5, 1).cumsum(axis=0)
        status_text.text("%i%% Complete" % i)
        chart.add_rows(new_rows)
        progress_bar.progress(i)
        last_rows = new_rows
        time.sleep(0.05)

    progress_bar.empty()

    # Streamlit widgets automatically run the script from top to bottom. Since
    # this button is not connected to any other logic, it just causes a plain
    # rerun.
    st.button("Re-run")


page_names_to_funcs = {
    "Home": home,
    "Popular Movies": popular_movies,
    "Personalized Movies": personalized_movies,
    "Related Movies": related_movies,
}

with st.sidebar:
    choose = option_menu(
        menu_title="Select a Demo",
        options=list(page_names_to_funcs.keys()),
        # Remark https://icons.getbootstrap.com/ for icons
        icons=["house", "hand-thumbs-up", "person", "people"],
        menu_icon="app-indicator",
        default_index=0,
        styles={
            "container": {"padding": "5!important", "background-color": "#fafafa"},
            "icon": {"color": "orange", "font-size": "25px"},
            "nav-link": {"font-size": "16px", "text-align": "left"},
            "nav-link-selected": {"background-color": "#02ab21"},
        }
    )

page_names_to_funcs[choose]()
