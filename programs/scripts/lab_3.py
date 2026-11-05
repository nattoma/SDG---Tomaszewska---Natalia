#Wektor - podstawy - zajęcia 3
import geopandas as gpd

#Zadanie 1 Dla warstwy z rzekami policz ile jest obiektów których MultiLineString zawiera dokładnie między 2 a 10 części składowych geometrii
rivers = gpd.read_file("D:/studia/semestr_5/pl_rzeki.geojson")

licznik = 0
for geom in rivers.geometry:

  if geom.geom_type == "MultiLineString":
    n_parts = len(geom.geoms)
    if 2 <= n_parts <= 10:
      licznik += 1

print(
    "Liczba obiektów MultiLineString zawierających od 2 do 10 części:"
    f" {licznik}"
)

#Zadanie 2 Dla warstwy demograficznej wyświetl na mapie kraje, w których odsetek osób w wieku 65+ wynosi ponad 18%
import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd

world_demo = gpd.read_file("D:/studia/semestr_5/lsp1.geojson")


world_demo["ludn_65_clean"] = (
    world_demo["ludność_w_wieku_65_lat_i_więcej"]
    .str.replace(" %", "", regex=False)
    .str.replace(" ", "", regex=False)
    .str.replace("brakdanych", "", regex=False)
    .str.replace("brak", "", regex=False)
    .str.replace(",", ".", regex=False)
)

world_demo["ludn_65_clean"] = pd.to_numeric(
    world_demo["ludn_65_clean"], errors="coerce"
)

filtered_countries = world_demo[world_demo["ludn_65_clean"] > 18]

fig, ax = plt.subplots(figsize=(10, 6))
filtered_countries.plot(ax=ax, color="crimson", edgecolor="black")
ax.set_title(
    "Kraje, w których odsetek osób w wieku 65+ wynosi ponad 18%", fontsize=11
)
plt.axis("off")
plt.show()



#Zadanie 3 Dla warstwy z wulkanami stwórz podzbiór wulkanów znajdujących się w Stanach Zjednoczonych. Następnie wypisz wszystkie typy wulkanów występujące w tym podzbiorze oraz oblicz, jaki procent wszystkich wulkanów w USA stanowi każdy z typów
import geopandas as gpd


sciezka_do_wulkanow = (
    r"D:\studia\semestr_5\wulkany\wulkany\lw1.geojson"
)
volcanoes = gpd.read_file(sciezka_do_wulkanow)

usa_volcanoes = volcanoes[volcanoes["kraj"] == "Stany Zjednoczone"].copy()

typy = usa_volcanoes["typ"].unique()
print("Występujące typy wulkanów w USA:", typy)

procenty = usa_volcanoes["typ"].value_counts(normalize=True) * 100
print("\nProcentowy udział poszczególnych typów wulkanów w USA:")
print(procenty)