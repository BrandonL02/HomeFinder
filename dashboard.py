import streamlit as st

app_title = 'Tampa Apartment Rent Analysis'

app_sub_title = 'Source: Apartments.com 2025'


def main():
    st.set_page_config(app_title)
    st.title(app_title)
    st.caption(app_sub_title)


if __name__ == "__main__":
    main()