import streamlit as st
import pandas as pd
import sqlite3
import streamlit.components.v1 as components
from visualizations import zip_price_map, display_interactive_apartment_map


app_title = 'Tampa Apartment Rent Analysis'

app_sub_title = 'Source: Apartments.com 2025'

def display_folium_map():
    m = zip_price_map()
    m.save("zip_price_map.html")
    with open("zip_price_map.html", "r", encoding="utf-8") as f:
        folium_html = f.read()
    components.html(folium_html, height=600)

def display_interactive_map(df):
    # Sidebar filters
    zip_options = df['ZipCode'].dropna().astype(str).str.zfill(5).unique()
    selected_zips = st.sidebar.multiselect("Filter by Zip Code", sorted(zip_options), default=sorted(zip_options))

    min_price = int(df['MinPrice'].min())
    max_price = int(df['MaxPrice'].max())
    selected_range = st.sidebar.slider("Price Range", min_value=min_price, max_value=max_price, value=(min_price, max_price))

    # Filter dataframe
    filtered_df = df.copy()
    filtered_df['ZipCode'] = filtered_df['ZipCode'].astype(str).str.zfill(5)
    filtered_df = filtered_df[
        (filtered_df['ZipCode'].isin(selected_zips)) &
        (filtered_df['MinPrice'] >= selected_range[0]) &
        (filtered_df['MaxPrice'] <= selected_range[1])
    ]

    # Generate map from filtered data
    from visualizations import display_interactive_apartment_map
    m = display_interactive_apartment_map(filtered_df)
    m.save("interactive_apartments_map.html")
    with open("interactive_apartments_map.html", "r", encoding="utf-8") as f:
        folium_interactive_html = f.read()
    components.html(folium_interactive_html, height=600)


def main():
    st.set_page_config(app_title)
    st.title(app_title)
    st.caption(app_sub_title)

    # Load data from the DB
    conn = sqlite3.connect('apartment_data.db')
    query = "SELECT * FROM apartments"
    df = pd.read_sql_query(query, conn)
    conn.close()

    st.subheader("Apartment Data")
    st.dataframe(df)

    st.subheader("Average Rent Price by Zip Code (Map)")
    display_folium_map()

    # Add interactive map
    st.subheader("Interactive Apartment Map")
    display_interactive_map(df)


if __name__ == "__main__":
    main()