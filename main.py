from tkinter import Tk
from config import screen_w, screen_h
root = Tk()
root.geometry(f'{screen_w}x{screen_h}')

if __name__ == '__main__':
    root.mainloop()