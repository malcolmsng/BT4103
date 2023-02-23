# Hello World
# all functions to be executed here
# trying stuff out
import os
import json
import shutil
import sys
import pandas as pd
import PySimpleGUI as sg


def add_row_window():


    layout = [[sg.T("Placeholder")]]
    window = sg.Window("Settings Window", layout,
                       modal=True, use_custom_titlebar=True)
    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            break
    
    window.close()




def excel_to_csv_window():
    return


def main_window():
    # GUI Definition
    layout = [
        # [sg.T("Input :", s=15, justification="r"), sg.I(
        #     key="-IN-"), sg.FileBrowse(file_types=(("Excel Files", "*.xls*"),))],
        # [sg.T("Output Folder:", s=15, justification="r"),
        #  sg.I(key="-OUT-"), sg.FolderBrowse()],
        [sg.B("Settings", s=16), sg.B("Add Rows To Excel", s=16), sg.B("Excel Sheet To CSV", s=16)], ]
    # window_title = settings["GUI"]["title"]
    window = sg.Window("Temp title", layout)
    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            break
        if event == "Add Rows To Excel":
            add_row_window()
        if event == "Excel To CSV":
            sg.popup_error("Not yet implemented")

    window.close()


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
    read_file.to_csv(csv_source, index=None, header=True)


if __name__ == '__main__':
    cwd = os.getcwd()
    # path = os.path.join(cwd, "data")
    # data = os.listdir(path)
    # excel_data = list(filter(lambda f: f.endswith('.xlsx'), data))
    # csv_data = list(filter(lambda f: f.endswith('.csv'), data))
    # convert gui data from excel to csv
    # print(excel_data)
    # excel_to_csv(excel_data[0])
    # args = sys.argv[1:]
    # python process_csv.py <arguments>
    # argument should be the path to the csv,
    # process_csv(csv_data[0])

    main_window()


# add row window
# add rows to csv window
# select column window
