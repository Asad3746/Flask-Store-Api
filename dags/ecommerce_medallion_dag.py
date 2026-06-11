from etl.lake.export import run_exports
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator

DEFAULT_ARGS = {
    "owner": "etl",
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
    "email_on_failure": False,
}

def task_ingest():
    from etl.bronze.ingest import run_ingest
    run_ingest()

def task_clean():
    from etl.silver.clean import run_clean
    run_clean()

def task_aggregate():
    from etl.gold.aggregate import run_aggregate
    run_aggregate()

def task_export_lake():
    run_exports()

with DAG(
    dag_id="ecommerce_medallion",
    description="Bronze → Silver → Gold → Data Lake ETL",
    schedule="0 2 * * *",
    start_date=datetime(2024, 1, 1),
    catchup=False,
    default_args=DEFAULT_ARGS,
    tags=["ecommerce", "medallion"],
) as dag:

    ingest = PythonOperator(
        task_id="bronze_ingest",
        python_callable=task_ingest
    )

    clean = PythonOperator(
        task_id="silver_clean",
        python_callable=task_clean
    )

    agg = PythonOperator(
        task_id="gold_aggregate",
        python_callable=task_aggregate
    )

    lake = PythonOperator(
        task_id="lake_export",
        python_callable=task_export_lake
    )

    ingest >> clean >> agg >> lake