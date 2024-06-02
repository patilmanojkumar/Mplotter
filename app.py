import streamlit as st
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
from zipfile import ZipFile
import os

# Title of the app
st.title("Shapefile Map Plotter with User Input Data")

# File uploader to upload the zip file containing the shapefile
uploaded_zipfile = st.file_uploader("Choose a .zip file containing the shapefile", type=["zip"])

# Function to extract and load the shapefile and return a GeoDataFrame
def load_shapefile(zip_file):
    with ZipFile(zip_file, 'r') as zip_ref:
        zip_ref.extractall("extracted_shapefile")
    for file in os.listdir("extracted_shapefile"):
        if file.endswith(".shp"):
            shapefile_path = os.path.join("extracted_shapefile", file)
            gdf = gpd.read_file(shapefile_path)
            return gdf

# If a zip file is uploaded
if uploaded_zipfile:
    gdf = load_shapefile(uploaded_zipfile)
    
    # Display the head of the GeoDataFrame
    st.dataframe(gdf.head())
    
    # Select the column in the shapefile to match user input data
    merge_column_gdf = st.selectbox("Select the column in the shapefile to merge on", gdf.columns)
    
    # Input locations and values
    st.write("Enter the location and corresponding values")
    num_entries = st.number_input("Number of entries", min_value=1, value=1, step=1)
    
    location_values = []
    for i in range(num_entries):
        location = st.text_input(f"Location {i + 1}")
        value = st.number_input(f"Value for {location}", format="%f")
        location_values.append((location, value))
    
    # Create a DataFrame from the user input
    data = pd.DataFrame(location_values, columns=[merge_column_gdf, 'Value'])
    st.write(data)
    
    # Merge the shapefile with the user input data
    merged_gdf = gdf.merge(data, left_on=merge_column_gdf, right_on=merge_column_gdf, how='left')
    
    # Plotting the map with the user input data
    fig, ax = plt.subplots(1, 1, figsize=(10, 6))
    merged_gdf.plot(column='Value', ax=ax, legend=True)
    st.pyplot(fig)
    
    # Clean up extracted files
    for file in os.listdir("extracted_shapefile"):
        os.remove(os.path.join("extracted_shapefile", file))
    os.rmdir("extracted_shapefile")
else:
    st.info("Please upload a zip file containing the shapefile.")
