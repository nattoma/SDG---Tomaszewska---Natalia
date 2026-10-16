import numpy as np
print("hello")


# Zadanie 1 
t1 = np.random.randint(1, 100, 15)

print("tablica1:", t1)
print("najmniejsza:", np.min(t1))
print("najwieksza:", np.max(t1))
print("odchylenie standardowe:", np.std(t1))

# Zadanie 2 
t2 = np.random.randint(1, 10, (4, 4))

print("tablica2:\n", t2)
print("suma kolumn:", t2.sum(axis=0))
print("suma wierszy:", t2.sum(axis=1))


#Zadanie 3

tabela = np.arange(0, 75, 3).reshape(5, 5)
warunek = (tabela % 2 == 0) & (tabela > 10)

print(np.argwhere(warunek))