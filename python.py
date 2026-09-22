import pandas as pd

df = pd.read_parquet("yellow_tripdata_2024-02.parquet")

print(df.shape)                      # rows, columns
print(df.dtypes)                     # schema
print(df.head())                     # sample rows
print(df.isnull().sum())             # nulls per column
print(df["tpep_pickup_datetime"].min(), df["tpep_pickup_datetime"].max())
print((df["trip_distance"] <= 0).sum(), "rows with zero/negative distance")
print((df["fare_amount"] <= 0).sum(), "rows with zero/negative fare")

