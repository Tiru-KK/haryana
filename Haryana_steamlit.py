import folium
import geopandas as gpd
import pandas as pd
import streamlit as st
from streamlit_folium import folium_static

# Set the page config at the beginning of the script
st.set_page_config(page_title="Haryana Election Prediction Map", layout="wide")

# Load Haryana GeoJSON or Shapefile
geo_data = gpd.read_file("/haryana.assembly.shp")

# Load your election data
election_data = pd.read_csv("/haryana.csv")

# Merge GeoJSON with election data
geo_data = geo_data.merge(election_data, left_on='ac_name', right_on='ac_name')

# Streamlit App Title
st.title("Haryana Election Prediction Map")

# Initialize session state for dropdown selections
if 'selected_ac_names' not in st.session_state:
    st.session_state['selected_ac_names'] = {
        'BJP': [],
        'INC': [],
        'Tough Fight': [],
        'Independent': []
    }

# All constituencies
all_ac_names = geo_data['ac_name'].tolist()

# Create a grid for constituencies and dropdowns (6 columns)
num_columns = 6
rows = [all_ac_names[i:i + num_columns] for i in range(0, len(all_ac_names), num_columns)]

# Create a container for a better layout
with st.container():
    # Display the dropdowns in a grid layout
    for row in rows:
        cols = st.columns(num_columns)
        for col, ac_name in zip(cols, row):
            selected_party = col.selectbox(
                label=f"{ac_name}",
                options=['Select Party', 'BJP', 'INC', 'Tough Fight', 'Independent'],
                index=0,
                key=ac_name
            )

            # Update selections in session state
            if selected_party != 'Select Party':
                if selected_party == 'BJP':
                    st.session_state['selected_ac_names']['BJP'].append(ac_name)
                elif selected_party == 'INC':
                    st.session_state['selected_ac_names']['INC'].append(ac_name)
                elif selected_party == 'Tough Fight':
                    st.session_state['selected_ac_names']['Tough Fight'].append(ac_name)
                elif selected_party == 'Independent':
                    st.session_state['selected_ac_names']['Independent'].append(ac_name)

# Submit button to apply all selections at once
if st.button("Update Map"):
    # Define a function to color constituencies based on selected constituencies
    def color_constituencies(row):
        if row['ac_name'] in st.session_state['selected_ac_names']['BJP']:
            return 'orange'
        elif row['ac_name'] in st.session_state['selected_ac_names']['INC']:
            return 'lightblue'
        elif row['ac_name'] in st.session_state['selected_ac_names']['Tough Fight']:
            return 'gray'
        elif row['ac_name'] in st.session_state['selected_ac_names']['Independent']:
            return 'red'
        else:
            return 'white'  # Unselected constituencies remain white

    # Create a Folium map centered on Haryana
    # Set a larger width and height for the map
    haryana_map = folium.Map(location=[29.0588, 76.0856], zoom_start=7, width='100%', height='100%')

    # Add GeoJSON to the map
    folium.GeoJson(
        geo_data,
        style_function=lambda feature: {
            'fillColor': color_constituencies(feature['properties']),
            'color': 'black',
            'weight': 1,
            'fillOpacity': 0.7,
        },
        tooltip=folium.GeoJsonTooltip(
            fields=['ac_name'],
            aliases=['Constituency'],
            localize=True
        )
    ).add_to(haryana_map)

    # Display the map with Streamlit
    # Increase map size within Streamlit container
    folium_static(haryana_map, width=1100, height=600)
