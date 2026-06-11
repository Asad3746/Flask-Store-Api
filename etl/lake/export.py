import os
import pandas as pd
from datetime import date
import boto3
from etl.db import get_conn

ENDPOINT = "https://s3.us-east-005.backblazeb2.com"
BUCKET = "etl-data-lake"

ACCESS_KEY = os.environ["B2_ACCESS_KEY"]
SECRET_KEY = os.environ["B2_SECRET_KEY"]

s3 = boto3.client(
    "s3",
    endpoint_url=ENDPOINT,
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY
)

today = date.today()


def upload_gold_table(query, name):
    with get_conn() as conn:
        df = pd.read_sql(query, conn)

    file_name = f"{name}_{today}.parquet"
    df.to_parquet(file_name, engine="pyarrow", index=False)

    s3.upload_file(
        file_name,
        BUCKET,
        f"gold/{name}/{file_name}"
    )

    os.remove(file_name)

    print(f"Uploaded and removed local file: {file_name}")


def run_exports():
    upload_gold_table(
        "SELECT * FROM gold.daily_order_summary",
        "daily_order_summary"
    )

    upload_gold_table(
        "SELECT * FROM gold.cart_abandonment_summary",
        "cart_abandonment_summary"
    )

    upload_gold_table(
        "SELECT * FROM gold.top_products_summary",
        "top_products_summary"
    )

if __name__ == "__main__":
    run_exports()