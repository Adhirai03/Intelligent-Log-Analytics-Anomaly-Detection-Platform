import pandas as pd

df = pd.read_csv("C:/Users/Ashika.Adhirai/Downloads/Intelligent Log Analytics & Anomaly Detection Platform/HDFS_v1/data/Event_occurrence_matrix.csv")

features = [f"E{i}" for i in range(1,30)]

print("Total Rows:", len(df))
print("Duplicate Rows:", df.duplicated().sum())
print("Duplicate Block IDs:", df["BlockId"].duplicated().sum())
print("Duplicate Event Patterns:", df[features].duplicated().sum())
print("Unique Event Patterns:", len(df[features].drop_duplicates()))