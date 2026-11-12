import geopandas as gpd
from tkinter import filedialog, messagebox

from src.data_service import set_layer


def load_data_and_remember_outcome():
    layer = load_data()
    set_layer(layer)
    

def load_data():
    path = filedialog.askopenfilename(
        title="Wybierz warstwę"
    )

    if not path:
        return None

    try:
        layer = gpd.read_file(path)
    except Exception:
        messagebox.showwarning(
            "Błąd wczytywania",
            "Nie udało się wczytać wybranego pliku.\n"
            "Upewnij się, że jest to prawidłowy plik GIS."
        )
        return None

    return layer
