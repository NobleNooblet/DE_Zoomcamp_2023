from pathlib import Path
import pandas as pd
from prefect import flow, task
from prefect_gcp.cloud_storage import GcsBucket
from random import randint
from prefect.tasks import task_input_hash
from datetime import timedelta



@task(retries=3,log_prints=True)
def fetch(dataset_url: str) -> pd.DataFrame:
    """Read taxi data from web into pandas DataFrame"""

    from random import randint

    # if randint(0,1) > 0:
    #     raise Exception

    df = pd.read_csv(dataset_url)
    print(len(df.index))
    return df

@task(log_prints=True)
def clean(df = pd.DataFrame) -> pd.DataFrame:
    """Fix dtype issues"""
    df['lpep_dropoff_datetime'] = pd.to_datetime(df['lpep_dropoff_datetime'])
    df['lpep_pickup_datetime'] = pd.to_datetime(df['lpep_pickup_datetime'])
    #print(df.head(2))
    #print('Columns: {}'.format(df.dtypes))
    #print('Rows: {}'.format(len(df)))
    return df

@task(log_prints=True)
def write_local(df:pd.DataFrame,color:str,dataset_file:str) -> Path:
    """Write Dataframe out as a parquet file"""
    path = Path('data/{}/{}.parquet'.format(color,dataset_file))
    df.to_parquet(path,compression='gzip')
    return path

@task(log_prints=True)
def write_gcs(path: Path) -> None:
    """Uploading local parquet file to GCS"""
    gcs_block = GcsBucket.load("zoom-gcs")
    gcs_block.upload_from_path(
        from_path=path,
        to_path=path.as_posix()
    )
    return


@flow()
def etl_web_to_gcs(year: int, month: int, color: str) -> None:
    """The main ETL function"""
    dataset_file = f'{color}_tripdata_{year}-{month:02}'
    dataset_url = f'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/{color}/{dataset_file}.csv.gz'

    df = fetch(dataset_url)
    df_clean = clean(df)
    path = write_local(df_clean,color,dataset_file)
    write_gcs(path)

@flow()
def etl_parent_flow(
    months: list[int] = [1,2], year: int = 2021, color: str = 'yellow'):

    for month in months:
        etl_web_to_gcs(year,month,color)

if __name__ == '__main__':
    color = 'yellow'
    months = [1,2,3]
    year = 2021
    etl_parent_flow(months,year,color)

