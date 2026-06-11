import pandas as pd

files = [
    "daily_order_summary_2026-06-10.parquet",
    "cart_abandonment_summary_2026-06-10.parquet",
    "top_products_summary_2026-06-10.parquet"
]

for file in files:
    print("\n" + "=" * 80)
    print(file)
    print("=" * 80)

    df = pd.read_parquet(file)

    print("\nColumns:")
    print(df.columns.tolist())

    print("\nRows:")
    print(df)

    print("\nShape:")
    print(df.shape)