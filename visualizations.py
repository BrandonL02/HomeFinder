import time
import sqlite3
import pandas as pd
import folium
import altair as alt




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

def rent_histogram():

    # Load data from the DB
    conn = sqlite3.connect('apartment_data.db')
    query = "SELECT MinPrice, MaxPrice FROM apartments"
    df = pd.read_sql_query(query, conn)
    conn.close()

    df['AvgPrice'] = (df['MinPrice'] + df['MaxPrice']) / 2
    hist = alt.Chart(df).mark_bar().encode(
        alt.X("AvgPrice", bin=alt.Bin(maxbins=30), title='Average Rent Price'),
        y='count()'
    ).properties(title='Distribution of Rent Prices')

    return hist
