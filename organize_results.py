import pandas as pd
import os
import datetime
import argparse

# Parse input arguments
parser = argparse.ArgumentParser("parallel run step results directory")
parser.add_argument("--processed_dataset_tabular", dest='processed_dataset_tabular', required=True)
parser.add_argument("--processed_dataset_file", dest='processed_dataset_file', required=True)
parser.add_argument("--processed_dataset", type=str, required=True)

args, _ = parser.parse_known_args()

#Get output data from previous step - saved as parallel_run_step.txt
pipeline_data_file = os.path.join(args.processed_dataset, 'parallel_run_step.txt')

#Parse as dataframe and assign headers
df_pipeline_data = pd.read_csv(pipeline_data_file, header=None, delimiter=" ")
df_pipeline_data.columns = ['D', 'E', 'F', 'G', 'A', 'B', 'C', 'Year']

#Note: additional DF formatting operations can be done here

#Create output directories for CSV/Excel files
os.makedirs(args.processed_dataset_tabular, exist_ok=True)
os.makedirs(args.processed_dataset_file, exist_ok=True)

#Save output files to blob storage
df_pipeline_data.to_csv(os.path.join(args.processed_dataset_tabular, 'processed_data.csv'), index=False)
df_pipeline_data.to_excel(os.path.join(args.processed_dataset_file, 'processed_data.xlsx'), index=False)