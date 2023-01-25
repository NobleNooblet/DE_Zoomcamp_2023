import wget
import pandas as pd

url = 'https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2022-01.parquet'

response = wget.download(url,'output.parquet')

df = pd.read_parquet('E:\PythonCourse\DE_Zoomcamp_2023\output.parquet', engine = 'pyarrow')

df.head()

output_file = 'E:\PythonCourse\DE_Zoomcamp/Week_1\Docker_Windows\output.csv'
df.to_csv(output_file, index = False)
