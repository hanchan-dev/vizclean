import tkinter as tk
from tkinter import ttk
from gui.chart_form import ChartForm


class ChartMenu:

    def __init__(self, app, container, df):
        self.app = app
        self.df = df

        self.frame = tk.Frame(container)
        self.frame.pack(fill="both", expand=True)

        ttk.Label(
            self.frame,
            text="Choose Chart Type",
            font=("Segoe UI", 18, "bold")
        ).pack(pady=20)

        charts = ["line", "bar", "pie", "scatter", "histogram"]

        for c in charts:
            ttk.Button(
                self.frame,
                text=c.upper(),
                width=30,
                command=lambda t=c: self.open_form(t)
            ).pack(pady=5)

        ttk.Button(
            self.frame,
            text="Back to Home",
            width=20,
            command=self.app.show_home
        ).pack(pady=20)

    def open_form(self, chart_type):
        self.frame.destroy()
        # ChartForm(self.app, self.app.container, self.df, chart_type)
        ChartForm(
            app=self.app,
            master=self.app.container,
            df=self.df,
            chart_type=chart_type,
            switch_page=self.app.switch_page
        )
