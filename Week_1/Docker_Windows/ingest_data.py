#!/usr/bin/env python
# coding: utf-8

import argparse
from time import time
import pandas as pd
from sqlalchemy import create_engine
import wget
import os

def main(params):
    parquet_file = params.url
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    table_name = params.table_name
    file_name = 'output.csv'


    response = wget.download(parquet_file,'output.parquet')

    df = pd.read_parquet('output.parquet', engine = 'pyarrow') 

    df.head()

    output_file = 'output.csv' 
    df.to_csv(output_file, index = False)


    engine = create_engine('postgresql://{}:{}@{}:{}/{}'.format(user,password,host,port,db))


    df_iter = pd.read_csv(file_name,iterator=True,chunksize=100000)

    df = next(df_iter)

    df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
    df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

    df.head(n=0).to_sql(con=engine,name=table_name,if_exists='replace')

    df.to_sql(con=engine,name=table_name,if_exists='append')

    while True:
        
        t_start = time()
        
        df = next(df_iter)
        
        df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
        df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)
        df.to_sql(con=engine,name=table_name,if_exists='append')
        
        t_end = time()
        
        print('insert another chunk..., it took {} seconds'.format(t_end - t_start))





if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Ingest CSV data to Postgres')

    parser.add_argument('--user',help='user name for postgres')
    parser.add_argument('--password',help='password for postgres')
    parser.add_argument('--port',help='port for postgres')
    parser.add_argument('--db',help='database name for postgres')
    parser.add_argument('--url',help='url of the csv file')
    parser.add_argument('--table_name',help='table name within the database')
    parser.add_argument('--host',help='host for postgres db')

    args = parser.parse_args()

    main(args)



