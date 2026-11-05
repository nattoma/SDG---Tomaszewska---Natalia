#Numpy - zajecia 1
import numpy as np

# Zadanie 1 Stwórz losową 1-wymiarową numpy array o długości 15 elementów. Następnie oblicz jej minimum, maksimum oraz odchylenie standardowe
t1 = np.random.randint(1, 100, 15)

print("tablica1:", t1)
print("najmniejsza:", np.min(t1))
print("najwieksza:", np.max(t1))
print("odchylenie standardowe:", np.std(t1))

# Zadanie 2 Stwórz losową tablicę 2-wymiarową numpy array 4 wiersze x 4 kolumny, a następnie oblicz sumę wartości dla każdej kolumny oraz dla każdego wiersza
t2 = np.random.randint(1, 10, (4, 4))

print("tablica2:\n", t2)
print("suma kolumn:", t2.sum(axis=0))
print("suma wierszy:", t2.sum(axis=1))


#Zadanie 3 Stwórz tablicę 2-wymiarową 5 wierszy x 5 wierszy, w której każda wartość będzie o 3 większa od poprzedniej. Podaj indeksy każdej wartości parzystej większej od 10
tabela = np.arange(0, 75, 3).reshape(5, 5)
warunek = (tabela % 2 == 0) & (tabela > 10)

print(np.argwhere(warunek))