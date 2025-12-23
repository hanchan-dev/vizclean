

# VizClean - Data Cleaning, Visualization, and Machine Learning GUI

VizClean adalah aplikasi desktop berbasis **Python + Tkinter** yang dirancang untuk membantu proses **data cleaning**, **visualisasi data**, serta **training & testing model Machine Learning** melalui antarmuka grafis (GUI).

Aplikasi ini ditujukan untuk keperluan tugas matakuliah Artificial Intelligence, yang dimana bisa eksplorasi data, dan eksperimen machine learning tanpa harus menulis perintah command line secara manual.

---

## Features

### 1. Input Data 📂
- Load dataset (CSV / Excel)

### 2. Data Cleaning (Automatic & Logged) 🧹
- Normalisasi nama kolom
- Trim whitespace
- Konversi tanggal otomatis
- Konversi numerik dari string
- Handling missing values
- Drop duplicate & empty rows
- **Cleaning log ditampilkan secara detail di GUI**

### 3. Data Visualization 📊
- Line Chart
- Bar Chart
- Pie Chart
- Histogram
- Scatter Plot
- Custom parameter (warna, label, limit, grid)
- Save plot ke file `.png`

### 4. Machine Learning (Supervised Classification)🤖
- Model yang tersedia:
  - Random Forest
  - Logistic Regression
  - Support Vector Machine (SVM)
  - K-Nearest Neighbors (KNN)
- Preprocessing otomatis:
  - Numeric scaling
  - Categorical encoding
- Pipeline berbasis `scikit-learn`
- Training & testing melalui GUI 
- Save / load model (`.pkl`) 
- Generate & save prediction output 
- **Visualisasi performa model (plot) di halaman terpisah**

---

## Project Structure
```
vizclean/
│
├── app/
│ ├── core/
│ │ ├── data_loader.py
│ │ ├── data_cleaner.py
│ │ ├── charting.py
│ │ └── logger.py
│ │
│ ├── ml/
│ │ ├── model_preprocessor.py
│ │ ├── model_trainer.py
│ │ ├── model_tester.py
│ │ ├── model_saver.py
│ │ └── metrics.py
│ │
│ └── gui/
│ ├── app_window.py
│ ├── cleaner_view.py
│ ├── chart_menu.py
│ ├── chart_form.py
│ ├── chart_viewer.py
│ ├── ml_menu.py
│ ├── ml_train_view.py
│ ├── ml_test_view.py
│ ├── ml_train_plot_view.py
│ └── ml_test_plot_view.py
│
├── main.py
├── requirements.txt
└── README.md
```


---

## Dataset Characteristics

- Dataset tabular (CSV / XLSX)
- Mendukung:
  - Numeric features
  - Categorical features
  - Date features
- Target column dipilih secara manual saat training/testing
- Tidak ada asumsi khusus terhadap domain dataset
- Dataset yang tersedia:
  - dataset utama yang digunakan pada tugas ini
      - vgsales.csv (Video Game Sales Dataset)
  - dataset cadangan untuk percobaan lain
      - netflix_titles.csv (Netflix Titles Dataset)
---

## Machine Learning Configuration

| Parameter             | Value                        |
|-----------------------|------------------------------|
| Task Type             | Supervised Classification    |
| Models                | RF, LR, SVM, KNN             |
| Train/Test Split      | User-defined (default 80/20) |
| Preprocessing         | Automatic (Pipeline)         |
| Hyperparameter Tuning | None (baseline-focused)      |
| Execution             | GUI-driven                   |

---

## How to Run

### Option 1 — Run from Source (Recommended for Development)

1. Pastikan Python 3.10+ terinstal
2. Buat virtual environment:
`python -m venv .venv`
3. Aktifkan environment:
`.venv\Scripts\activate`
4. Install dependencies:
`pip install -r requirements.txt`
5. Jalankan aplikasi:
`python main.py`


---

### Option 2 - Run as Executable (.exe)

Jika menggunakan versi `.exe` hasil PyInstaller:

- Tidak perlu install Python ataupun konfigurasi environment
- Jalankan langsung file `vizclean.exe`


---

## Output Files

### Visualization
- `.png` image files (chart & plot)

### Machine Learning
- `.pkl` → saved model
- `.csv` → prediction results

---

## Evaluation Notes

- Accuracy digunakan sebagai metrik dasar evaluasi
- Classification Report dan Confusion Matrix ditampilkan di GUI
- Plot performa model bersifat visual-support (bukan tuning)
- Fokus proyek ini adalah **pipeline, reproducibility, dan usability**, bukan hyperparameter optimization

---

## Design Philosophy

- Modular
- Object-Oriented Programming (OOP)
- Separation of concerns (core, ml, gui)
- GUI-first experience
- Minimal magic, explicit flow

---

## Conclusion

VizClean menggabungkan proses **data preparation**, **visual analytics**, dan **machine learning experimentation** dalam satu aplikasi desktop terpadu.  
Proyek ini menekankan pada kejelasan alur, transparansi proses, dan kemudahan penggunaan - terutama untuk kebutuhan akademik dan pembelajaran AI.

---

## Author

Developed by: 

Handika Chandra Pratama - **(230511049)**

Riswanto Rumasukun - **(230511086)**

M Naufal Aulia - **(230511042)**
