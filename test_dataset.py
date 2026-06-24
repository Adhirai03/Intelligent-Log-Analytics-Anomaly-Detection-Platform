print("Program Started")

import pandas as pd

df = pd.read_csv(
    "C:/Users/Ashika.Adhirai/Downloads/Intelligent Log Analytics & Anomaly Detection Platform/HDFS_v1/data/Event_occurrence_matrix.csv"
)

print("Dataset Shape:")
print(df.shape)

print("\nColumns:")
print(df.columns.tolist())

print("\nFirst 5 Rows:")
print(df.head())