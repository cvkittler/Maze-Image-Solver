import tkinter as tk
from tkinter import filedialog
from PIL import ImageTk, Image

root = tk.Tk()

root.title("Maze Solver")
root.state('zoomed')

redButton = tk.Frame(root, background="red")
redButton.grid(row=0,column=0,sticky="NSEW")

root.columnconfigure(0,weight=1)
root.rowconfigure(0,weight=1)

root.mainloop()