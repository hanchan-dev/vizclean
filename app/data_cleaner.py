import pandas as pd
import numpy as np
import re
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

        changed = (original != trimmed)
        changed_count = changed.sum()

        if changed_count > 0:
            trim_counts[col] = int(changed_count)

        df[col] = trimmed

    log.add("trim_column_values", {"affected_columns": trim_counts})
    return df

# convert string numeric to numeric
def convert_numeric(df, log, digit_treshold=0.5):

    numeric_counts = {}
    nrows = len(df)

    for col in df.select_dtypes(include=["object"]).columns:
        original = df[col].astype(str)

        has_digit = original.str.contains(r'\d', regex=True, na=False)
        digit_ratio = has_digit.sum() / max(1, nrows)


        if digit_ratio > digit_treshold:

            extracted = original.str.extract(r'(\d+\.?\d*)')[0]

            changed = (original != extracted)
            changed_count = int(changed.sum())

            converted = pd.to_numeric(extracted, errors='coerce')

            if converted.notna().any():
                df[col] = converted

                if changed_count > 0:
                    numeric_counts[col] = changed_count

            else:
                pass

        else:
            continue

    log.add("convert_numeric", {"affected_columns": numeric_counts})
    return df

def convert_date(df, log):

    date_regex = re.compile(r'^(\d{4}[-/\.]\d{1,2}[-/\.]\d{1,2}|\d{1,2}[-/\.]\d{1,2}[-/\.]\d{4})$')
    date_counts = {}

    for col in df.select_dtypes(include=["object"]).columns:
        col_str = df[col].astype(str)

        if col_str.str.match(date_regex).all():
            original = col_str

            converted_dt = pd.to_datetime(original, errors='coerce', infer_datetime_format=True).strftime('%Y-%m-%d')

            changed = (original != converted_dt)
            changed_count = changed.sum()

            if changed_count > 0:
                date_counts[col] = int(changed_count)

            df[col] = converted_dt

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

    for col in df.select_dtypes(include=["object"]).columns:
        original = df[col].astype(str)

        normalized = (
            original.str.lower()
                # .str.replace(r"[^a-zA-Z0-9\s.,;:!?_-]", '', regex=True)
                .str.replace(r"[^a-zA-Z0-9\s]", '', regex=True)
                .str.replace(r"\s+", " ", regex=True)
                .str.strip()
        )

        normalized = normalized.replace(["", "nan"], np.nan)
        changed_count = (original != normalized).sum()

        if changed_count > 0:
            normalize_counts[col] = int(changed_count)

        df[col] = normalized

    log.add("normalize_text", {
        "affected_columns": normalize_counts
    })

    return df


# def replace_empty_as_nan(df, log):
#     # replace "", " ", "   ", "\n", "\t" → NaN
#     df = df.replace(r'^\s*$', np.nan, regex=True)
#
#     # logging
#     missing_counts = {}
#     for col in df.columns:
#         empty_count = df[col].isna().sum()
#         if empty_count > 0:
#             missing_counts[col] = int(empty_count)
#
#     log.add("replace_empty_as_nan", {"affected_columns": missing_counts})
#     return df




def clean_data(df):
    log = CleaningLogger()

    df = df.copy()

    df = clean_column_name(df, log)
    # df = replace_empty_as_nan(df, log)
    df = trim_text_columns(df, log)
    df = normalize_text(df, log)
    df = convert_numeric(df, log)
    df = convert_date(df, log)
    df = fill_missing(df, log)
    df = drop_entry_duplicate(df, log)

    return df, log.get_log()


