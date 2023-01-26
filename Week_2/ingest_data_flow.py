#!/usr/bin/env python
# coding: utf-8

import argparse
from time import time
import pandas as pd
from sqlalchemy import create_engine
import wget
import os
from prefect import flow, task
from prefect.tasks import task_input_hash
from prefect_sqlalchemy import SqlAlchemyConnector
from datetime import timedelta

#create a task to extract the data
@task(log_prints=True,tags=['extract'],cache_key_fn=task_input_hash,cache_expiration=timedelta(days=1))
def extract_data(url:str):
    parquet_file = url
    file_name = 'output.csv'

    response = wget.download(parquet_file,'output.parquet')

    df = pd.read_parquet('output.parquet', engine = 'pyarrow') 

    df.head()

    output_file = 'output.csv' 
    df.to_csv(output_file, index = False)

    df_iter = pd.read_csv(file_name,iterator=True,chunksize=100000)

    df = next(df_iter)

    df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
    df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

    return df

#create a task to transform the data
@task(log_prints=True)
def transform_data(data):
    print("pre: missing passenger count: {}".format(data['passenger_count'].isin([0]).sum()))
    df = data[data['passenger_count'] != 0]
    print('post: missing passenger count: {}'.format(df['passenger_count'].isin([0]).sum()))
    return df


#create a task to load the data
@task(log_prints=True,retries=3)
def load_data(table_name,data):


    connection_block = SqlAlchemyConnector.load("postgres-connector")

    with connection_block.get_connection(begin=False) as engine:

        data.head(n=0).to_sql(con=engine,name=table_name,if_exists='replace')
        data.to_sql(con=engine,name=table_name,if_exists='append')



    #engine = create_engine('postgresql://{}:{}@{}:{}/{}'.format(user,password,host,port,db))

    

    


@flow(name="subflow",log_prints=True)
def log_subflow(table_name: str):
    print("Logging subflow for: {}".format(table_name))

#create the flow
@flow(name="Ingest Data")
def main_flow(table_name:str):

    # user = "root"
    # password = "root"
    # host = "localhost"
    # port = "5432"
    # db = "ny_taxi"
    #table_name = "yellow_taxi_trips"
    url = "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2022-01.parquet"
    log_subflow(table_name)

    raw_data = extract_data(url)
    data = transform_data(raw_data)

    load_data(table_name,data)

if __name__ == '__main__':
    
    main_flow(table_name = "yellow_trips")
