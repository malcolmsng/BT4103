# Hello World
# all functions to be executed here
# trying stuff out
import os
import json
import shutil
import sys
import pandas as pd


def process_csv(csv_data):
    # process csv data
    df_source = f"./data/{csv_data}"
    sample_data = pd.read_csv(df_source, skiprows=1)
    df = pd.DataFrame(sample_data)
    # print(df.head())
    return
# convert xlsx to csv format
def excel_to_csv(excel_data):
    xlsx_source = f"./data/{excel_data}"
    csv_source = xlsx_source.replace(".xlsx", ".csv")
    read_file = pd.read_excel(xlsx_source)
    read_file.to_csv(csv_source,index=None, header=True)
    


if __name__ == '__main__':
    cwd = os.getcwd()
    path = os.path.join(cwd, "data")
    data = os.listdir(path)
    excel_data = list(filter(lambda f: f.endswith('.xlsx'), data))
    csv_data = list(filter(lambda f: f.endswith('.csv'), data))
    # convert gui data from excel to csv
    print(excel_data)
    excel_to_csv(excel_data[0])
    # args = sys.argv[1:]
    # python process_csv.py <arguments>
    # argument should be the path to the csv,
    process_csv(csv_data[0])
