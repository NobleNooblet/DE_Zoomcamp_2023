import pandas as pd
from prefect import flow, task
from kaggle.api.kaggle_api_extended import KaggleApi
from pathlib import Path
from prefect_gcp.cloud_storage import GcsBucket


#authenticate with Kaggle
api = KaggleApi()
api.authenticate()



@task(log_prints=True)
def download_input_files(dataset):
    print('Downloading data set to local repository')
    api.dataset_download_files(dataset, path="./input",unzip=True)
    print('Files successfully downloaded')

@task(log_prints=True)
def write_gcs(file_name):
    """Uploading gzip file to GCS"""
    gcs_block = GcsBucket.load("data-engineering-project")

    print('Uploading {} to GCS bucket'.format(file_name))
    from_path = Path('..\\data\\{}'.format(file_name))
    to_path = Path('raw_data/esport_earnings/{}'.format(file_name))

    gcs_block.upload_from_path(
        from_path=from_path,
        to_path=to_path.as_posix()
    )

    print('Upload completed successfully')

@flow(name="Ingest Data")
def main_flow(dataset):

    lisft_of_files = ['highest_earning_players.csv','country-and-continent-codes-list.csv']
    print('Initiating main flow...')

    download_input_files(dataset)

    for file in lisft_of_files:
        write_gcs(file)
    


if __name__ == '__main__':
    main_flow('jackdaoud/esports-earnings-for-players-teams-by-game')

