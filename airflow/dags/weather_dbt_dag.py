from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    "retries": 2,
    "retry_delay": timedelta(minutes=2),
}

with DAG(
    dag_id="weather_pipeline_dbt",
    start_date=datetime(2024, 1, 1),
    schedule="@daily",
    catchup=False,
    default_args=default_args,
    tags=["weather", "dbt"],
) as dag:

    dbt_run = BashOperator(
        task_id="dbt_run",
        bash_command="""
        dbt run \
        --project-dir /opt/airflow/weather_dbt \
        --profiles-dir /opt/airflow/.dbt
        """,
    )

    dbt_test = BashOperator(
        task_id="dbt_test",
        bash_command="""
        dbt test \
        --project-dir /opt/airflow/weather_dbt \
        --profiles-dir /opt/airflow/.dbt
        """,
    )

    dbt_run >> dbt_test