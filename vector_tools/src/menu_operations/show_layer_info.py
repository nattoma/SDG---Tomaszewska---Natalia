from tkinter import messagebox

from src.data_service import get_layer

def show_layer_info():
    layer = get_layer()

    if layer is None:
        return

    info = (
        f"Liczba obiektów: {len(layer)}\n"
        f"Liczba kolumn: {len(layer.columns)}\n"
        f"Typ geometrii: {', '.join(layer.geom_type.unique())}\n"
        f"Układ współrzędnych: {layer.crs}"
    )

    messagebox.showinfo(
        "Informacje o warstwie",
        info
    )
