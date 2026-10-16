import pandas as pd
#Zadanie 1 i 3

dane = {
    'imie': ['Anna', 'Piotr', 'Katarzyna', 'Michał', 'Magdalena', 'Tomasz', 'Ewa', 'Jan', 'Karolina', 'Paweł'],
    'wzrost': [165, 180, 172, 185, 160, 175, 168, 190, 158, 182],
    'waga': [55, 85, 68, 92, 59, 78, 62, 95, 84, 88]
}

df = pd.DataFrame(dane)

df['BMI'] = df['waga'] / ((df['wzrost'] / 100) ** 2)
print(df)

# Zadanie 3 

df['wiek'] = [22, 35, 28, 42, 19, 31, 45, 26, 38, 29]

srednia_wieku = df['wiek'].mean()
print("Średnia wieku wynosi:", srednia_wieku)

warunek = (df['wiek'] > srednia_wieku) & (df['BMI'] > 25)

wybrane = df[warunek]

wynik = wybrane[['imie', 'wiek', 'BMI']]

print("\nOsoby spełniające kryteria:")
print(wynik)


# Zadanie 2

import pandas as pd

df1 = pd.DataFrame({"a": [1, 2], "b": [3, 4]})

df1.to_json("dane.json")
df2 = pd.read_json("dane.json")

print(df1.equals(df2))