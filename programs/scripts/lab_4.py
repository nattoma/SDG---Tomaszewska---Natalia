#Wektor - struktura - zajęcia 4 
import geopandas as gpd
from shapely.geometry import box

# Zadanie 1 Dla warstwy z pasami ukształtowania policz ich powierzchnie w m2, korzystając z układu epsg:2180

sciezka_pasy = r"D:\studia\semestr_5\pl_pasy_ukształtowania.geojson"
pasy = gpd.read_file(sciezka_pasy)


pasy_2180 = pasy.to_crs(2180)


pasy_2180["powierzchnia_m2"] = pasy_2180.geometry.area

print("--- ZADANIE 1: Powierzchnia pasów (pierwsze 5) ---")
print(pasy_2180[["powierzchnia_m2"]].head())



#Zadanie 2 Stwórz obiekt Bounding Box dla warstwy z miastami wojewódzkimi, a następnie oblicz jego obwód

sciezka_miasta = r"D:\studia\semestr_5\pl_miasta_wojewódzkie.geojson"
miasta = gpd.read_file(sciezka_miasta)

miasta_2180 = mias_2180 = miasta.to_crs(2180)


bbox = miasta_2180.total_bounds  # [minx, miny, maxx, maxy]
bbox_poly = box(bbox[0], bbox[1], bbox[2], bbox[3])


obwod = bbox_poly.length
print(f"\n--- ZADANIE 2 ---")
print(f"Obwód Bounding Boxa wynosi: {obwod:.2f} metrów")



#Zadanie 3 Dla warstwy z rzekami stwórz nową kolumnę w której wyliczysz liczbę linii (LineString) znajdujących się wewnątrz. Analogicznie stwórz następnie drugą kolumnę w której wyliczysz łączną liczbę punktów składających się na geometrię

sciezka_rzeki = r"D:\studia\semestr_5\pl_rzeki.geojson"
rzeki = gpd.read_file(sciezka_rzeki)


def count_linestrings(geom):
  if geom is None:
    return 0
  if geom.geom_type == "LineString":
    return 1
  elif geom.geom_type == "MultiLineString":
    return len(geom.geoms)
  return 0


def count_total_points(geom):
  if geom is None:
    return 0
  total_pts = 0
  if geom.geom_type == "LineString":
    total_pts += len(geom.coords)
  elif geom.geom_type == "MultiLineString":
    for line in geom.geoms:
      total_pts += len(line.coords)
  return total_pts


# Tworzenie nowych kolumn w tabeli atrybutów
rzeki["liczba_linii"] = rzeki.geometry.apply(count_linestrings)
rzeki["liczba_punktow"] = rzeki.geometry.apply(count_total_points)

print("\n--- ZADANIE 3: Rzeki (liczba linii i punktów) ---")
print(rzeki[["liczba_linii", "liczba_punktow"]].head())