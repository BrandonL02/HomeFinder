import sqlite3
import pandas as pd
import folium

def zip_price_map():

    # Load data from the DB
    conn = sqlite3.connect('apartment_data.db')
    query = "SELECT ZipCode, MinPrice, MaxPrice FROM apartments"
    df = pd.read_sql_query(query, conn)
    conn.close()

    # Drop null values and calculate average price
    df = df.dropna(subset=['ZipCode', 'MinPrice', 'MaxPrice'])
    df['ZipCode'] = df['ZipCode'].astype(str).str.zfill(5)
    df['MeanPrice'] = (df['MaxPrice'] + df['MinPrice']) / 2

    # Group apartments by zip code
    avg_rent = df.groupby("ZipCode")['MeanPrice'].mean().reset_index()

    # Load geojson of FL zip codes
    geojson_path = 'fl_florida_zip_codes_geo.min.json'

    # Create a folium map centered around Florida
    m = folium.Map(location=[28.04, -82.5], zoom_start=11)

    # Add choropleth layer
    folium.Choropleth(
        geo_data=geojson_path,
        name='choropleth',
        data=avg_rent,
        columns=['ZipCode', 'MeanPrice'],
        key_on='feature.properties.ZCTA5CE10',
        fill_color='YlOrRd',
        color='FF5733',
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name='Average Rent Price ($)',
        nan_fill_color='grey',
    ).add_to(m)

    folium.LayerControl().add_to(m)

    return m

import folium
from folium.plugins import MarkerCluster

def display_interactive_apartment_map(df):

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

    # Create folium map
    map_center = [28.04, -82.5]  # Tampa
    m = folium.Map(location=map_center, zoom_start=11)
    marker_cluster = MarkerCluster().add_to(m)

    # Add apartment markers
    for _, row in filtered_df.iterrows():
        popup_text = f"<b>${int(row['MinPrice'])} - ${int(row['MaxPrice'])}</b><br>{row['ZipCode']}"
        if 'Latitude' in row and 'Longitude' in row:
            location = [row['Latitude'], row['Longitude']]
            folium.Marker(location=location, popup=popup_text).add_to(marker_cluster)

    # Display map

    return m

