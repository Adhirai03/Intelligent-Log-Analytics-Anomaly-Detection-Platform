import pandas as pd
from pathlib import Path
from sklearn.preprocessing import LabelEncoder # converts text labels into numbers

ROOT_DIR = Path(__file__).resolve().parents[1]

def load_data(path):

    if isinstance(path, str):
        # Handle relative paths by resolving from ROOT_DIR
        if not path.startswith('/') and not ':' in path:
            path = ROOT_DIR / path
    
    df = pd.read_csv(path)

    # Convert labels
    df["Target"] = df["Label"].map({
        "Success":0,
        "Fail":1
    })

    features = [f"E{i}" for i in range(1,30)]

    X = df[features]
    y = df["Target"]

    return X,y,df