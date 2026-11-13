#Powiat średzki - D:\studia\semestr_5\zaliczenie - moj folder z danymi dla powiatu Średzkiego
# - utworzyć pusty DataFrame zawierający kolumny ...
# - wczytanie wszystkich plików i załadowanie każdy z nich do osobnego obiektu geodataframe tworzac liste, 
# - do kazdego obiektu oblicz wymagane statystyki i uzupelnij nim kolejne rekordy dataframe wynikowego 


import os
import geopandas as gpd
import pandas as pd

# stworzenie pustego dataframe z kolumnami
tabela = pd.DataFrame(
    columns=[
        "nazwa warstwy",
        "rodzaj geometrii",
        "ilość obiektów",
        "średnia powierzchnia obiektów",
        "średnia długość obiektów",
        "średnia złożoność linii",
        "średnie wypełnienie przestrzeni",
    ]
)

# sciezka do moich plikow
folder = r"D:\studia\semestr_5\zaliczenie"

lista_warstw = []
lista_nazw = []

#sprawdzenie kazdego pliku w moim folderze
for nazwa_pliku in os.listdir(folder):
    if nazwa_pliku.endswith(".shp"):
        pelna_sciezka = folder + "\\" + nazwa_pliku
        warstwa = gpd.read_file(pelna_sciezka)

        lista_warstw.append(warstwa)
        lista_nazw.append(nazwa_pliku)





# policzenie wymaganych statystyk
numer_wiersza = 0

for i in range(len(lista_warstw)):
    warstwa = lista_warstw[i]
    nazwa = lista_nazw[i]

    ile_obiektow = len(warstwa)
    typy = warstwa.geom_type.unique()
    rodzaj_geom = str(typy[0]) 


    sr_powierzchnia = None
    sr_dlugosc = None
    sr_zlozonosc = None
    sr_wypelnienie = None

    # policzenie dla poligonow
    if "Polygon" in rodzaj_geom:
        sr_powierzchnia = warstwa.area.mean()
        sr_dlugosc = warstwa.length.mean()

        suma_wypelnien = 0
        for obiekt in warstwa.geometry:
            pole_obiektu = obiekt.area
            pole_prostokata = (
                obiekt.envelope.area
            ) 
            procent = (pole_obiektu / pole_prostokata) * 100
            suma_wypelnien = suma_wypelnien + procent

        sr_wypelnienie = suma_wypelnien / ile_obiektow

    #dla linii
    if "LineString" in rodzaj_geom:
        sr_dlugosc = warstwa.length.mean()
        suma_zlozonosci = 0
        for obiekt in warstwa.geometry:
            
            ilosc_wierzcholkow = len(list(obiekt.coords))
            dlugosc_linii = obiekt.length
            zlozonosc = ilosc_wierzcholkow / dlugosc_linii
            suma_zlozonosci = suma_zlozonosci + zlozonosc

        sr_zlozonosc = suma_zlozonosci / ile_obiektow


    #wypisanie wynikow
    tabela.loc[numer_wiersza] = [
        nazwa,
        rodzaj_geom,
        ile_obiektow,
        sr_powierzchnia,
        sr_dlugosc,
        sr_zlozonosc,
        sr_wypelnienie,
    ]
    numer_wiersza = numer_wiersza + 1


# wyswietlenie wyniku
pd.set_option("display.max_columns", None)
pd.set_option("display.width", 1000)
print(tabela)

# zapisanie jako csv
sciezka_zapisu = r"D:\studia\semestr_5\zaliczenie\wyniki_powiat_sredzki1.csv"
tabela.to_csv(sciezka_zapisu, index=False, sep=";", encoding="utf-8-sig")

print("dziala", sciezka_zapisu)