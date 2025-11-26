import pandas as pd
import numpy as np
import datetime
import pandas.api.types as ptypes
from .logger import CleaningLogger


# Membersihkan data pada kolom
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

def trim_text_columns(df, log):

    trim_counts = {}

    for col in df.select_dtypes(include=["object"]).columns:
        original = df[col].astype(str)
        trimmed = original.str.strip()
        trimmed = trimmed.replace("nan", pd.NA)

        changed = (original != trimmed)
        changed_count = changed.sum()

        if changed_count > 0:
            trim_counts[col] = int(changed_count)

        df[col] = trimmed

    log.add("trim_column_values", {"affected_columns": trim_counts})
    return df

# convert string numeric to numeric
# def convert_numeric(df, log, digit_treshold=0.5):
#
#     numeric_counts = {}
#     nrows = len(df)
#
#     for col in df.select_dtypes(include=["object"]).columns:
#         original = df[col].astype(str)
#
#         has_digit = original.str.contains(r'\d', regex=True, na=False)
#         digit_ratio = has_digit.sum() / max(1, nrows)
#
#
#         if digit_ratio > digit_treshold:
#
#             extracted = original.str.extract(r'(\d+\.?\d*)')[0]
#
#             changed = (original != extracted)
#             changed_count = int(changed.sum())
#
#             converted = pd.to_numeric(extracted, errors='coerce')
#
#             if converted.notna().any():
#                 df[col] = converted
#
#                 if changed_count > 0:
#                     numeric_counts[col] = changed_count
#
#             else:
#                 pass
#
#         else:
#             continue
#
#     log.add("convert_numeric", {"affected_columns": numeric_counts})
#     return df

def convert_numeric(df, log, digit_treshold=0.5):

    numeric_counts = {}
    nrows = len(df)

    for col in df.select_dtypes(include=["object"]).columns:

        # ignore kolom yang sudah diproses sebagai date
        if ptypes.is_datetime64_any_dtype(df[col]):
            continue

        original = df[col].astype(str)

        has_digit = original.str.contains(r'\d', regex=True, na=False)
        digit_ratio = has_digit.sum() / max(1, nrows)

        if digit_ratio <= digit_treshold:
            continue

        extracted = original.str.extract(r'(\d+\.?\d*)')[0]
        converted = pd.to_numeric(extracted, errors='coerce')

        changed_count = (df[col] != converted.astype("object")).sum()

        df[col] = converted

        if changed_count > 0:
            numeric_counts[col] = int(changed_count)

    log.add("convert_numeric", {"affected_columns": numeric_counts})
    return df


# def convert_date(df, log):
#
#     # date_regex = re.compile(r'^(\d{4}[-/\.]\d{1,2}[-/\.]\d{1,2}|\d{1,2}[-/\.]\d{1,2}[-/\.]\d{4})$')
#     date_regex = re.compile(
#         r'^(\d{4}[-/.]\d{1,2}[-/.]\d{1,2}|\d{1,2}[-/.]\d{1,2}[-/.]\d{4})$'
#     )
#     date_counts = {}
#
#     for col in df.select_dtypes(include=["object"]).columns:
#         col_str = df[col].astype(str)
#
#         # match_ratio = col_str.str.match(date_regex).mean()
#         mask = col_str.str.match(date_regex) | df[col].isna()
#         match_ratio = mask.mean()
#
#         # if col_str.str.match(date_regex).all():
#         if match_ratio > 0.6:
#             original = col_str
#
#             # converted_dt = pd.to_datetime(original, errors='coerce', infer_datetime_format=True).dt.strftime('%Y-%m-%d')
#             converted_dt = pd.to_datetime(col_str, errors='coerce')
#
#             # changed = (original != converted_dt)
#             # changed_count = changed.sum()
#
#             # changed_count = (df[col] != converted_dt.astype(str)).sum()
#             changed_count = df[col].ne(converted_dt.astype("object")).sum()
#
#             if changed_count > 0:
#                 date_counts[col] = int(changed_count)
#
#             df[col] = converted_dt
#
#
#     log.add("convert_date", {"affected_columns": date_counts})
#     return df

