import streamlit as st
import pandas as pd
import sqlite3
import streamlit.components.v1 as components
from visualizations import zip_price_map, rent_histogram, bed_vs_price

app_title = 'Tampa Apartment Rent Analysis'

app_sub_title = 'Source: Apartments.com 2025'


def display_folium_map():
    m = zip_price_map()
    m.save("zip_price_map.html")
    with open("zip_price_map.html", "r", encoding="utf-8") as f:
        folium_html = f.read()
    components.html(folium_html, height=600)


def main():
    st.set_page_config(app_title)
    st.title(app_title)
    st.caption(app_sub_title)

    # Load apartment dataframe
    conn = sqlite3.connect('apartment_data.db')
    query = "SELECT * FROM apartments"
    df = pd.read_sql_query(query, conn)
    conn.close()

    # Display apartment dataframe
    st.subheader("Apartment Data")
    st.dataframe(df)
    st.dataframe(df.set_index(df.columns[0]))

    # Display folium map of average Tampa rent
    st.subheader("Average Rent Price by Zip Code (Map)")
    display_folium_map()

    # Display histogram of Tampa rent
    st.subheader("Histogram of Rent Prices")
    hist = rent_histogram()
    st.altair_chart(hist, use_container_width=True)

    # Display scatter plot of ang rent vs avg bed count
    st.subheader("Scatter Plot of Average Rent vs Average Bed Count")
    scatter = bed_vs_price()
    st.altair_chart(scatter, use_container_width=True)

    # Load amenity dataframe
    conn = sqlite3.connect('apartment_data.db')
    query = "SELECT * FROM amenities"
    amenity_df = pd.read_sql_query(query, conn)
    conn.close()

    # Display amenity dataframe with apartment names
    st.subheader("Apartment Data")
    merged_amenity_df = pd.merge(df[['id', 'Apartment']], amenity_df, on='id', how='left')
    st.dataframe(merged_amenity_df)
    st.dataframe(merged_amenity_df.set_index(merged_amenity_df.columns[0]))

if __name__ == "__main__":
    main()
