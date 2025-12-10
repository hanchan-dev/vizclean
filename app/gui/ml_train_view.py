# app/gui/ml_train_view.py
import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext

import pandas as pd

from app.ml.model_trainer import ModelTrainer
from app.ml.model_saver import ModelSaver

class MLTrainView(ttk.Frame):
    """
    GUI untuk training model.
    Menyimpan pipeline hasil training ke self.app.model_pipeline
    dan metadata ke self.app.model_meta.
    """

    def __init__(self, app, container, df):
        super().__init__(container)
        self.app = app
        self.df = df
        self.pack(fill="both", expand=True)

        self.inputs = {}

        ttk.Label(self, text="Train Model", font=("Segoe UI", 16, "bold")).pack(pady=15)

        # target column combobox
        ttk.Label(self, text="Target Column").pack()
        self.target_box = ttk.Combobox(self, values=list(self.df.columns), width=50)
        self.target_box.pack(pady=6)

        # model choice
        ttk.Label(self, text="Model").pack()
        models = ["RandomForest", "LogisticRegression", "SVM", "KNN"]
        self.model_box = ttk.Combobox(self, values=models, width=50)
        self.model_box.set(models[0])
        self.model_box.pack(pady=6)

        # split ratio
        ttk.Label(self, text="Test Size (fraction, e.g. 0.2)").pack()
        self.split_entry = ttk.Entry(self, width=20)
        self.split_entry.insert(0, "0.2")
        self.split_entry.pack(pady=6)

        # Train button
        ttk.Button(self, text="Train", command=self.train_model).pack(pady=10)

        # Save model button
        ttk.Button(self, text="Save Model to File", command=self.save_model_dialog).pack(pady=6)

        # Back
        ttk.Button(self, text="Back to ML Menu", command=lambda: app.switch_page("ml_menu")).pack(pady=8)

        # output box
        ttk.Label(self, text="Output / Logs").pack(pady=8)
        self.log_box = scrolledtext.ScrolledText(self, width=100, height=12)
        self.log_box.pack(padx=10, pady=6)

    def train_model(self):
        target = self.target_box.get().strip()
        model_name = self.model_box.get().strip()
        test_size_str = self.split_entry.get().strip()

        if not target:
            messagebox.showwarning("Input error", "Pilih target column.")
            return

        try:
            test_size = float(test_size_str)
            if not (0.01 < test_size < 0.5):
                # izinkan range umum; user bisa ubah jika mau
                pass
        except Exception:
            messagebox.showwarning("Input error", "Masukkan test size sebagai angka desimal, misal 0.2")
            return

        try:
            self.log_box.delete("1.0", tk.END)
            self.log_box.insert(tk.END, f"Training model {model_name} dengan target '{target}'...\n")

            result = ModelTrainer.train(self.df, target_col=target, model_name=model_name, test_size=test_size)

            pipeline = result["pipeline"]
            accuracy = result["accuracy"]

            # simpan ke app state
            self.app.model_pipeline = pipeline
            self.app.model_meta = {
                "model_name": model_name,
                "target": target,
                "accuracy": accuracy
            }

            self.log_box.insert(tk.END, f"Training selesai.\nAccuracy (on test split): {accuracy:.4f}\n")
            self.log_box.insert(tk.END, "Model pipeline tersimpan di memori aplikasi.\n")
            messagebox.showinfo("Training Completed", f"Training selesai. Accuracy: {accuracy:.4f}")

        except Exception as e:
            messagebox.showerror("Training Error", str(e))
            self.log_box.insert(tk.END, f"Error: {e}\n")

    def save_model_dialog(self):
        # jika belum ada model terlatih, beri pilihan untuk menyimpan tetap
        if not hasattr(self.app, "model_pipeline") or self.app.model_pipeline is None:
            messagebox.showwarning("No Model", "Belum ada model terlatih. Latih model terlebih dahulu.")
            return

        path = filedialog.asksaveasfilename(
            defaultextension=".pkl",
            filetypes=[("Pickle", "*.pkl")]
        )
        if not path:
            return

        try:
            ModelSaver.save(self.app.model_pipeline, path)
            messagebox.showinfo("Saved", f"Model disimpan di: {path}")
        except Exception as e:
            messagebox.showerror("Save Error", str(e))
