# Hello World
# all functions to be executed here
# trying stuff out
import os
# import json
# import shutil
# import sys
import pandas as pd
import PySimpleGUI as sg
# import textwrap
from pathlib import Path


def is_valid_path(filepath):
    if filepath and Path(filepath).exists():
        return True
    sg.popup_error("Filepath not correct")
    return False


def settings_window(settings):
    layout = [[sg.T("SETTINGS")],
              [sg.T("Font Size:"), sg.I(settings["GUI"]
                                        ["font_size"], s=20, key="-FONT_SIZE-")],
              [sg.T("Font Family:"), sg.I(settings["GUI"]
                                          ["font_family"], s=20, key="-FONT_FAMILY-")],
              [sg.T("Theme:"), sg.I(settings["GUI"]
                                    ["theme"], s=20, key="-THEME-")],
              #   [sg.T("Sheet Name:"), sg.I(settings["EXCEL"]
              #                              ["sheet_name"], s=20, key="-SHEET_NAME-")],
              [sg.B("Save Current Settings", s=20)]]
    window = sg.Window("Settings Window", layout,
                       modal=True, use_custom_titlebar=True)
    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            break
        if event == "Save Current Settings":
            # Write to ini file
            # settings["EXCEL"]["sheet_name"] = values["-SHEET_NAME-"]
            settings["GUI"]["font_size"] = values["-FONT_SIZE-"]
            settings["GUI"]["font_family"] = values["-FONT_FAMILY-"]
            settings["GUI"]["theme"] = values["-THEME-"]

            # Display success message & close window
            sg.popup_no_titlebar("Settings saved!")
            break
    window.close()


# def add_row_window():

#     layout = [[sg.T("Placeholder")], [[sg.T("Input :", s=15, justification="r"), sg.I(
#         key="-IN-"), sg.FileBrowse(file_types=(("Excel Files", "*.xls*"),))], ]]
#     window = sg.Window("Add Row to Excel", layout,
#                        modal=True, use_custom_titlebar=True)
#     while True:
#         event, values = window.read()
#         if event == sg.WINDOW_CLOSED:
#             break

#     window.close()

# chose excel file --> choose csv file


def gui_settings_window():
    layout = [[sg.T("Indicate which excel file and sheet to open")],
              [[sg.T("Input :", s=15, justification="r"), sg.I(
                  key="-IN-"), sg.FileBrowse(file_types=(("Excel Files", "*.xls*"),), key='file_name')]],
              [sg.T("Sheet Name:", s=15, justification='r'), sg.I(
                  settings["EXCEL"]["sheet_name"], s=20, key="-SHEET_NAME-")],
              [sg.Push(), sg.B("Open Excel Data", s=16, key='open_excel')]
              ]
    window = sg.Window("Retrieve/update row in excel", layout,
                       modal=True, use_custom_titlebar=True)
    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            break
        if event == 'open_excel':
            try:
                file = str(values["file_name"])
                sheet = str(values["-SHEET_NAME-"])
                gui_window(file, sheet)
            except ValueError:
                sg.popup_no_titlebar("Sheet name does not exist!")
                
            break

    window.close()


def gui_window(file, sheet):
    df = pd.read_excel(io=file, sheet_name=sheet, skiprows=1)
    layout = [[sg.T("Row to Edit: "), sg.T("-", key='to_edit')],
              [sg.T("Item ID :", size=(40, 1), justification="r"),
               sg.I(key="item_id")],
              [sg.T("Test Lead :", size=(40, 1), justification="r"),
               sg.I(key="input_1")],
              [sg.T("Why defect was not identified during testing? :",
                    size=(40, 1), justification="r"), sg.I(key="input_2")],
              [sg.T("Are related requirements recorded in the BR or UCS? :",
                    size=(40, 2), justification="r"), sg.I(key="input_3")],
              [sg.T("If prior response is 'Yes', list down the BR or UCS document number(s) and clause identifier(s) :", size=(
                  40, 2), justification="r"), sg.I(key="input_4")],
              [sg.T("Primary Root Cause Classification #3 :", size=(
                  40, 1), justification="r"), sg.I(key="input_5")],
              [sg.T("Remark :", size=(40, 1), justification="r"),
               sg.I(key="input_6")],
              [sg.T("Proposed solution to prevent recurrence :", size=(
                  40, 1), justification="r"), sg.I(key="input_7")],

              [sg.B("Search", key="search"), sg.Push(),
               sg.B("Update", key="Update")]

              ]
    window = sg.Window("Retrieve/update row in excel", layout, size=(1200, 500),
                       modal=True, use_custom_titlebar=True)
    idx = 0
    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            break
        if event == 'search':
            idx = df[df['Item Id'] == str(values['item_id'])].index
            if idx > 0:
                sg.popup(" Item id: {}\n Submit Date: {}\n Title: {}\n Description: {}\n Phase Found: {}\n State: {}\n Severity: {}\n Module/Device Type Text: {}\n Module/Device Varient: {}\n OIC Team Default: {}\n Software Version: {}\n Defect Owner: {}\n Associated Prj: {}\n".format(
                    df.loc[idx, 'Item Id'].values[0],
                    df.loc[idx, 'Submit Date'].values[0],
                    df.loc[idx, 'Title'].values[0],
                    df.loc[idx, 'Description'].values[0],
                    df.loc[idx, 'Phase Found'].values[0],
                    df.loc[idx, 'State'].values[0],
                    df.loc[idx, 'Severity'].values[0],
                    df.loc[idx, 'Module/Device Type Text'].values[0],
                    df.loc[idx, 'Module/Device Varient'].values[0],
                    df.loc[idx, 'OIC Team Default'].values[0],
                    df.loc[idx, 'Software Version'].values[0],
                    df.loc[idx, 'Defect Owner'].values[0],
                    df.loc[idx, 'Associated Prj'].values[0]))
                window['to_edit'].update(idx.values[0])

                window['input_1'].update(df.iloc[idx, 13].values[0])
                window['input_2'].update(df.iloc[idx, 14].values[0])
                window['input_3'].update(df.iloc[idx, 15].values[0])
                window['input_4'].update(df.iloc[idx, 16].values[0])
                window['input_5'].update(df.iloc[idx, 17].values[0])
                window['input_6'].update(df.iloc[idx, 18].values[0])
                window['input_7'].update(df.iloc[idx, 19].values[0])
            else:
                sg.popup("Not found")
        if event == 'Update':
            if idx == 0:
                sg.popup("Select row to update")
            else:
                df.iloc[idx, 13] = str(values['input_1'])
                df.iloc[idx, 14] = str(values['input_2'])
                df.iloc[idx, 15] = str(values['input_3'])
                df.iloc[idx, 16] = str(values['input_4'])
                df.iloc[idx, 17] = str(values['input_5'])
                df.iloc[idx, 18] = str(values['input_6'])
                df.iloc[idx, 19] = str(values['input_7'])
                sg.popup("Updated!")
                df.to_excel("output.xlsx", sheet_name=sheet, index=False)
    return


