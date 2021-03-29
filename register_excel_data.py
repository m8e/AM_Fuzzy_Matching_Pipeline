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
parser.add_argument('--excel_path_param', type=str, required=True)
parser.add_argument("--excel_dataset", dest='excel_dataset', required=True)
args, _ = parser.parse_known_args()
excel_path_param = args.excel_path_param
excel_dataset = args.excel_dataset

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
ds.download(tempdir, prefix=excel_path_param)

#Get files in flat structure
files = []
for dirpath, dirnames, filenames in os.walk(tempdir):
    for filename in [f for f in filenames]:
        files.append(os.path.join(dirpath, filename))
        
#Get excel file
excel_file = [x for x in files if '.xls' in x][0]
xl = pd.ExcelFile(excel_file, engine='openpyxl')
sheets = [x for x in xl.sheet_names if x!='YearRange']

src_files = []

#Iterate over all sheets and save local copy (store path in src_files)
for sheet in sheets:
    df = pd.read_excel(excel_file, sheet_name=sheet, engine='openpyxl')
    df.to_csv(os.path.join(tempdir, '{}.csv'.format(sheet)), index=False)
    src_files.append(os.path.join(tempdir, '{}.csv'.format(sheet)))
        
#Make directory on mounted storage
os.makedirs(excel_dataset, exist_ok=True)

#Upload files and remove local copy
for file in src_files:
    basename = os.path.basename(file)
    dest = shutil.copy(file, os.path.join(excel_dataset, basename))
    os.remove(file)