# def convert_date(df, log):
#
#     date_regex = re.compile(
#         r'^(\d{4}[-/.]\d{1,2}[-/.]\d{1,2}|\d{1,2}[-/.]\d{1,2}[-/.]\d{4})$'
#     )
#
#     date_counts = {}
#
#     for col in df.select_dtypes(include=["object"]).columns:
#         col_str = df[col].astype(str)
#
#         # Cek rasio data yang MATCH dengan pola tanggal
#         match_mask = col_str.str.match(date_regex)
#         match_ratio = match_mask.mean()
#
#         # Hanya kolom yang >60% cocok dianggap kolom tanggal
#         if match_ratio <= 0.6:
#             continue
#
#         # Convert HANYA value yang match regex
#         converted = pd.to_datetime(
#             col_str.where(match_mask),     # hanya yang cocok regex
#             errors='coerce'                # gagal jadi NaN
#         )
#
#         # Hitung perubahan
#         changed_count = df[col].ne(converted.astype("object")).sum()
#
#         if changed_count > 0:
#             date_counts[col] = int(changed_count)
#
#         df[col] = converted
#
#     log.add("convert_date", {"affected_columns": date_counts})
#     return df

# def convert_date(df, log):
#
#     date_regex = re.compile(
#         r'^(\d{4}[-/.]\d{1,2}[-/.]\d{1,2}|\d{1,2}[-/.]\d{1,2}[-/.]\d{4})$'
#     )
#
#     date_counts = {}
#
#     for col in df.select_dtypes(include=["object"]).columns:
#         col_str = df[col].astype(str)
#
#         # hanya nilai yang PERSIS cocok format date
#         is_date = col_str.str.match(date_regex)
#
#         # minimal 1 baris cocok → proses!
#         if is_date.sum() == 0:
#             continue
#
#         converted_dt = pd.to_datetime(
#             col_str.where(is_date),  # hanya convert yang cocok
#             errors="coerce"
#         )
#
#         # changed_count = df[col].ne(converted_dt.astype("object")).sum()
#         changed_count = (
#                 df[col].astype("string").fillna("") !=
#                 converted_dt.astype("string").fillna("")
#         ).sum()
#
#         if changed_count > 0:
#             date_counts[col] = int(changed_count)
#
#         df[col] = converted_dt
#
#     log.add("convert_date", {"affected_columns": date_counts})
#     return df

def is_date_column(series):
    return series.dropna().apply(lambda x: isinstance(x, datetime.date)).all()

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


def normalize_text(df, log):

    normalize_counts = {}

    for col in df.columns:

        if ptypes.is_numeric_dtype(df[col]) or ptypes.is_datetime64_any_dtype(df[col]) or is_date_column(df[col]):
            continue  # JANGAN sentuh datetime atau numeric

        original = df[col].astype(str)

        normalized = (
            original.str.lower()
                .str.replace(r"[^a-z0-9\s]", "", regex=True)
                .str.replace(r"\s+", " ", regex=True)
                .str.strip()
        )

        normalized = normalized.replace(["", "nan"], np.nan)

        changed_count = (original != normalized).sum()

        if changed_count > 0:
            normalize_counts[col] = int(changed_count)

        df[col] = normalized

    log.add("normalize_text", {"affected_columns": normalize_counts})
    return df


# def normalize_text(df, log):
#
#     normalize_counts = {}
#
#     for col in df.select_dtypes(include=["object"]).columns:
#         original = df[col].astype(str)
#
#         normalized = (
#             original.str.lower()
#                 # .str.replace(r"[^a-zA-Z0-9\s.,;:!?_-]", '', regex=True)
#                 .str.replace(r"[^a-zA-Z0-9\s]", '', regex=True)
#                 .str.replace(r"\s+", " ", regex=True)
#                 .str.strip()
#         )
#
#         normalized = normalized.replace(["", "nan"], np.nan)
#         changed_count = (original != normalized).sum()
#
#         if changed_count > 0:
#             normalize_counts[col] = int(changed_count)
#
#         df[col] = normalized
#
#     log.add("normalize_text", {
#         "affected_columns": normalize_counts
#     })
#
#     return df



def clean_data(df):
    log = CleaningLogger()

    df = df.copy()

    # df = clean_column_name(df, log)
    # # df = replace_empty_as_nan(df, log)
    # df = trim_text_columns(df, log)
    # df = convert_date(df, log)
    # df = normalize_text(df, log)
    # df = fill_missing(df, log)
    # df = convert_numeric(df, log)
    # df = drop_entry_duplicate(df, log)

    df = clean_column_name(df, log)
    df = trim_text_columns(df, log)

    # 1. Konversi date dulu
    df = convert_date(df, log)

    # 2. Normalisasi hanya untuk text object
    df = normalize_text(df, log)

    # 3. Baru numeric
    # df = convert_numeric(df, log)

    # 4. Isi missing
    df = fill_missing(df, log)

    # 5. Drop duplikasi
    df = drop_entry_duplicate(df, log)

    return df, log.get_log()