def excel_to_csv_window():

    layout = [
        [sg.Column([[sg.T("Add all rows from project Excel file to master CSV file")]],
                   vertical_alignment='center', justification='center',  k='-C-')],
        [sg.T("Excel File (Source) :", s=20, justification="r"), sg.I(
            key="-EXCEL-"), sg.FileBrowse(file_types=(("Excel Files", "*.xls*"),)), ],
        [sg.T("CSV File (Destination) :", s=20, justification="r"),
         sg.I(key="-CSV-"), sg.FileBrowse(file_types=(("CSV Files", "*.csv*"),))],
        [sg.T("Header Row:", s=20, justification="r"), sg.I(key="-HEADER-", s=4),
         sg.T("Indicate the header row number", s=32, font=('Helvetica', 8, 'normal')), ],
        #   [sg.T("Rows To Add :", s=15, justification="r"), sg.I(default_text="1:99",
        #                                                         key="-ROWS-", s=8),
        #    sg.T("Columns To Add :", s=15, justification="r"), sg.I(default_text="A:AZ",
        #                                                            key="-COLUMNS-", s=8),
        #   sg.B("Add Rows", s=16), ]
        [sg.Column([[sg.B("Add Rows", s=16)]],
                   vertical_alignment='center', justification='center',  k='-C-')]

    ]
    window = sg.Window("Add Rows to CSV", layout,
                       modal=True, use_custom_titlebar=True)
    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            break
        if event == "Add Rows":
            excel_to_csv(excel_path=values["-EXCEL-"],
                         csv_path=values["-CSV-"],
                         skip_rows=values["-HEADER-"]
                         )

    window.close()


def excel_to_csv(excel_path, csv_path, skip_rows):
    # xlsx_source = f"./data/{excel_data}"
    # csv_source = xlsx_source.replace(".xlsx", ".csv")

    # to skip

    read_file = pd.read_excel(
        excel_path, skiprows=range(0, int(skip_rows)))
    print(int(skip_rows))
    print(read_file)
    read_file.to_csv(csv_path, mode="a", index=None,)


def analyse_data():
    # process csv data

    layout = [
        [sg.Column([[sg.T("Analyse selected columns")]],
                   vertical_alignment='center', justification='center',  k='-C-')],

        [
            sg.T("Columns To Analyse :", s=18, justification="r"), sg.I(default_text="AA:AG",
                                                                        key="-COLUMNS-", s=6),
            sg.B("Start Analysis", s=12), ]
        # [sg.Column([[sg.B("Add Rows", s=16)]],
        #            vertical_alignment='center', justification='center',  k='-C-')]

    ]
    window = sg.Window("Analyse Data", layout,
                       modal=True, use_custom_titlebar=True)
    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            break
        if event == "Generate Analysis":
            # excel_to_csv(excel_path=values["-EXCEL-"],
            #              csv_path=values["-CSV-"],
            #              rows=values["-ROWS-"],
            #              columns=values["-COLUMNS-"])
            # sample_data = pd.read_csv(
            #     excel_path, skiprows=1, usecols=values["-COLUMNS-"])
            # df = pd.DataFrame(sample_data)
            break

    window.close()
    return
# convert xlsx to csv format


def main_window():
    # GUI Definition
    layout = [
        [
            sg.B("Settings", s=16),
            # sg.B("Add Rows To Excel", s=16),
            sg.B("Update Row in Excel", s=16),
            sg.B("Add Rows to CSV", s=16),
            sg.B("Analyse Data", s=16),
        ],

    ]
    # window_title = settings["GUI"]["title"]
    window = sg.Window("LTA GUI Tool", layout)
    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            break
        if event == "Settings":
            settings_window(settings)
        # if event == "Add Rows To Excel":
        #     add_row_window()
        if event == "Add Rows to CSV":
            excel_to_csv_window()
        if event == "Update Row in Excel":
            gui_settings_window()
        if event == "Analyse Data":
            analyse_data()

    window.close()


if __name__ == '__main__':
    cwd = os.getcwd()
    # cosmetics for GUI
    settings = sg.UserSettings(
        path=cwd, filename="config.ini", use_config_file=True, convert_bools_and_none=True
    )
    theme = settings["GUI"]["theme"]
    font_family = settings["GUI"]["font_family"]
    font_size = int(settings["GUI"]["font_size"])
    sg.theme(theme)
    sg.set_options(font=(font_family, font_size))
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
