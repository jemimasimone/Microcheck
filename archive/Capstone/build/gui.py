from pathlib import Path
from tkinter import Tk, Canvas, Button, PhotoImage
import tkinter.font as tkFont

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"assets/frame0")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

# Place the window at the middle of the screen
def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    window.geometry(f"{width}x{height}+{x}+{y}")

def update_canvas(*args):
    canvas.config(width = window.winfo_width(), height = window.winfo_height())
    
    footer_height = int(window.winfo_height() * 0.15)  
    footer_y = window.winfo_height() - footer_height
    canvas.coords(footer_rect, 0, footer_y, window.winfo_width(), window.winfo_height())

    button_width = int(window.winfo_width() * 0.13) 
    button_height = int(footer_height * 0.6)  
    zoom_button_size = int(window.winfo_width() * 0.04)  
    all_button_width = int(window.winfo_width() * 0.13)  
    all_button_height = int(button_height * 0.5)  
    spacing = (window.winfo_width() - button_width * 3) // 4

    font_size = int(window.winfo_width() * 0.015) 
    button_font = tkFont.Font(family="IstokWeb Bold", size=font_size)
    for button in [button_3, button_4, button_5, button_all]:
        button.config(font=button_font)

    button_positions = {
        button_1: (int(30), int(30)),
        button_2: (int(30), int(30 + zoom_button_size + 30)),
        button_3: (window.winfo_width() // 2 - button_width // 2, footer_y + (footer_height - button_height) // 2),
        button_4: (spacing, footer_y + (footer_height - button_height) // 2),
        button_5: (window.winfo_width() - button_width - spacing, footer_y + (footer_height - button_height) // 2),
        button_all: (window.winfo_width() // 2 - all_button_width // 2, int(30))
    }

    for button, (x, y) in button_positions.items():
        if button in [button_1, button_2]:
            button.place(x=x, y=y, width=zoom_button_size, height=zoom_button_size)
        else:
            button.place(x=x, y=y, width=all_button_width if button == button_all else button_width, height=all_button_height if button == button_all else button_height)


window = Tk()
window_width = 700
window_height  = 550

center_window(window, window_width, window_height)
window.configure(bg="#FFFFFF")
window.title("Microcheck")

# Set minimum size
window.minsize(window_width, window_height)

canvas = Canvas(
    window,
    bg="white",
    relief="flat"
)

canvas.grid(row=0, column=0, sticky="nsew")

# Footer section
footer_height = 100
footer_rect = canvas.create_rectangle(
    0, window_height - footer_height,
    window_width, window_height,
    fill="#008CB8",
    outline=""
)

button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
button_image_2 = PhotoImage(file=relative_to_assets("button_2.png"))
button_image_3 = PhotoImage(file=relative_to_assets("button_3.png"))
button_image_4 = PhotoImage(file=relative_to_assets("button_4.png"))
button_image_5 = PhotoImage(file=relative_to_assets("button_5.png"))
button_image_all = PhotoImage(file=relative_to_assets("button_all.png"))

# Buttons
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightbackground="#FFFFFF",
    command=lambda: print("Zoom In clicked"),
    relief="raised",
    cursor="hand2"
)

button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightbackground="#FFFFFF",
    command=lambda: print("Zoom Out clicked"),
    relief="raised",
    cursor="hand2"
)

button_all = Button(
    text="All",
    compound="center",
    borderwidth=0,
    highlightbackground="#FFFFFF",
    command=lambda: print("All clicked"),
    relief="raised",
    fg="#454545",
    font=("IstokWeb Bold", 15 * -1),
    cursor="hand2",
    padx = 10,
    pady = 10,
    activebackground="light gray",
    activeforeground="black"
)

# Footer buttons
button_3 = Button(
    text="Fragment",
    compound="center",
    command=lambda: print("Fragment is clicked"),
    relief="raised",
    fg="#454545",
    font=("IstokWeb Bold", 15 * -1),
    cursor="hand2",
    padx = 10,
    pady = 10,
    activebackground="light gray",
    activeforeground="black"
)

button_4 = Button(
    text="Pellet",
    compound="center",
    command=lambda: print("Pellet is clicked"),
    relief="raised",
    fg="#454545",
    font=("IstokWeb Bold", 15 * -1),
    cursor="hand2",
    padx = 10,
    pady = 10,
    activebackground="light gray",
    activeforeground="black"
)

button_5 = Button(
    text="Fiber",
    compound="center",
    command=lambda: print("Fiber is clicked"),
    relief="raised",
    fg="#454545",
    font=("IstokWeb Bold", 15 * -1),
    cursor="hand2",
    padx = 10,
    pady = 10,
    activebackground="light gray",
    activeforeground="black"
)

button_1.place(x=30, y=30, width=30, height=30)
button_2.place(x=30, y=90, width=30, height=30)
button_3.place(x=window_width // 2 - 45, y=window_height - footer_height + 15, width=120, height=60)
button_4.place(x=55, y=window_height - footer_height + 15, width=120, height=60)
button_5.place(x=window_width - 145, y=window_height - footer_height + 15, width=120, height=60)
button_all.place(x=window_width // 2 - 45, y=30, width=90, height=30)

# Update units
window.rowconfigure(0, weight=1)
window.columnconfigure(0, weight=1)

window.bind("<Configure>", update_canvas)
update_canvas()

window.mainloop()
