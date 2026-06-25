import pandas as pd


def load_data(filepath):
    """
    Load Event Occurrence Matrix dataset
    """
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