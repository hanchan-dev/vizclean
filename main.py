import tkinter as tk
from app.gui.app_window import AppWindow


if __name__ == '__main__':
    root = tk.Tk()
    root.title('VizClean')
    root.geometry('900x600')
    AppWindow(root)

    root.mainloop()
