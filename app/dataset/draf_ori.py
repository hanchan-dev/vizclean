import pandas as pd
import numpy as np
import re

from pandas.core.interchange.dataframe_protocol import DataFrame

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


# trim columns value
# def trim_text_columns(df, log):
#     for col in df.select_dtypes(include=["object"]).columns:
#         df[col] = df[col].astype(str).str.strip()
#
#     log.add({"trim columns value": "done"})
#     return df

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
def convert_numeric(df, log):
    numeric_regex = re.compile(r'^-?\d+(\.\d+)?$')
    numeric_counts = {}

    for col in df.select_dtypes(include=["object"]).columns:
        col_str = df[col].astype(str)

        if col_str.str.match(numeric_regex).all():
            original = col_str
            converted = pd.to_numeric(original, errors='coerce')

            changed = (original != converted)
            changed_count = changed.sum()

            if changed_count > 0:
                numeric_counts[col] = int(changed_count)

            df[col] = converted

    log.add("convert_numeric", {"affected_columns": numeric_counts})
    return df

    # for col in df.select_dtypes(include=["object"]).columns:
    #     is_numeric = df[col].astype(str).str.match(numeric_regex).all()
    #
    #     if is_numeric:
    #         df[col] = pd.to_numeric(df[col], errors='coerce')
    #
    #         log.add({f"converted_to_numeric_{col}": df[col].isna().sum()})

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

        elif df[col].dtype in [np.int64, np.float64]:
            median = df[col].median()
            filled = df[col].fillna(median)
            df[col] = filled
            numeric_log[col] = int(missing_before)

        else:
            mode = df[col].mode()
            fill_value = mode[0] if not mode.empty else 'Unknown'
            filled = df[col].fillna(fill_value)
            df[col] = filled

    # filled_count = df[col].isna().sum()
    # if filled_count > 0:
    #     log.add("fill_mising_value", {f"filled_missing_{col}": int(filled_count)})
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

        changed_count = (original != normalized).sum()

        if changed_count > 0:
            normalize_counts[col] = int(changed_count)

        df[col] = normalized

    log.add("normalize_text", {
        "affected_columns": normalize_counts
    })

    return df




def clean_data(df):
    log = CleaningLogger()

    df = df.copy()

    df = clean_column_name(df, log)
    df = trim_text_columns(df, log)
    df = normalize_text(df, log)
    df = convert_numeric(df, log)
    df = convert_date(df, log)
    df = fill_missing(df, log)
    df = drop_entry_duplicate(df, log)

    return df, log.get_log()


