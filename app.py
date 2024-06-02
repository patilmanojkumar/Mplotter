import streamlit as st
import geopandas as gpd
import matplotlib.pyplot as plt

st.title('Geospatial Data Visualization with GeoPandas')

# Step 1: Upload shapefile
uploaded_file = st.file_uploader("Choose a shapefile", type=["shp", "shx", "dbf", "prj"])

if uploaded_file is not None:
    # Step 2: Load shapefile into a GeoDataFrame
    gdf = gpd.read_file(uploaded_file)
    
    # Step 3: Display basic information about the GeoDataFrame
    st.subheader('GeoDataFrame Information')
    st.write(gdf.head())

    # Step 4: Plot the map
    st.subheader('Plot of the Shapefile')
    fig, ax = plt.subplots()
    gdf.plot(ax=ax)
    st.pyplot(fig)

    # Step 5: Add interactive options
    st.subheader('Custom Plotting Options')
    column = st.selectbox('Choose column to color by', gdf.columns)
    cmap = st.selectbox('Choose colormap', plt.colormaps())

    fig, ax = plt.subplots()
    gdf.plot(column=column, cmap=cmap, legend=True, ax=ax)
    st.pyplot(fig)
else:
    st.write("Please upload a shapefile to visualize")

# Instructions and additional info
st.subheader('Instructions')
st.write("""
1. Upload the shapefile parts (shp, shx, dbf, prj).
2. View the initial plot of the shapefile.
3. Use custom plotting options to visualize data on the map.
""")
