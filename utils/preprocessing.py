import pandas as pd
from sklearn.preprocessing import LabelEncoder

def load_data(path):

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