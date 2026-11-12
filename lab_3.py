import geopandas as gpd

path_to_files = "D:/studia/semestr_5/wulkany" 

# SHP:

shp_v = gpd.read_file(path_to_files+"lw1/lw1.shp")
print(shp_v.head())

# GEOJSON:

geojson_v = gpd.read_file(path_to_files+"lw1.geojson")
print(geojson_v.head())

# GPKG:

gpkg_v = gpd.read_file(path_to_files+"lw1.gpkg")
print(gpkg_v.head())

# CSV:

import pandas as pd
csv_v_raw = pd.read_csv(path_to_files+"lw1.csv")
csv_v = gpd.GeoDataFrame(
    csv_v_raw,
    geometry=gpd.points_from_xy(
        csv_v_raw["x"],
        csv_v_raw["y"]
    ),
    crs="EPSG:4326"
) # Skąd wynika większe skomplikowanie przy csv?

print(csv_v_raw)