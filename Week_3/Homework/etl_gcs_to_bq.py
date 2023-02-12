from pathlib import Path
import pandas as pd
from prefect import flow, task
from prefect_gcp.cloud_storage import GcsBucket
from prefect_gcp import GcpCredentials


@task
def read_data(path: Path) -> pd.DataFrame:
    """Data cleaning example"""

    df = pd.read_csv(path)
    return df

@task()
def write_bq(df:pd.DataFrame)->None:
    """Write DF to BigQuery"""
    gcp_credentials_block = GcpCredentials.load("zoom-gcp-creds")

    df.to_gbq(
        destination_table='trips_data_all.fhv_2019',
        project_id='dtc-de-course-375810',
        credentials=gcp_credentials_block.get_credentials_from_service_account(),
        chunksize=500_000,
        if_exists='append'
    )

@flow()
def etl_gcs_to_bq(year,month):
    """Main ETL flow to load data into biq Query data warehouse"""
    path = f'./data/fhv_tripdata_{year}-{month:02}.csv.gz'
    df = read_data(path)
    write_bq(df)

if __name__ == '__main__':
    year = 2019
    month = 1
    while month <= 12:
        print(month)
        etl_gcs_to_bq(year,month)
        month +=1