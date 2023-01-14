from tkinter import *
from tkinter.ttk import *
import tkinter as tk
from PIL import ImageTk, Image
import sys

BG_COLOUR = "#8D021F"

window = Tk()

top_frame = Frame(master=window)
top_frame.grid(row=0, column=0, columnspan=5, padx=100, pady=100)

def disableLook():
    with open("STOPCHECKLOOK", "w") as f: f.close()

if sys.argv[1] == "slouch":

    title = Label(text="Hey! Stop slouching!", master=top_frame, font=("Arial", 40, "bold"), background=BG_COLOUR, foreground="#FFCCCB")
    title.pack()

    left_frame = Frame(master=window)
    left_frame.grid(row=1, column=0, padx=100)

    warning = Label(text="You're leaning\ntoo far forward.\n\nLean back a bit!", master=left_frame, font=("Roboto", 20), justify="center", background=BG_COLOUR, foreground="white")
    warning.pack()

    bad_frame = Frame(master=window)
    bad_frame.grid(row=1, column=1, padx=0, sticky="e")
    bad_img = ImageTk.PhotoImage(Image.open("posture/lean.jpg"))
    bad = Label(image=bad_img, master=bad_frame, borderwidth=25)
    bad.pack()

    arrow_frame = Frame(master=window)
    arrow_frame.grid(row=1, column=2)
    arrow_canvas = Canvas(arrow_frame, width=250, height=350, border=24, bg="#8D021F", highlightthickness=0)
    arrow_canvas.pack()

    arrow_img = ImageTk.PhotoImage(Image.open("posture/arrow-right-circle-fill.png"))
    arrow_canvas.create_image(155, 200, image=arrow_img)

    good_frame = Frame(master=window)
    good_frame.grid(row=1, column=3)
    good_img = ImageTk.PhotoImage(Image.open("posture/hunch.jpg"))
    good = Label(image=good_img, master=good_frame, borderwidth=25)
    good.pack()


    bottom_frame = Frame(master=window)
    bottom_frame.grid(row=2, column=0, columnspan=5, pady=100)

    padding_frame = Frame(master=window)
    padding_frame.grid(row=1, column=4, padx=50)

    close_prompt = Label(text="This will close automatically when you sit straight.", master=bottom_frame, font=("Arial", 14, "italic"), justify="center", background=BG_COLOUR, foreground="white")
    close_prompt.pack()

elif sys.argv[1] == "side":
    title = Label(text="Hey! Look here!", master=top_frame, font=("Arial", 40, "bold"), background=BG_COLOUR, foreground="#FFCCCB")
    title.pack()

    left_frame = Frame(master=window)
    left_frame.grid(row=1, column=0, padx=100)

    warning = Label(text="You're looking away\nfrom your screen.\n\nThis strains your neck!\n", master=left_frame, font=("Roboto", 20), justify="center", background=BG_COLOUR, foreground="white")
    warning.pack()

    ignore = tk.Button(text="Ignore this check", master=left_frame, command=disableLook, highlightthickness=0, bd=0)
    ignore.pack()

    bad_frame = Frame(master=window)
    bad_frame.grid(row=1, column=1, padx=0, sticky="e")
    bad_img = ImageTk.PhotoImage(Image.open("posture/turn.jpg"))
    bad = Label(image=bad_img, master=bad_frame, borderwidth=25)
    bad.pack()

    arrow_frame = Frame(master=window)
    arrow_frame.grid(row=1, column=2)
    arrow_canvas = Canvas(arrow_frame, width=250, height=350, border=24, bg="#8D021F", highlightthickness=0)
    arrow_canvas.pack()

    arrow_img = ImageTk.PhotoImage(Image.open("posture/arrow-right-circle-fill.png"))
    arrow_canvas.create_image(155, 200, image=arrow_img)

    good_frame = Frame(master=window)
    good_frame.grid(row=1, column=3)
    good_img = ImageTk.PhotoImage(Image.open("posture/hunch.jpg"))
    good = Label(image=good_img, master=good_frame, borderwidth=25)
    good.pack()


    bottom_frame = Frame(master=window)
    bottom_frame.grid(row=2, column=0, columnspan=5, pady=100)

    padding_frame = Frame(master=window)
    padding_frame.grid(row=1, column=4, padx=50)

    close_prompt = Label(text="This will close automatically when you sit straight.", master=bottom_frame, font=("Arial", 14, "italic"), justify="center", background=BG_COLOUR, foreground="white")
    close_prompt.pack()

window.wm_attributes("-topmost", 1)
window.overrideredirect(True)
window.eval('tk::PlaceWindow . center')
window.configure(background=BG_COLOUR)
window.mainloop()
