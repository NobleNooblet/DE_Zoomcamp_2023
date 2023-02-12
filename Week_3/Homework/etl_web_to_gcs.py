from pathlib import Path
import pandas as pd
from prefect import flow, task
from prefect_gcp.cloud_storage import GcsBucket
import wget


@task(retries=3)
def fetch(dataset_url: str,filename: str) -> pd.DataFrame:
    """Read taxi data from web into pandas DataFrame"""

    #from random import randint

    # if randint(0,1) > 0:
    #     raise Exception

    #df = pd.read_csv(dataset_url)
    #return df
    result = wget.download(dataset_url,'./data/{}.csv.gz'.format(filename))

# @task(log_prints=True)
# def clean(df = pd.DataFrame) -> pd.DataFrame:
#     """Fix dtype issues"""
#     df['lpep_dropoff_datetime'] = pd.to_datetime(df['lpep_dropoff_datetime'])
#     df['lpep_pickup_datetime'] = pd.to_datetime(df['lpep_pickup_datetime'])
#     #print(df.head(2))
#     #print('Columns: {}'.format(df.dtypes))
#     #print('Rows: {}'.format(len(df)))
#     return df

# @task()
# def write_local(df:pd.DataFrame,color:str,dataset_file:str) -> Path:
#     """Write Dataframe out as a parquet file"""
#     path = Path('data/{}/{}.parquet'.format(color,dataset_file))
#     df.to_parquet(path,compression='gzip')
#     return path

@task()
def write_gcs(from_path: Path,to_path: Path) -> None:
    """Uploading gzip file to GCS"""
    gcs_block = GcsBucket.load("zoom-gcs")
    gcs_block.upload_from_path(
        from_path=from_path,
        to_path=to_path.as_posix()
    )
    return


@flow()
def etl_web_to_gcs(year,month) -> None:
    """The main ETL function"""
    dataset_file = f'fhv_tripdata_{year}-{month:02}'
    dataset_url = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/fhv/{}.csv.gz'.format(dataset_file)


    fetch(dataset_url,dataset_file)
    from_path = Path('data/{}.csv.gz'.format(dataset_file))
    to_path = Path('data/fhv/{}.csv.gz'.format(dataset_file))
    write_gcs(from_path,to_path)

if __name__ == '__main__':
    counter = 1
    print(counter)
    while counter <= 12:
        etl_web_to_gcs(2019,counter)
        counter +=1

