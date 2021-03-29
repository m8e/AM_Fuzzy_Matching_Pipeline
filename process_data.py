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
parser = argparse.ArgumentParser("Process Data")
args, _ = parser.parse_known_args()

#Get current run
current_run = None

#Get associated AML workspace
ws = None

#Get sql data
sql_dataset = None
sql_df = None

#init() operation is run once at the start of execution
def init():
    global current_run, ws, sql_dataset, sql_df
    #Get current run and workspace
    current_run = Run.get_context()
    ws = current_run.experiment.workspace

    sql_dataset = current_run.input_datasets['sql_data']
    sql_df = sql_dataset.to_pandas_dataframe()
    
def run(input_data):
    # 1.0 Set up output directory and the results list
    result_list = []
    
    #Iterate over all files in FileDataset
    for idx, csv_file_path in enumerate(input_data):
        file_name = os.path.basename(csv_file_path)[:-4]
        data = pd.read_csv(csv_file_path)
        
        #REPLACE THIS LOGIC WITH CUSTOM CODE
        merged_df = pd.concat([data, sql_df], axis=1)
        merged_df = merged_df.dropna()

        #Add all output rows to result_list
        for _, row in merged_df.iterrows():
            result_list.append((row))
        
    #Return all rows formatted as a Pandas dataframe
    return pd.DataFrame(result_list)
        
        