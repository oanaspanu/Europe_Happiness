import geopandas as gpd
import pandas as pd
import folium

# Path to the shapefile
shapefile_path = r"./ne_110m_admin_0_countries/ne_110m_admin_0_countries.shp"

# Load the shapefile
world = gpd.read_file(shapefile_path)
europe = world[world['CONTINENT'] == 'Europe']

# Load the cluster data
cluster_data = pd.read_csv('clusters.csv')
europe_clusters = europe.merge(cluster_data, left_on='NAME', right_on='Country', how='left')
europe_clusters['Cluster'] = europe_clusters['Cluster'].fillna('No Cluster')
color_map = {'C0': 'orange', 'C11': 'green', 'C12': 'red', 'No Cluster': 'gray'}

# Create a Folium map centered on Europe
m = folium.Map(location=[54.5260, 15.2551], zoom_start=4)  # Coordinates roughly center Europe

# Function to apply colors based on the cluster
def style_function(feature):
    cluster = feature['properties']['Cluster']
    return {
        'fillColor': color_map.get(cluster, 'gray'),
        'color': 'black',
        'weight': 1,
        'fillOpacity': 0.6,
    }

# Add GeoJSON to the Folium map
folium.GeoJson(
    europe_clusters,
    style_function=style_function,
    tooltip=folium.GeoJsonTooltip(fields=['NAME', 'Cluster'], aliases=['Country', 'Cluster'])
).add_to(m)

m.save('europe_clusters_map.html')