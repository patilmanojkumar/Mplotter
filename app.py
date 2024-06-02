import streamlit as st
import geopandas as gpd
import matplotlib.pyplot as plt
import zipfile
import os

st.title('Geospatial Data Visualization with GeoPandas')

# Step 1: Upload a zip file containing shapefile parts
uploaded_file = st.file_uploader("Choose a zip file containing shapefile", type="zip")

if uploaded_file is not None:
    # Step 2: Extract the zip file
    with zipfile.ZipFile(uploaded_file, 'r') as zip_ref:
        zip_ref.extractall("extracted_shapefile")

    # Find the .shp file within the extracted contents
    shapefile_path = None
    for root, dirs, files in os.walk("extracted_shapefile"):
        for file in files:
            if file.endswith(".shp"):
                shapefile_path = os.path.join(root, file)
                break

    if shapefile_path:
        # Step 3: Load the shapefile into a GeoDataFrame
        gdf = gpd.read_file(shapefile_path)
        
        # Step 4: Display basic information about the GeoDataFrame
        st.subheader('GeoDataFrame Information')
        st.write(gdf.head())

        # Step 5: Plot the map
        st.subheader('Plot of the Shapefile')
        fig, ax = plt.subplots()
        gdf.plot(ax=ax)
        st.pyplot(fig)

        # Step 6: Add interactive options
        st.subheader('Custom Plotting Options')
        column = st.selectbox('Choose column to color by', gdf.columns)
        cmap = st.selectbox('Choose colormap', plt.colormaps())

        fig, ax = plt.subplots()
        gdf.plot(column=column, cmap=cmap, legend=True, ax=ax)
        st.pyplot(fig)
    else:
        st.error("No .shp file found in the uploaded zip file")
else:
    st.write("Please upload a zip file containing shapefile to visualize")

# Instructions and additional info
st.subheader('Instructions')
st.write("""
1. Upload a zip file containing all shapefile parts (.shp, .shx, .dbf, .prj).
2. View the initial plot of the shapefile.
3. Use custom plotting options to visualize data on the map.
""")
