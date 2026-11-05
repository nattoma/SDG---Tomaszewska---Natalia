#Wektor - tworzenmie obrazów - zajęcia 5

#Zadanie 1 Stwórz warstwę liniową, która po wyświetleniu będzie zawierała pierwsze 3 drukowane litery Twojego imienia i pierwsze 3 drukowane litery Twojego nazwiska. Każda literka powinna być osobnym rekordem w GeoDataFrame. Wyeksportuj te dane i wyświetl w QGIS.
from shapely import LineString
import geopandas as gpd


letters_geometry = [
    # N
    LineString([(0, 0), (0, 4), (2, 0), (2, 4)]),
    # A 
    LineString([(3, 0), (4, 4), (5, 0)]), 
    LineString([(3.5, 2), (4.5, 2)]),
    # T
    LineString([(6, 4), (8, 4), (7, 4), (7, 0)]),
    # T
    LineString([(9, 4), (11, 4), (10, 4), (10, 0)]),
    # O
    LineString([(12, 0), (12, 4), (14, 4), (14, 0), (12, 0)]),
    # M
    LineString([(15, 0), (15, 4), (16, 2), (17, 4), (17, 0)]),
]


gdf_letters = gpd.GeoDataFrame(
    {
        "id": range(1, len(letters_geometry) + 1),
        "inicjal": ["N", "A", "A_kreska", "T", "T", "O", "M"],
    },
    geometry=letters_geometry,
    crs="EPSG:4326",
)

output_path = r"D:\studia\semestr_5\inicjaly_nat_tom.geojson"
gdf_letters.to_file(output_path, driver="GeoJSON")
print(f"Zapisano poprawiony plik z inicjałami do: {output_path}")



#Zadanie 2 Z danych o wyspach stwórz słownik, gdzie kluczem będą nazwy krajów a wartością lista geometrii wysp do nich przypisanych. Następnie stwórz ranking top 10 krajów które mają największą sumaryczną powierzchnię wysp w m2
import re
import geopandas as gpd
import pandas as pd


path = r"D:\studia\semestr_5\fw2.geojson"
islands = gpd.read_file(path)

def parse_area(area_str):
  if not area_str or pd.isna(area_str):
    return 0.0
  cleaned = str(area_str).lower().replace(" ", "").replace(",", ".")
  match = re.search(r"([\d.]+)([km²m²]*)", cleaned)
  if not match:
    return 0.0
  val = float(match.group(1))
  unit = match.group(2)
  if "km" in unit:
    val *= 1_000_000  
  return val


islands["powierzchnia_m2"] = islands["powierzchnia"].apply(parse_area)

country_dict = {}
for idx, row in islands.iterrows():
  countries = [c.strip() for c in str(row["państwo"]).split(",")]
  for country in countries:
    if country not in country_dict:
      country_dict[country] = []
    country_dict[country].append(row["geometry"])

country_area = islands.assign(
    panstwo_split=islands["państwo"].str.split(",")
).explode("panstwo_split")
country_area["panstwo_split"] = country_area["panstwo_split"].str.strip()

top_10_countries = (
    country_area.groupby("panstwo_split")["powierzchnia_m2"]
    .sum()
    .reset_index()
    .sort_values(by="powierzchnia_m2", ascending=False)
    .head(10)
)

print("Top 10 krajów o największej sumarycznej powierzchni wysp:")
print(top_10_countries.to_string(index=False))




#Zadanie 3 Z danych o wyspach stwórz nowy GeoDataFrame zawierający tylko wyspy należące do Japonii. Przeprowadź dla nich 3 wizualizacje różniące się poziomem uproszczenia geometrii. Dla każdego poziomu wypisz: ilość krawędzi (linii) oraz ilość wierzchołków (punktów) z których się składa
import geopandas as gpd

path = r"D:\studia\semestr_5\fw2.geojson"
islands = gpd.read_file(path)


japan_islands = islands[islands["państwo"].str.contains("Japonia", na=False)].copy()

japan_metric = japan_islands.to_crs(3395)



def count_topology(geom):
  verts = 0
  edges = 0
  if geom.is_empty:
    return 0, 0
  geom_list = (
      geom.geoms
      if geom.geom_type in ["MultiPolygon", "GeometryCollection"]
      else [geom]
  )
  for poly in geom_list:
    if poly.geom_type == "Polygon":
      ext_coords = list(poly.exterior.coords)
      verts += len(ext_coords)
      edges += len(ext_coords) - 1
      for interior in poly.interiors:
        int_coords = list(interior.coords)
        verts += len(int_coords)
        edges += len(int_coords) - 1
  return verts, edges



tolerances = [2000, 10000, 25000]

for tol in tolerances:
  simplified_geom = japan_metric.geometry.simplify(tol)

  total_vertices = 0
  total_edges = 0

  for geom in simplified_geom:
    v, e = count_topology(geom)
    total_vertices += v
    total_edges += e

  print(f"--- Poziom uproszczenia (Tolerancja: {tol} m) ---")
  print(f"Ilość wierzchołków (punktów): {total_vertices}")
  print(f"Ilość krawędzi (linii): {total_edges}\n")

ax = japan_metric.geometry.simplify(10000).plot(color="teal", edgecolor="black")
ax.set_title("Wyspy Japonii po uproszczeniu geometrii (10 km)")