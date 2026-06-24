import shap
import joblib
import pandas as pd

print("Loading Model...")

model = joblib.load(
    "saved_models/random_forest.pkl"
)

print("Loading Dataset...")

df = pd.read_csv(
    "C:/Users/Ashika.Adhirai/Downloads/Intelligent Log Analytics & Anomaly Detection Platform/HDFS_v1/data/Event_occurrence_matrix.csv"
)

features = [f"E{i}" for i in range(1,30)]

X = df[features]

sample_X = X.sample(
    1000,
    random_state=42
)

print("Creating Explainer...")

explainer = shap.TreeExplainer(model)

print("Calculating SHAP Values...")

shap_values = explainer.shap_values(sample_X)

print("Type:", type(shap_values))

try:
    print("Shape:", shap_values.shape)
except:
    print("Length:", len(shap_values))

shap.summary_plot(
    shap_values,
    sample_X
)