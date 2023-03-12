import pandas as pd
import wget
import os

from kaggle.api.kaggle_api_extended import KaggleApi
api = KaggleApi()
api.authenticate()


#kaggle.api.authenticate()

def download_input_files(dataset):
    api.dataset_download_files(dataset, path="./input",unzip=True)
if __name__ == '__main__':
    download_input_files('jackdaoud/esports-earnings-for-players-teams-by-game')

