import tkinter as tk
from tkinter import ttk
from gui.chart_viewer import ChartViewer


class ChartForm(ttk.Frame):

    def __init__(self, app, master, df, chart_type, switch_page):
        super().__init__(master)
        self.app = app
        self.master = master
        self.df = df
        self.chart_type = chart_type
        self.switch_page = switch_page

        self.pack(fill="both", expand=True)

        self.inputs = {}

        ttk.Label(self, text=f"{chart_type.upper()} SETTINGS",
                  font=("Segoe UI", 16, "bold")).pack(pady=10)

        # --- struktur input tiap chart ------------------------

        # self.chart_fields = {
        #     "line": [
        #         ("Title", "title"),
        #         ("X Column", "x_col", df.columns),
        #         ("Y Column", "y_col", df.columns),
        #         ("X Label", "x_label"),
        #         ("Y Label", "y_label"),
        #         ("Marker", "marker"),
        #         ("Marker Size", "markersize"),
        #         ("Color", "color1"),
        #         ("Grid (yes/no)", "grid")
        #     ],
        #
        #     "bar": [
        #         ("Title", "title"),
        #         ("X Column", "x_col", df.columns),
        #         ("Y Column", "y_col", df.columns),
        #         ("X Label", "x_label"),
        #         ("Y Label", "y_label"),
        #         ("Color", "color1"),
        #         ("Grid (yes/no)", "grid")
        #     ],
        #
        #     "pie": [
        #         ("Title", "title"),
        #         ("Labels Column", "x_col", df.columns),
        #         ("Values Column", "y_col", df.columns),
        #     ],
        #
        #     "scatter": [
        #         ("Title", "title"),
        #         ("X Column (Set 1)", "x_col", df.columns),
        #         ("Y Column (Set 1)", "y_col", df.columns),
        #         ("X Column (Set 2)", "x_col1", df.columns),
        #         ("Y Column (Set 2)", "y_col2", df.columns),
        #         ("Legend 1", "legend1"),
        #         ("Legend 2", "legend2"),
        #         ("X Label", "x_label"),
        #         ("Y Label", "y_label"),
        #         ("Color 1", "color1"),
        #         ("Color 2", "color2"),
        #     ],
        #
        #     "histogram": [
        #         ("Title", "title"),
        #         ("Column", "x_col", df.columns),
        #         ("X Label", "x_label"),
        #         ("Y Label", "y_label"),
        #         ("Bins", "bins"),
        #         ("Color", "color1"),
        #         ("Grid (yes/no)", "grid")
        #     ]
        # }

        self.chart_fields = {
            "line": [
                ("Title", "title"),
                ("Column", "col", df.columns),
                ("Color", "color1"),
                ("Grid (yes/no)", "grid",),
                ("X Label", "x_label"),
                ("Y Label", "y_label"),
                ("Marker", "marker"),
                ("Marker Size", "markersize"),
                ("Max Items (optional)", "limit")
            ],

            "bar": [
                ("Title", "title"),
                ("Column", "col", df.columns),
                ("X Label", "x_label"),
                ("Y Label", "y_label"),
                ("Color", "color1"),
                ("Grid (yes/no)", "grid"),
                ("Max Items (optional)", "limit")
            ],

            "pie": [
                ("Title", "title"),
                ("Column", "col", df.columns),
                ("Max Items (optional)", "limit")
            ],

            "scatter": [
                ("Title", "title"),
                ("Column 1", "col_1", df.columns),
                ("Column 2", "col_2", df.columns),
                ("X Label", "x_label"),
                ("Y Label", "y_label"),
                ("Color 1", "color1"),
                ("Color 2", "color2"),
                ("Marker 1", "marker"),
                ("Marker 2", "marker2"),
                ("Size", "markersize"),
                ("Grid (yes/no)", "grid"),
                ("Max Items (optional)", "limit")
            ],


            "histogram": [
                ("Title", "title"),
                ("Column", "col", df.columns),
                ("Bins", "bins"),
                ("Color", "color1"),
                ("X Label", "x_label"),
                ("Y Label", "y_label"),
                ("Grid (yes/no)", "grid"),
                ("Max Items (optional)", "limit")
            ]
        }

        # --- render input field otomatis -----------------------------

        for field in self.chart_fields[self.chart_type]:
            label, key = field[0], field[1]

            ttk.Label(self, text=label).pack()

            # kalau ada pilihan kolom → combobox
            if len(field) == 3:
                values = list(field[2])
                box = ttk.Combobox(self, values=values, width=35)
                box.pack(pady=4)
                self.inputs[key] = box
            else:
                entry = ttk.Entry(self, width=40)
                entry.pack(pady=4)
                self.inputs[key] = entry

        ttk.Button(self,
                   text="Generate Chart",
                   command=self.generate).pack(pady=15)

        ttk.Button(self,
                   text="Back",
                   command=lambda: switch_page("chart_menu")
                   ).pack(pady=10)

    # def generate(self):
    #     params = {k: v.get() for k, v in self.inputs.items()}
    #
    #     if "grid" in params:
    #         params["grid"] = params["grid"].strip().lower() == "yes"
    #
    #     if "bins" in params and params["bins"].isdigit():
    #         params["bins"] = int(params["bins"])
    #
    #     # Hapus form
    #     for widget in self.master.winfo_children():
    #         widget.destroy()
    #
    #     ChartViewer(
    #         master=self.master,
    #         switch_page=self.switch_page,
    #         df=self.df,
    #         chart_type=self.chart_type,
    #         **params
    #     )

    def generate(self):
        params = {k: v.get() for k, v in self.inputs.items()}

        if "grid" in params:
            params["grid"] = params["grid"].strip().lower() == "yes"

        if "bins" in params and params["bins"].isdigit():
            params["bins"] = int(params["bins"])

        if "limit" in params:
            params["limit"] = int(params["limit"]) if params["limit"].isdigit() else None

        if "markersize" in params:
            params["markersize"] = int(params["markersize"]) if params["markersize"].strip().isdigit() else 6

        for widget in self.master.winfo_children():
            widget.destroy()

        ChartViewer(
            master=self.master,
            switch_page=self.switch_page,
            df=self.df,
            chart_type=self.chart_type,
            **params
        )
