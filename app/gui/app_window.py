import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd

from app.gui.cleaner_view import CleanerView
from app.gui.chart_menu import ChartMenu


class AppWindow(tk.Frame):

    def __init__(self, master):
        super().__init__(master)
        self.master = master

        master.title("Vizclean: Data Cleaner & Chart Generator")
        master.geometry("720x480")

        self.df = None
        self.df_cleaned = None

        # MAIN CONTAINER
        self.container = tk.Frame(master)
        self.container.pack(fill="both", expand=True)

        self.show_home()

    # ================= HOME PAGE =================

    def show_home(self):
        """Reset container lalu tampilkan halaman Home."""
        self.clear_container()

        frame = tk.Frame(self.container)
        frame.pack(fill="both", expand=True)

        ttk.Label(
            frame,
            text="Welcome to VizClean",
            font=("Segoe UI", 22, "bold")
        ).pack(pady=25)

        ttk.Button(
            frame,
            text="Upload Dataset (CSV / Excel)",
            command=self.upload_file,
            width=40
        ).pack(pady=10)

        ttk.Button(
            frame,
            text="Clean Data",
            command=self.open_cleaner,
            width=40
        ).pack(pady=10)

        ttk.Button(
            frame,
            text="Chart Menu",
            command=self.open_chart_menu,
            width=40
        ).pack(pady=10)

        ttk.Button(
            frame,
            text="Exit",
            command=self.master.quit,
            width=20
        ).pack(pady=20)



    def switch_page(self, page_name):
        """Controller navigasi seperti router kecil."""
        self.clear_container()

        if page_name == "home":
            self.show_home()

        elif page_name == "chart_menu":
            df_source = self.df_cleaned if self.df_cleaned is not None else self.df
            ChartMenu(self, self.container, df_source)

        else:
            raise ValueError(f"Unknown page: {page_name}")

    # ================ UTILITY ================

    def clear_container(self):
        """Hapus seluruh widget sebelum ganti halaman."""
        for widget in self.container.winfo_children():
            widget.destroy()

    # =================== FILE UPLOAD ====================

    def upload_file(self):
        filepath = filedialog.askopenfilename(
            filetypes=[
                ("CSV Files", "*.csv"),
                ("Excel Files", "*.xlsx;*.xls")
            ]
        )
        if not filepath:
            return

        try:
            if filepath.endswith(".csv"):
                self.df = pd.read_csv(filepath)
            else:
                self.df = pd.read_excel(filepath)

            messagebox.showinfo("Success", "Dataset loaded successfully.")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to load file:\n{e}")

    # =================== CLEANER VIEW ====================

    def open_cleaner(self):
        if self.df is None:
            messagebox.showwarning("No Data", "Upload dataset first.")
            return

        self.clear_container()
        CleanerView(self, self.container, self.df)

    # =================== CHART MENU ====================

    def open_chart_menu(self):

        try:
            if self.df is None:
                messagebox.showwarning("No Data", "Upload dataset first.")
                return

            df_source = self.df_cleaned if self.df_cleaned is not None else self.df

            self.clear_container()
            ChartMenu(self, self.container, df_source)

        except Exception as e:
            messagebox.showwarning("Type Error", f"{e}")
            return
