import streamlit as st
import pandas as pd
import sqlite3
import streamlit.components.v1 as components
from visualizations import zip_price_map

app_title = 'Tampa Apartment Rent Analysis'

app_sub_title = 'Source: Apartments.com 2025'


def display_folium_map():
    m = zip_price_map()
    m.save("zip_price_map.html")
    with open("zip_price_map.html", "r", encoding="utf-8") as f:
        folium_html = f.read()
    components.html(folium_html, height=600)


def main():
    st.cache_data.clear()
    st.set_page_config(app_title)
    st.title(app_title)
    st.caption(app_sub_title)
    st.set_page_config(app_title, layout="wide")

    st.markdown("""
            <style>
                section[data-testid="stSidebar"] {
                    display: none !important;
                }
                div[data-testid="collapsedControl"] {
                    display: none !important;
                }
            </style>
        """, unsafe_allow_html=True)

    # Load data from the DB
    conn = sqlite3.connect('apartment_data.db')
    query = "SELECT * FROM apartments"
    df = pd.read_sql_query(query, conn)
    conn.close()

    st.subheader("Apartment Data")
    st.dataframe(df)

    st.subheader("Average Rent Price by Zip Code (Map)")
    display_folium_map()

    st.subheader('Test')


if __name__ == "__main__":
    main()
