import datetime

import pandas as pd
import pandas.api.types as ptypes
from app.core.logger import CleaningLogger


class DataCleaner:

    # Membersihkan data pada kolom
    @staticmethod
    def clean_column_name(df, log):
        original_cols = df.columns.tolist()

        df.columns = (
            df.columns.str.strip()
            .str.lower()
            .str.replace(' ', '_')
            .str.replace(r'[^a-zA-Z0-9_]', '', regex=True)
        )

        log.add("clean_column_name", {
            'before': original_cols,
            'after': df.columns.tolist()
        })

        return df


    # drop entry & duplicate
    @staticmethod
    def trim_text_columns(df, log):

        trim_counts = {}

        for col in df.select_dtypes(include=["object"]).columns:
            original = df[col].astype(str)
            trimmed = original.str.strip()
            # trimmed = trimmed.replace("nan", pd.NA)

            changed = (original != trimmed)
            changed_count = changed.sum()

            if changed_count > 0:
                trim_counts[col] = int(changed_count)

            df[col] = trimmed

        log.add("trim_column_values", {"affected_columns": trim_counts})
        return df

    @staticmethod
    def convert_date(df, log):

        date_counts = {}

        for col in df.select_dtypes(include=["object"]).columns:

            col_series = df[col]

            # Ambil 100 sample agar tidak berat
            sample = col_series.dropna().astype(str).head(100)

            if sample.empty:
                continue

            # coba parse
            parsed = pd.to_datetime(sample, errors="coerce", format="mixed")

            success_ratio = parsed.notna().mean()

            # Lebih dari 30% berhasil → kemungkinan besar kolom tanggal
            if success_ratio < 0.3:
                continue

            # Parse seluruh kolom
            full_parsed = pd.to_datetime(col_series, errors="coerce", format="mixed").dt.date

            changed_count = (
                col_series.astype(str).fillna("") !=
                full_parsed.astype(str).fillna("")
            ).sum()

            if changed_count > 0:
                date_counts[col] = int(changed_count)

            df[col] = full_parsed

        log.add("convert_date", {"affected_columns": date_counts})
        return df

    # convert string numeric to numeric
    @staticmethod
    def is_date_column(series):
        return series.dropna().apply(lambda x: isinstance(x, datetime.date)).all()



    @staticmethod
    def convert_numeric(df, log, digit_treshold=0.5):

        numeric_counts = {}
        nrows = len(df)

        for col in df.select_dtypes(include=["object"]).columns:

            if ptypes.is_datetime64_any_dtype(df[col]) or DataCleaner.is_date_column(df[col]):
                continue

            original = df[col]

            # Nilai string sebelum diubah
            old_str = original.astype(str).fillna("")

            has_digit = old_str.str.contains(r'\d', regex=True, na=False)
            digit_ratio = has_digit.sum() / max(1, nrows)

            if digit_ratio <= digit_treshold:
                continue

            extracted = old_str.str.extract(r'(\d+\.?\d*)')[0]
            converted = pd.to_numeric(extracted, errors='coerce')

            # String setelah diubah
            new_str = converted.astype(str).fillna("")

            # DETEKSI PERUBAHAN: nilai atau tipe
            changed_count = ((old_str != new_str) | (original.dtype != converted.dtype)).sum()

            df[col] = converted

            if changed_count > 0:
                numeric_counts[col] = int(changed_count)

        log.add("convert_numeric", {"affected_columns": numeric_counts})
        return df

    @staticmethod
    def normalize_text(df, log):

        normalize_counts = {}

        for col in df.columns:

            if ptypes.is_numeric_dtype(df[col]) or ptypes.is_datetime64_any_dtype(df[col]) or DataCleaner.is_date_column(df[col]):
                continue  # JANGAN sentuh datetime atau numeric

            original = df[col].astype(str)

            normalized = (
                original.str.lower()
                    .str.replace(r"[^a-z0-9\s]", "", regex=True)
                    .str.replace(r"\s+", "", regex=True)
                    .str.strip()
            )

            normalized = normalized.replace(["", "nan"], pd.NA)

            changed_count = (original != normalized).sum()

            if changed_count > 0:
                normalize_counts[col] = int(changed_count)

            df[col] = normalized

        log.add("normalize_text", {"affected_columns": normalize_counts})
        return df

    @staticmethod
    def fill_missing(df, log):

        numeric_log = {}
        category_log = {}

        for col in df.columns:
            missing_before = df[col].isna().sum()

            if missing_before == 0:
                continue

            if ptypes.is_numeric_dtype(df[col]):
                non_null = df[col].dropna()
                if not non_null.empty:
                    median = non_null.median()
                    df[col] = df[col].fillna(median)
                    numeric_log[col] = missing_before
                else:
                    continue

            else:
                # mode = df[col].mode()
                # fill_value = mode[0] if not mode.empty else 'Unknown'
                df[col] = df[col].fillna("unknown")
                category_log[col] = missing_before

        log.add("fill_mising_value", {
            "numeric": numeric_log,
            "categorical": category_log
        })

        return df


    @staticmethod
    def drop_entry_duplicate(df, log):
        before = len(df)

        df = df.dropna(how='all')
        after_dropna = len(df)

        df = df.drop_duplicates(keep='first')
        after_dedup = len(df)

        log.add("drop_entry_duplicate", {
            "dropped_nan": before - after_dropna,
            "dropped_duplicates": after_dropna - after_dedup,
            "total_after_cleaning": after_dedup
        })

        return df

    @staticmethod
    def clean_data(df):
        log = CleaningLogger()
        raw_df = df.copy()

        cleaned_df = DataCleaner.clean_column_name(raw_df, log)
        cleaned_df = DataCleaner.trim_text_columns(cleaned_df, log)
        # cleaned_df = DataCleaner.convert_date(cleaned_df, log)
        cleaned_df = DataCleaner.normalize_text(cleaned_df, log)
        cleaned_df = DataCleaner.convert_numeric(cleaned_df, log)
        cleaned_df = DataCleaner.fill_missing(cleaned_df, log)
        cleaned_df = DataCleaner.drop_entry_duplicate(cleaned_df, log)

        return cleaned_df, log.get_log()


