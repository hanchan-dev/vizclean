# app/gui/ml_test_view.py
import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext

from app.ml.model_saver import ModelSaver
from app.ml.model_tester import ModelTester

class MLTestView(ttk.Frame):
    """
    GUI untuk testing model.
    Bisa memakai model yang tersimpan di app.model_pipeline atau load dari file .pkl
    """

    def __init__(self, app, container, df):
        super().__init__(container)
        self.app = app
        self.df = df
        self.pack(fill="both", expand=True)

        ttk.Label(self, text="Test Model", font=("Segoe UI", 16, "bold")).pack(pady=12)

        # Info model status
        self.model_label = ttk.Label(self, text=self._model_status_text())
        self.model_label.pack(pady=6)

        # Load model from file
        ttk.Button(self, text="Load Model from File (.pkl)", command=self.load_model_file).pack(pady=6)

        # Choose target for test data
        ttk.Label(self, text="Target Column (test data)").pack()
        self.target_box = ttk.Combobox(self, values=list(self.df.columns), width=50)
        self.target_box.pack(pady=6)

        # Test button
        ttk.Button(self, text="Run Test on Current Data", command=self.run_test_current).pack(pady=8)

        # Save predictions
        ttk.Button(self, text="Save Predictions (CSV)", command=self.save_predictions).pack(pady=6)

        ttk.Button(self, text="Back to ML Menu", command=lambda: app.switch_page("ml_menu")).pack(pady=8)

        ttk.Label(self, text="Report / Output").pack(pady=8)
        self.report_box = scrolledtext.ScrolledText(self, width=100, height=18)
        self.report_box.pack(padx=10, pady=6)

        self.latest_predictions = None
        self.latest_report = None

    def _model_status_text(self):
        if hasattr(self.app, "model_pipeline") and self.app.model_pipeline is not None:
            meta = getattr(self.app, "model_meta", {})
            name = meta.get("model_name", "unknown")
            acc = meta.get("accuracy", None)
            if acc is not None:
                return f"Model in-memory: {name} (accuracy: {acc:.4f})"
            return f"Model in-memory: {name}"
        return "No model loaded in memory."

    def load_model_file(self):
        path = filedialog.askopenfilename(filetypes=[("Pickle", "*.pkl")])
        if not path:
            return
        try:
            model = ModelSaver.load(path)
            self.app.model_pipeline = model
            self.model_label.config(text=self._model_status_text())
            messagebox.showinfo("Loaded", f"Model loaded from {path}")
        except Exception as e:
            messagebox.showerror("Load Error", str(e))

    def run_test_current(self):
        if not hasattr(self.app, "model_pipeline") or self.app.model_pipeline is None:
            messagebox.showwarning("No Model", "Belum ada model di memori. Load model atau latih dulu.")
            return

        target = self.target_box.get().strip()
        if not target:
            messagebox.showwarning("Input error", "Pilih target column untuk testing.")
            return

        try:
            result = ModelTester.run_test(self.app.model_pipeline, self.df, target_col=target)
            acc = result["accuracy"]
            report = result["report"]
            cm = result["confusion_matrix"]

            self.latest_predictions = result["predictions"]
            self.latest_report = report

            self.report_box.delete("1.0", tk.END)
            self.report_box.insert(tk.END, f"Accuracy: {acc:.4f}\n\n")
            self.report_box.insert(tk.END, "Confusion Matrix:\n")
            self.report_box.insert(tk.END, f"{cm}\n\n")
            self.report_box.insert(tk.END, "Classification Report:\n")
            self.report_box.insert(tk.END, f"{report}\n")

            messagebox.showinfo("Test Completed", f"Testing selesai. Accuracy: {acc:.4f}")

        except Exception as e:
            messagebox.showerror("Testing Error", str(e))

    def save_predictions(self):
        if self.latest_predictions is None:
            messagebox.showwarning("No Predictions", "Jalankan testing terlebih dahulu.")
            return

        path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV", "*.csv")])
        if not path:
            return

        try:
            # attach predictions to df then save
            out_df = self.df.copy()
            out_df["__prediction__"] = self.latest_predictions
            out_df.to_csv(path, index=False)
            messagebox.showinfo("Saved", f"Predictions saved to {path}")
        except Exception as e:
            messagebox.showerror("Save Error", str(e))
