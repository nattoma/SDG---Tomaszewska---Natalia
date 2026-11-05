import tkinter as tk

def create_window():
    # Utworzenie głównego okna + canvas:

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


    # Grafika tła:

    window.background_screen = tk.PhotoImage(
        file="src/img/ekran1.png"
    )

    canvas.create_image(
        0,
        0,
        image=window.background_screen,
        anchor="nw"
    )


    # Tytuł programu:
    canvas.create_text(
        200,
        50,
        text="VectorTools",
        font=("Arial", 30, "bold"),
        fill="white"
    )


    # Menu:

    canvas.create_text(
        180,
        420,
        text="Wybierz operację:",
        font=("Arial", 16, "bold"),
        fill="white"
    )

    return (window, canvas)