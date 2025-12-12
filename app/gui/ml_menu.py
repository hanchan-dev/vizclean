import tkinter as tk
from tkinter import ttk
from app.gui.ml_train_view import MLTrainView
from app.gui.ml_test_view import MLTestView

class MLMenu:
    def __init__(self, app, container, df):
        self.app = app
        self.df = df

        self.frame = tk.Frame(container)
        self.frame.pack(fill="both", expand=True)

        ttk.Label(
            self.frame,
            text="Machine Learning Classifier",
            font=("Segoe UI", 18, "bold")
        ).pack(pady=20)

        ttk.Button(
            self.frame,
            text="Train Model",
            width=30,
            command=self.open_train
        ).pack(pady=8)

        ttk.Button(
            self.frame,
            text="Test Model",
            width=30,
            command=self.open_test
        ).pack(pady=8)

        ttk.Button(
            self.frame,
            text="Back to Home",
            width=20,
            command=self.app.show_home
        ).pack(pady=20)

    def open_train(self):
        self.frame.destroy()
        MLTrainView(self.app, self.app.container, self.df)

    def open_test(self):
        self.frame.destroy()
        MLTestView(self.app, self.app.container, self.df)
