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

        # Step 5: Select a categorical column
        columns = list(gdf.columns)
        selected_column = st.selectbox('Choose a categorical column', columns)

        if selected_column:
            unique_values = gdf[selected_column].unique()

            # Step 6: Assign values to each unique category
            st.subheader(f'Assign values for {selected_column}')
            assigned_values = {}
            num_columns = 4  # Adjust this value based on your preference
            cols = st.columns(num_columns)
            for i, value in enumerate(unique_values):
                col = cols[i % num_columns]
                assigned_values[value] = col.number_input(f'Value for {value}', value=0)

            # Add the assigned values as a new column to the GeoDataFrame
            gdf['assigned_value'] = gdf[selected_column].map(assigned_values)

            # Step 7: Plot the map based on the assigned values
            st.subheader(f'Plot of the Shapefile colored by assigned values for {selected_column}')
            fig, ax = plt.subplots()
            gdf.plot(column='assigned_value', legend=True, ax=ax)
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
3. Choose a categorical column and assign numerical values to each unique category.
4. Plot the GeoDataFrame based on the assigned values.
""")
