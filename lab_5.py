import geopandas as gpd
from shapely.geometry import LineString

# Litera N
n = LineString([(0, 0), (0, 4), (2, 0), (2, 4)])
# Litera A
a = LineString([(3, 0), (4, 4), (5, 0), (3.5, 2), (4.5, 2)])
# Litera T
t1 = LineString([(6, 4), (8, 4)])
t2 = LineString([(7, 0), (7, 4)])
# Litera T 
t3 = LineString([(9, 4), (11, 4)])
t4 = LineString([(10, 0), (10, 4)])
# Litera O
o = LineString([(12, 0), (12, 4), (14, 4), (14, 0), (12, 0)])
# Litera M
m = LineString([(15, 0), (15, 4), (16, 2), (17, 4), (17, 0)])

letters_gdf = gpd.GeoDataFrame(
    {
        "litera": ["N", "A", "T", "T", "O", "M"]
    },
    geometry=[n, a, LineString(t1.coords[:] + t2.coords[:]), LineString(t3.coords[:] + t4.coords[:]), o, m],
    crs="EPSG:2180"
)

letters_gdf.to_file("moje_inicjaly.geojson", driver="GeoJSON")
letters_gdf.plot()




import geopandas as gpd

# Wczytanie danych o wyspach
islands = gpd.read_file("../dane/fw2.geojson")

# 1. Stworzenie słownika: klucz = kraj, wartość = lista geometrii
island_dict = {}
for country, group in islands.groupby("kraj"):  # Zmień "kraj" na kolumnę z nazwą państwa jeśli trzeba
    island_dict[country] = list(group.geometry)

# 2. Ranking top 10 krajów o największej sumarycznej powierzchni wysp
# Najlepiej wykonać to rzutując na układ metryczny (np. EPSG:2180), aby powierzchnia była w m²
if islands.crs != "EPSG:2180":
    islands_m = islands.to_crs("EPSG:2180")
else:
    islands_m = islands

# Grupowanie po kraju i sumowanie powierzchni
top_countries = (
    islands_m.groupby("kraj")["geometry"]
    .apply(lambda geom: geom.area.sum())
    .reset_index(name="suma_powierzchni_m2")
    .sort_values(by="suma_powierzchni_m2", ascending=False)
    .head(10)
)

print("Top 10 krajów o największej sumarycznej powierzchni wysp:")
print(top_countries)