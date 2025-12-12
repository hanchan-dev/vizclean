import tkinter as tk
from tkinter import ttk
from app.gui.chart_viewer import ChartViewer


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


        canvas = tk.Canvas(self, highlightthickness=0)
        scroll_y = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)

        canvas.configure(yscrollcommand=scroll_y.set)

        canvas.pack(side="left", fill="both", expand=True)
        scroll_y.pack(side="right", fill="y")

        scroll_frame = ttk.Frame(canvas)
        canvas_window = canvas.create_window((0, 0), window=scroll_frame, anchor="nw")

        def resize_canvas(event):
            # update the window width inside canvas
            canvas.itemconfig(canvas_window, width=event.width)

        canvas.bind("<Configure>", resize_canvas)

        scroll_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )


        center_holder = ttk.Frame(scroll_frame)
        center_holder.pack(fill="both", expand=True)

        inner_wrapper = ttk.Frame(center_holder)
        inner_wrapper.pack(anchor="center", pady=20)


        ttk.Label(inner_wrapper, text=f"{chart_type.upper()} SETTINGS",
                  font=("Segoe UI", 16, "bold")).pack(pady=10)


        self.chart_fields = {
            "line": [
                ("Column", "col", df.columns),
                ("Title", "title"),
                ("Color", "color1"),
                ("Grid (yes/no)", "grid",),
                ("X Label", "x_label"),
                ("Y Label", "y_label"),
                ("Marker", "marker"),
                ("Marker Size", "markersize"),
                ("Max Items (optional)", "limit")
            ],

            "bar": [
                ("Column", "col", df.columns),
                ("Title", "title"),
                ("X Label", "x_label"),
                ("Y Label", "y_label"),
                ("Color", "color1"),
                ("Grid (yes/no)", "grid"),
                ("Max Items (optional)", "limit")
            ],

            "pie": [
                ("Column", "col", df.columns),
                ("Title", "title"),
                ("Max Items (optional)", "limit")
            ],

            "scatter": [
                ("Column 1", "col_1", df.columns),
                ("Column 2", "col_2", df.columns),
                ("Title", "title"),
                ("X Label", "x_label"),
                ("Y Label", "y_label"),
                ("Color 1", "color1"),
                ("Color 2", "color2"),
                ("Marker 1", "marker"),
                ("Marker 2", "marker2"),
                ("Legend 1", "legend1"),
                ("Legend 2", "legend2"),
                ("Size", "markersize"),
                ("Grid (yes/no)", "grid"),
                ("Max Items (optional)", "limit")
            ],


            "histogram": [
                ("Column", "col", df.columns),
                ("Title", "title"),
                ("Color", "color1"),
                ("X Label", "x_label"),
                ("Y Label", "y_label"),
                ("Grid (yes/no)", "grid"),
                ("Max Items (optional)", "limit")
            ]
        }


        for field in self.chart_fields[self.chart_type]:
            label, key = field[0], field[1]

            ttk.Label(inner_wrapper, text=label).pack()

            # kalau ada pilihan kolom → combobox
            if len(field) == 3:
                values = list(field[2])
                box = ttk.Combobox(inner_wrapper, values=values, width=35)
                box.pack(pady=4)
                self.inputs[key] = box
            else:
                entry = ttk.Entry(inner_wrapper, width=40)
                entry.pack(pady=4)
                self.inputs[key] = entry

        ttk.Button(inner_wrapper,
                   text="Generate Chart",
                   command=self.generate).pack(pady=15)

        ttk.Button(inner_wrapper,
                   text="Back",
                   command=lambda: switch_page("chart_menu")
                   ).pack(pady=10)



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
