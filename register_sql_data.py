from azureml.core import Run, Workspace, Datastore, Dataset
from azureml.data.datapath import DataPath
import pandas as pd
import numpy as np
import os
import argparse
import datetime
import json
import tempfile
import shutil

#Parse input arguments
parser = argparse.ArgumentParser("Register SQL Data")
parser.add_argument('--sql_path_param', type=str, required=True)
parser.add_argument("--sql_dataset", dest='sql_dataset', required=True)

####### New 04-06-2021 #######
#add min_year/max_year parameters to this step to be used for data filtering
parser.add_argument("--min_year", type=int, required=True)
parser.add_argument("--max_year", type=int, required=True)

args, _ = parser.parse_known_args()
sql_path_param = args.sql_path_param
sql_dataset = args.sql_dataset
min_year = args.min_year
max_year = args.max_year

#Get current run
current_run = Run.get_context()

#Get associated AML workspace
ws = current_run.experiment.workspace

#Get default datastore
ds = ws.get_default_datastore()

#Get temporary directory
tempdir = './hold'
os.makedirs(tempdir, exist_ok=True)

#Download files to tempory directory
ds.download(tempdir, prefix=sql_path_param)

#Get files in flat structure
files = []
for dirpath, dirnames, filenames in os.walk(tempdir):
    for filename in [f for f in filenames]:
        files.append(os.path.join(dirpath, filename))

####### New 04-06-2021 #######
#sql data can be loaded into a dataframe and preprocessed using the steps shown here
csv_file = [x for x in files if x.endswith('.csv')][0]

sql_df = pd.read_csv(csv_file)
sql_df = sql_df[(sql_df['YEAR'] >= min_year) & (sql_df['YEAR'] <= max_year)]

#Make directory on mounted storage
os.makedirs(sql_dataset, exist_ok=True)

#Upload modified dataframe
sql_df.to_csv(os.path.join(sql_dataset, 'processed_sql_data.csv'), index=False)

#Upload files and remove local copy
# for file in files:
#     basename = os.path.basename(file)
#     dest = shutil.copy(file, os.path.join(sql_dataset, basename))
#     os.remove(file)