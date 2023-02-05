from pathlib import Path
import pandas as pd
from prefect import flow, task
from prefect_gcp.cloud_storage import GcsBucket
from prefect_gcp import GcpCredentials

@task()
def extract_from_gcs(color:str,year:int,month:str) -> Path:
    """Download trip data from GCS"""
    gcs_path = f'data/{color}/{color}_tripdata_{year}-{month:02}.parquet'
    gcs_block = GcsBucket.load("zoom-gcs")
    gcs_block.get_directory(from_path=gcs_path,local_path='../')
    return Path('../{}'.format(gcs_path))

@task
def transform(path: Path) -> pd.DataFrame:
    """Data cleaning example"""

    df = pd.read_parquet(path)
    print('pre: missing passenger count: {}'.format(df['passenger_count'].isna().sum()))
    df['passenger_count'].fillna(0, inplace=True)
    print('post: missing passenger count: {}'.format(df['passenger_count'].isna().sum()))
    return df

@task()
def write_bq(df:pd.DataFrame)->None:
    """Write DF to BigQuery"""
    gcp_credentials_block = GcpCredentials.load("zoom-gcp-creds")

    df.to_gbq(
        destination_table='trips_data_all.rides',
        project_id='dtc-de-course-375810',
        credentials=gcp_credentials_block.get_credentials_from_service_account(),
        chunksize=500_000,
        if_exists='append'
    )

@flow()
def etl_gcs_to_bq():
    """Main ETL flow to load data into biq Query data warehouse"""
    color='yellow'
    year=2021
    month = '01'
    path = extract_from_gcs(color,year,month)
    df = transform(path)
    write_bq(df)

if __name__ == '__main__':
    etl_gcs_to_bq()