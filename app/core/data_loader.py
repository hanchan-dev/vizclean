import pandas as pd

class FileLoader:
    @staticmethod
    def load_file(self, file_path: str):
        """Load a CSV file into a pandas DataFrame."""
        try:
            ext = file_path.split('.')[-1].lower()

            if ext == 'csv':
                df = pd.read_csv(file_path)
            elif ext == 'xlsx' or ext == 'xls':
                df = pd.read_excel(file_path)
            elif ext == 'parquet':
                df = pd.read_parquet(file_path)
            else:
                raise ValueError("Unsupported file format. Please provide a CSV or Excel file.")

            return df

        except Exception as e:
            print(f"Error loading file {file_path}: {e}")
            return None