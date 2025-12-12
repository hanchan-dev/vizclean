import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class MLTrainPlotView(ttk.Frame):

    def __init__(self, app, container, train_result, switch_back):
        """
        train_result = dictionary dari ModelTrainer.train()
        switch_back = fungsi untuk kembali ke MLTrainView
        """
        super().__init__(container)
        self.app = app
        self.train_result = train_result
        self.switch_back = switch_back

        self.fig = None
        self.canvas = None

        self.pack(fill="both", expand=True)

        # Title
        ttk.Label(
            self,
            text="Training Plot",
            font=("Segoe UI", 16, "bold")
        ).pack(pady=20)

        ttk.Button(self, text="Generate Plot", command=self.generate_plot).pack(pady=8)
        ttk.Button(self, text="Save Plot", command=self.save_plot).pack(pady=8)
        ttk.Button(self, text="Back", command=self.switch_back).pack(pady=20)

        # Frame untuk menempatkan plot
        self.plot_frame = tk.Frame(self)
        self.plot_frame.pack(fill="both", expand=True)

    def generate_plot(self):
        try:
            if self.canvas:
                self.canvas.get_tk_widget().destroy()

            from sklearn.metrics import ConfusionMatrixDisplay
            y_test = self.train_result["y_test"]
            predictions = self.train_result["predictions"]

            self.fig = plt.Figure(figsize=(6, 4), dpi=100)
            ax = self.fig.add_subplot(111)
            ConfusionMatrixDisplay.from_predictions(y_test, predictions, ax=ax)
            ax.set_title("Confusion Matrix (Training Test Split)")

            # embed canvas
            self.canvas = FigureCanvasTkAgg(self.fig, master=self.plot_frame)
            self.canvas.draw()
            self.canvas.get_tk_widget().pack(fill="both", expand=True)

        except Exception as e:
            messagebox.showerror("Plot Error", str(e))

    def save_plot(self):
        if not self.fig:
            messagebox.showwarning("No Plot", "Buat plot dulu.")
            return

        path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG", "*.png")]
        )

        if path:
            self.fig.savefig(path)
            messagebox.showinfo("Saved", "Plot saved successfully.")
