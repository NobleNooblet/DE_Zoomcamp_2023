import pandas as pd
from prefect import flow, task
from prefect_gcp.cloud_storage import GcsBucket
from prefect_gcp import GcpCredentials

gcs_block = GcsBucket.load("data-engineering-project")
gcp_credentials_block = GcpCredentials.load("gcp-project-service-account")
#df = pd.read_csv('gs://bucket/your_path.csv')

@task(log_prints=True)
def load_gcs_file(gcs_file):
    """
    This function loads the gcs files and returns the data as a pandas data frame.
    Parameters:
        gcs_file -> This is the name of the file in the GCS bucket.
    """
    gcs_path = 'gs://project_data_bucket_dataengineeringproject-380415/raw_data/esport_earnings/{}.csv'.format(gcs_file)
    df = pd.read_csv(gcs_path)
    return df

@task(log_prints=True)
def upload_to_bq(df,table_name):
    """
    This function loads data into Big Query
    Parameters:
        df -> Pandas data frame with the data to load into BQ
        table_name -> The biq query table name to be used
    """
    df.to_gbq(
        destination_table='staging_project_data.{}'.format(table_name),
        project_id='dataengineeringproject-380415',
        credentials=gcp_credentials_block.get_credentials_from_service_account(),
        if_exists='replace'
    )

@flow(name="GCS to BQ")
def main_flow(gcs_file,table_name):
    """
    This is the main flow function that kicks off the load_gcs_file and upload_to_bq functions
    """
    print('Reading {}...'.format(gcs_file))
    df = load_gcs_file(gcs_file)
    print('{} loaded in a data frame...'.format(gcs_file))


    upload_to_bq(df,table_name)
    print('{} successfully loaded into Google Big Query staging data set'.format(table_name))
    


if __name__ == '__main__':

    data_files = {"country-and-continent-codes-list":"country_codes","highest_earning_players":"player_earnings"}
    for file in data_files:
        main_flow(file,data_files[file])



