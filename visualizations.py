import time
import sqlite3
import pandas as pd
import folium
from folium.plugins import MarkerCluster
import streamlit as st
from geopy.geocoders import Nominatim


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


geolocator = Nominatim(user_agent="tampa_apartment_mapper")

def geocode_address(address):
    try:
        location = geolocator.geocode(address)
        if location:
            return location.latitude, location.longitude
    except Exception as e:
        print(f"Error geocoding {address}: {e}")
    return None, None

def display_interactive_apartment_map(df):
    # Ensure lat/lon columns exist
    if 'Latitude' not in df.columns or 'Longitude' not in df.columns:
        df['Latitude'] = None
        df['Longitude'] = None

    for idx, row in df.iterrows():
        if pd.isna(row['Latitude']) or pd.isna(row['Longitude']):
            lat, lon = geocode_address(row['Address'])
            df.at[idx, 'Latitude'] = lat
            df.at[idx, 'Longitude'] = lon
            time.sleep(1)  # prevent rate limit issues

    # Drop missing geocodes
    df = df.dropna(subset=['Latitude', 'Longitude'])

    # Create the map
    m = folium.Map(location=[28.04, -82.5], zoom_start=11)
    marker_cluster = MarkerCluster().add_to(m)

    for _, row in df.iterrows():
        popup_text = f"<b>${int(row['MinPrice'])} - ${int(row['MaxPrice'])}</b><br>{row['Address']}"
        location = [row['Latitude'], row['Longitude']]
        folium.Marker(location=location, popup=popup_text).add_to(marker_cluster)

    return m


