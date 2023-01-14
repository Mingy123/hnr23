from tkinter import *
from tkinter.ttk import *
from PIL import ImageTk, Image

BG_COLOUR = "#8D021F"

window = Tk()

top_frame = Frame(master=window)
top_frame.grid(row=0, column=0, columnspan=2, padx=400, pady=100)

title = Label(text="Hey! Stop slouching!", master=top_frame, font=("Arial", 40, "bold"), background=BG_COLOUR, foreground="#FFCCCB")
title.pack()

left_frame = Frame(master=window)
left_frame.grid(row=1, column=0)

warning = Label(text="You're leaning too far forward.\nLean back a bit!", master=left_frame, font=("Arial", 20), justify="center", background=BG_COLOUR, foreground="white")
warning.pack()

right_frame = Frame(master=window)
right_frame.grid(row=1, column=1)

bad = Label(image=ImageTk.PhotoImage(Image.open("lean.jpg")), master=right_frame, borderwidth=25)
bad.pack()

arrow = Label(image=ImageTk.PhotoImage(Image.open("arrow-right-fill.png")), master=right_frame)
arrow.pack()

good = Label(image=ImageTk.PhotoImage(Image.open("hunch.jpg")), master=right_frame)
good.pack()


bottom_frame = Frame(master=window)
bottom_frame.grid(row=2, column=0, columnspan=2, pady=100)

close_prompt = Label(text="This will close automatically when you sit straight.", master=bottom_frame, font=("Arial", 14, "italic"), justify="center")
close_prompt.pack()

window.wm_attributes("-topmost", 1)
window.overrideredirect(True)
window.eval('tk::PlaceWindow . center')
window.configure(background=BG_COLOUR)
window.mainloop()
