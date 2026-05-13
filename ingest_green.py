import pandas as pd
from sqlalchemy import create_engine

parquet_file = "green_tripdata_2025-11.parquet"

engine = create_engine("postgresql://root:root@127.0.0.1:5433/ny_taxi")

df = pd.read_parquet(parquet_file)

print(df.head())
print(df.dtypes)
print(f"Rows: {len(df)}")

df.to_sql(
    name="green_tripdata_2025_11",
    con=engine,
    if_exists="replace",
    index=False,
    chunksize=100000
)

print("green_tripdata_2025_11 loaded successfully")