import streamlit as st
import geopandas as gpd
import plotly.express as px
import json
import tempfile
import os

st.title('Map Plotter')

# Step 1: Upload a zip file containing shapefile parts or a JSON file
uploaded_file = st.file_uploader("Choose a zip file containing shapefile or a JSON file", type=["zip", "json"])

if uploaded_file is not None:
    file_type = uploaded_file.name.split('.')[-1]

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_file_path = os.path.join(temp_dir, uploaded_file.name)

        with open(temp_file_path, "wb") as temp_file:
            temp_file.write(uploaded_file.getvalue())

        if file_type == "zip":
            # Handle shapefile
            with zipfile.ZipFile(temp_file_path, 'r') as zip_ref:
                zip_ref.extractall(temp_dir)

            # Find the .shp file within the extracted contents
            shapefile_path = None
            for root, dirs, files in os.walk(temp_dir):
                for file in files:
                    if file.endswith(".shp"):
                        shapefile_path = os.path.join(root, file)
                        break

            if shapefile_path:
                # Load the shapefile into a GeoDataFrame
                gdf = gpd.read_file(shapefile_path)
            else:
                st.error("No .shp file found in the uploaded zip file")
                st.stop()
        elif file_type == "json":
            # Handle JSON file
            with open(temp_file_path, "r") as json_file:
                json_data = json.load(json_file)

            # Check if the JSON data represents geographic data
            if "features" in json_data and "geometry" in json_data["features"][0]:
                # If the JSON data is already in GeoJSON format, create GeoDataFrame directly
                gdf = gpd.GeoDataFrame.from_features(json_data["features"])
            else:
                # If the JSON data is not in GeoJSON format, convert it
                # (This conversion depends on the structure of your JSON data)
                st.error("The uploaded JSON file does not contain geographic data in GeoJSON format.")
                st.stop()

        # Display basic information about the GeoDataFrame
        st.subheader('GeoDataFrame Information')
        st.write(gdf.head())

        # Select a categorical column
        columns = list(gdf.columns)
        selected_column = st.selectbox('Choose a categorical column', columns)

        if selected_column:
            # Rest of the code for assigning values, plotting, and instructions as before
else:
    st.write("Please upload a zip file containing shapefile or a JSON file to visualize")

# Instructions and additional info
st.subheader('Instructions')
st.write("""
1. Upload a zip file containing all shapefile parts (.shp, .shx, .dbf, .prj) or a JSON file.
2. View the initial plot of the shapefile or JSON data.
3. Choose a categorical column and assign numerical values to each unique category.
4. Plot the GeoDataFrame based on the assigned values.
""")
