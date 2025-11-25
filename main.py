import tkinter as tk
from gui.app_window import AppWindow


if __name__ == '__main__':
    # df = pd.read_csv('app/dataset/coffee_raw3.csv')
    # cleaned, log = dc.clean_data(df)
    #
    # print(cleaned.to_string(), "\n\n")
    # print(log)
    #
    # cleaned.to_csv('cleaned.csv', index=False)

    root = tk.Tk()
    root.title('VizClean')
    root.geometry('900x600')
    AppWindow(root)

    root.mainloop()
