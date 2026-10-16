import tkinter as tk
from PIL import Image, ImageTk

# --- Definicje metod ---
def close_program():
    window.destroy()

# --- Utworzenie głównego okna + Canvas ---
window = tk.Tk()
window.title("VectorTools")
window.resizable(False, False)

canvas = tk.Canvas(
    window,
    width=650,
    height=550,
    highlightthickness=0
)
canvas.pack()

# --- Grafika tła (obsługa PNG przez Pillow) ---
obraz_pil = Image.open("ekran1.png")
background_screen = ImageTk.PhotoImage(obraz_pil)

canvas.create_image(
    0,
    0,
    image=background_screen,
    anchor=tk.NW
)

# Zapobieganie usunięciu grafiki przez Garbage Collector
canvas.image = background_screen

# --- Tytuł programu ---
canvas.create_text(
    200,
    50,
    text="VectorTools",
    font=("Arial", 30, "bold"),
    fill="#871F78"
)

# --- Menu ---
canvas.create_text(
    180,
    420,
    text="Wybierz operację:",
    font=("Arial", 16, "bold"),
    fill="#FF6EC7"
)

# --- Przycisk zamknięcia ---
canvas.create_text(
    180,
    465,
    text="Zamknij program",
    font=("Arial", 11, "bold"),
    fill="white",
    tags="zamknij"
)

# Obsługa kliknięcia i najechania myszką (hover)
canvas.tag_bind(
    "zamknij",
    "<Button-1>",
    lambda event: close_program()
)

canvas.tag_bind(
    "zamknij",
    "<Enter>",
    lambda event: canvas.itemconfig("zamknij", fill="#cc0066")
)



# --- Główna pętla programu ---
window.mainloop()