from pathlib import Path
import pandas as pd
from prefect import flow, task
from prefect_gcp.cloud_storage import GcsBucket


@task(retries=3)
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
    df['tpep_pickup_datetime'] = pd.to_datetime(df['tpep_pickup_datetime'])
    df['tpep_dropoff_datetime'] = pd.to_datetime(df['tpep_dropoff_datetime'])
    #print(df.head(2))
    #print('Columns: {}'.format(df.dtypes))
    #print('Rows: {}'.format(len(df)))
    return df

@task()
def write_local(df:pd.DataFrame,color:str,dataset_file:str) -> Path:
    """Write Dataframe out as a parquet file"""
    path = Path('data/{}/{}.parquet'.format(color,dataset_file))
    df.to_parquet(path,compression='gzip')
    return path

@task()
def write_gcs(path: Path) -> None:
    """Uploading local parquet file to GCS"""
    gcs_block = GcsBucket.load("zoom-gcs")
    gcs_block.upload_from_path(
        from_path=path,
        to_path=path.as_posix()
    )
    return


@flow()
def etl_web_to_gcs() -> None:
    """The main ETL function"""
    color = 'yellow'
    year = 2019
    month = '03'
    dataset_file = '{}_tripdata_{}-{}'.format(color,year,month)
    dataset_url = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/{}/{}.csv.gz'.format(color,dataset_file)


    df = fetch(dataset_url)
    df_clean = clean(df)
    path = write_local(df_clean,color,dataset_file)
    write_gcs(path)

if __name__ == '__main__':
    etl_web_to_gcs()

