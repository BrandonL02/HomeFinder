import streamlit as st
import pandas as pd
import sqlite3

app_title = 'Tampa Apartment Rent Analysis'

app_sub_title = 'Source: Apartments.com 2025'


def main():
    st.set_page_config(app_title)
    st.title(app_title)
    st.caption(app_sub_title)

    # Load data from the DB
    conn = sqlite3.connect('apartment_data.db')
    query = "SELECT * FROM apartments"
    df = pd.read_sql_query(query, conn)
    conn.close()

    st.write(df.shape)
    st.write(df.head())
    st.write(df.columns)


if __name__ == "__main__":
    main()