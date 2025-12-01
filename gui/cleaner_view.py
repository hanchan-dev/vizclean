import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from app.core.data_cleaner import clean_data


class CleanerView:

    def __init__(self, app, container, df):
        self.app = app
        self.frame = tk.Frame(container)
        self.frame.pack(fill="both", expand=True)

        ttk.Label(
            self.frame,
            text="Data Cleaning",
            font=("Segoe UI", 18, "bold")
        ).pack(pady=20)

        try:
            cleaned_df, logs = clean_data(df)
            self.app.df_cleaned = cleaned_df
        except Exception as e:
            messagebox.showerror("Error", str(e))
            app.show_home()
            return

        log_box = scrolledtext.ScrolledText(self.frame, width=120, height=25)
        log_box.pack(padx=15, pady=10)

        for step, detail in logs.items():
            log_box.insert(tk.END, f"{step}:\n{detail}\n\n")

        ttk.Button(
            self.frame,
            text="Back to Home",
            command=self.app.show_home
        ).pack(pady=20)
