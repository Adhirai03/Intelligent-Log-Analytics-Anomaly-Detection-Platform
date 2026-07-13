import pandas as pd
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]

def load_data(filepath):
    """
    Load Event Occurrence Matrix dataset
    """
    if isinstance(filepath, str):
        # Handle relative paths by resolving from ROOT_DIR
        if not filepath.startswith('/') and not ':' in filepath:
            filepath = ROOT_DIR / filepath
    df = pd.read_csv(filepath)
    return df


def get_total_logs(df):
    """
    Total number of log traces
    """
    return len(df)


def get_success_fail_counts(df):
    """
    Success vs Fail distribution
    """
    return df["Label"].value_counts()


def get_failure_type_distribution(df):
    """
    Distribution of failure types
    """
    fail_df = df[df["Label"] == "Fail"]

    return fail_df["Type"].value_counts().sort_index()


def get_top_events(df, top_n=10):
    """
    Most frequent event templates
    """

    event_cols = [
        col for col in df.columns
        if col.startswith("E")
    ]

    event_counts = df[event_cols].sum()

    return (
        event_counts
        .sort_values(ascending=False)
        .head(top_n)
    )

import pandas as pd

def get_anomaly_associated_events(df, templates, top_n=10):
    """
    Finds the events that are most associated with anomalies
    by comparing their occurrence in Success vs Fail logs.
    """

    # Split data
    success_df = df[df["Label"] == "Success"]
    fail_df = df[df["Label"] == "Fail"]

    # Event columns (E1, E2, ...)
    event_cols = [c for c in df.columns if c.startswith("E")]

    # Total occurrences in each class
    success_counts = success_df[event_cols].sum()
    fail_counts = fail_df[event_cols].sum()

    result = pd.DataFrame({
        "EventId": event_cols,
        "Success": success_counts.values,
        "Fail": fail_counts.values
    })

    # Association score
    result["AnomalyScore"] = (
        result["Fail"] /
        (result["Success"] + result["Fail"] + 1e-6)
    )

    # Ignore events never seen
    result = result[result["Fail"] > 0]

    # Merge with template file
    result = result.merge(
        templates,
        on="EventId",
        how="left"
    )

    # Sort by anomaly score
    result = result.sort_values(
        by="AnomalyScore",
        ascending=False
    )

    return result.head(top_n)