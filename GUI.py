import tkinter as tk
from config import win_width, win_height, win_bg_color
root = tk.Tk()
root.geometry(f'{win_width}x{win_height}')
root['bg'] = win_bg_color

header = tk.Label(root, text='Craft', fg='red', bg=win_bg_color, font='Tahoma 25')
header.place(relx=0.02, rely=0.02)


# тут всякие объекты графические и их расположение