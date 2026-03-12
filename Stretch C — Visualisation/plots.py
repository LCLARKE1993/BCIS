import streamlit as st
import plotly.express as px
import geopandas as gpd
from Stetch_B_Duckdb import main
# 1. Load data
def load():
    # grab the data from the main function -  Full dataset 
    # GeoDataFrame for constituencies
    #Merge both datasets for plotting on a choropleth map
    gdf = gpd.read_file('Parliamentary_Constituencies_July_2024.geojson') 
    result_df = main()
    merged_gdf = gdf.merge(result_df, left_on='PCON24NM', right_on='constituency_name')
    return merged_gdf, result_df

def create_choropleth(merged_gdf, result_df):
    # 2. Create Choropleth Map based merge_gdf and result_df
    fig = px.choropleth(
        merged_gdf,
        geojson=merged_gdf.geometry,
        locations=merged_gdf.index,
        color='median_habitable_rooms',
        hover_name='constituency_name',
        color_continuous_scale="Viridis",
        title="Median Habitable Rooms by UK Constituency"
    )
    fig.update_geos(fitbounds="locations", visible=False)

    # With out this the entire World map is shown as a result this allows us to target the UK
    fig.update_layout(
        geo=dict(
            projection_scale=5, # Higher number zooms in more
            center={"lat": 52.4862, "lon": -1.8904} # Coordinates for Birmingham
        )
    )
    return fig

def Streamlit_Display():
    # run the load function to get the merged GeoDataFrame and result DataFrame
    # create the choropleth map
    #display the choropleth map on streamlit
    merged_gdf, result_df = load()
    fig =create_choropleth(merged_gdf, result_df)
    st.title("Housing Choropleth Map")
    st.plotly_chart(fig)
    st.title("Top 10 Constituencies by Median Habitable Rooms")
    top_10_sorted = result_df[["constituency_name", "median_habitable_rooms"]].sort_values(
        by="median_habitable_rooms", 
        ascending=False
    ).head(10)
    # get the top 10 constituencies sorted by median habitable rooms descending order (highest first)
    # display the top 10 constituencies in a table on streamlit
    st.dataframe(top_10_sorted) 
    return st
if __name__ == "__main__":
    Streamlit_Display()