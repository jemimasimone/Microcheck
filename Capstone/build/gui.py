from pathlib import Path
from tkinter import Tk, Canvas, Button, PhotoImage

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\DELL\Desktop\school\Capstone\build\assets\frame0")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


window = Tk()

window.geometry("700x550")
window.configure(bg="#FFFFFF")
window.title("MicroCheck")

canvas = Canvas(
    window,
    bg="#FFFFFF",
    height=550,
    width=700,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)

canvas.place(x=0, y=0)

button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_1 clicked"),
    relief="flat"
)
button_1.place(
    x=30.0,
    y=30.0,
    width=30.0,
    height=30.0
)

button_image_2 = PhotoImage(
    file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_2 clicked"),
    relief="flat"
)
button_2.place(
    x=30.0,
    y=90.0,
    width=30.0,
    height=30.0
)

canvas.create_rectangle(
    0.0,
    450.0,
    700.0,
    550.0,
    fill="#008CB8",
    outline="")

button_image_3 = PhotoImage(
    file=relative_to_assets("button_3.png"))
button_3 = Button(
    image=button_image_3,
    text="Fragment",
    compound="center",
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_3 clicked"),
    relief="flat",
    fg="#454545",
    font=("IstokWeb Bold", 15 * -1)
)
button_3.place(
    x=305.0,
    y=485.0,
    width=90.0,
    height=30.0
)

button_image_4 = PhotoImage(
    file=relative_to_assets("button_4.png"))
button_4 = Button(
    image=button_image_4,
    text="Pellet",
    compound="center",
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_4 clicked"),
    relief="flat",
    fg="#454545",
    font=("IstokWeb Bold", 15 * -1)
)
button_4.place(
    x=55.0,
    y=485.0,
    width=90.0,
    height=30.0
)

button_image_5 = PhotoImage(
    file=relative_to_assets("button_5.png"))
button_5 = Button(
    image=button_image_5,
    text="Fiber",
    compound="center",
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_5 clicked"),
    relief="flat",
    fg="#454545",
    font=("IstokWeb Bold", 15 * -1)
)
button_5.place(
    x=544.0,
    y=485.0,
    width=90.0,
    height=30.0
)

button_image_all = PhotoImage(
    file=relative_to_assets("button_all.png"))  # Replace with your actual image file path
button_all = Button(
    image=button_image_all,
    text="All",
    compound="center",
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_all clicked"),
    relief="flat",
    fg="#454545",
    font=("IstokWeb Bold", 15 * -1)
)
button_all.place(
    x=305.0,
    y=30.0,
    width=90.0,
    height=30.0
)


window.resizable(False, False)
window.mainloop()
