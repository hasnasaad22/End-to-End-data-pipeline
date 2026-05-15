FROM apache/airflow:2.8.4

USER airflow

RUN pip install --no-cache-dir \
    dbt-core==1.8.2 \
    dbt-postgres==1.8.2 \
    requests \
    psycopg2-binary

ENV PATH="${PATH}:/home/airflow/.local/bin"

USER root

RUN apt-get update && apt-get install -y git

USER airflow


