FROM python:3.9

RUN pip install pandas sqlalchemy psycopg2 wget pyarrow

WORKDIR /app

COPY ingest_green_taxi_data.py ingest_green_taxi_data.py

ENTRYPOINT ["python","ingest_green_taxi_data.py"]