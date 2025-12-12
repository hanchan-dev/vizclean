import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class MLTestPlotView(ttk.Frame):
    def __init__(self, app, container, test_result, switch_back):
        super().__init__(container)
        self.app = app
        self.test_result = test_result
        self.switch_back = switch_back

        self.fig = None
        self.canvas = None

        self.pack(fill="both", expand=True)

        ttk.Label(
            self,
            text="Testing Plot",
            font=("Segoe UI", 16, "bold")
        ).pack(pady=20)

        ttk.Button(self, text="Generate Plot", command=self.generate_plot).pack(pady=8)
        ttk.Button(self, text="Save Plot", command=self.save_plot).pack(pady=8)
        ttk.Button(self, text="Back", command=self.switch_back).pack(pady=20)

        self.plot_frame = tk.Frame(self)
        self.plot_frame.pack(fill="both", expand=True)

    def generate_plot(self):
        try:
            if self.canvas:
                self.canvas.get_tk_widget().destroy()

            from sklearn.metrics import ConfusionMatrixDisplay

            cm = self.test_result["confusion_matrix"]
            y_true = self.test_result["y_test"]
            y_pred = self.test_result["predictions"]

            self.fig = plt.Figure(figsize=(6, 4), dpi=100)
            ax = self.fig.add_subplot(111)
            ConfusionMatrixDisplay.from_predictions(y_true, y_pred, ax=ax)
            ax.set_title("Confusion Matrix (Testing Data)")

            self.canvas = FigureCanvasTkAgg(self.fig, master=self.plot_frame)
            self.canvas.draw()
            self.canvas.get_tk_widget().pack(fill="both", expand=True)

        except Exception as e:
            messagebox.showerror("Plot Error", str(e))

    def save_plot(self):
        if not self.fig:
            messagebox.showwarning("No Plot", "Generate plot first.")
            return

        path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG", "*.png")]
        )
        if path:
            self.fig.savefig(path)
            messagebox.showinfo("Saved", "Plot saved successfully.")
