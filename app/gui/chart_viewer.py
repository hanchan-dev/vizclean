import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from app.core.charting import Chart


class ChartViewer(ttk.Frame):

    def __init__(self, master, switch_page, df, chart_type, **params):
        super().__init__(master)
        self.df = df
        self.chart_type = chart_type
        self.params = params
        self.switch_page = switch_page

        self.fig = None
        self.canvas = None

        self.pack(fill="both", expand=True)

        ttk.Label(
            self,
            text=f"{chart_type.upper()} CHART",
            font=("Segoe UI", 16, "bold")
        ).pack(pady=20)

        ttk.Button(
            self,
            text="Show Chart",
            command=self.show_chart
        ).pack(pady=10)

        ttk.Button(
            self,
            text="Save Chart",
            command=self.save_chart
        ).pack(pady=10)

        ttk.Button(
            self,
            text="Back",
            command=lambda: self.switch_page("chart_menu")
        ).pack(pady=20)

        # container tempat chart muncul
        self.chart_frame = tk.Frame(self)
        self.chart_frame.pack(fill="both", expand=True)


    # ======================================================

    def show_chart(self):
        try:
            # hapus canvas lama jika ada
            if self.canvas:
                self.canvas.get_tk_widget().destroy()

            # figure baru
            self.fig = plt.Figure(figsize=(6, 4), dpi=100)

            #
            # Pastikan create_chart menggambar pada self.fig
            #
            Chart.create_chart(
                df=self.df,
                chart_type=self.chart_type,
                fig=self.fig,
                **self.params
            )

            # embed figure ke Tkinter
            self.canvas = FigureCanvasTkAgg(self.fig, master=self.chart_frame)
            self.canvas.draw()
            self.canvas.get_tk_widget().pack(fill="both", expand=True)

        except Exception as e:
            messagebox.showerror("Error", str(e))


    def save_chart(self):
        if self.fig is None:
            messagebox.showwarning("No Chart", "Show the chart first.")
            return

        path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG", "*.png")]
        )
        if path:
            self.fig.savefig(path)
            messagebox.showinfo("Saved", "Chart saved successfully.")
