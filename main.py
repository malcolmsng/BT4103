# Hello World
# all functions to be executed here
# trying stuff out
import os
import json
import shutil
import sys
import pandas as pd
import PySimpleGUI as sg


def settings_window(settings):
    layout = [[sg.T("SETTINGS")],
              [sg.T("Font Size:"), sg.I(settings["GUI"]
                                        ["font_size"], s=20, key="-FONT_SIZE-")],
              [sg.T("Font Family:"), sg.I(settings["GUI"]
                                          ["font_family"], s=20, key="-FONT_FAMILY-")],
              [sg.T("Theme:"), sg.I(settings["GUI"]
                                    ["theme"], s=20, key="-THEME-")],
              [sg.T("Sheet Name:"), sg.I(settings["EXCEL"]
                                         ["sheet_name"], s=20, key="-SHEET_NAME-")],
              [sg.B("Save Current Settings", s=20)]]
    window = sg.Window("Settings Window", layout,
                       modal=True, use_custom_titlebar=True)
    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            break
        if event == "Save Current Settings":
            # Write to ini file
            settings["EXCEL"]["sheet_name"] = values["-SHEET_NAME-"]
            settings["GUI"]["font_size"] = values["-FONT_SIZE-"]
            settings["GUI"]["font_family"] = values["-FONT_FAMILY-"]
            settings["GUI"]["theme"] = values["-THEME-"]

            # Display success message & close window
            sg.popup_no_titlebar("Settings saved!")
            break
    window.close()


def add_row_window():

    layout = [[sg.T("Placeholder")], [[sg.T("Input :", s=15, justification="r"), sg.I(
        key="-IN-"), sg.FileBrowse(file_types=(("Excel Files", "*.xls*"),))], ]]
    window = sg.Window("Add Row to Excel", layout,
                       modal=True, use_custom_titlebar=True)
    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            break

    window.close()


def excel_to_csv_window():
    layout = [[sg.T("Placeholder")],
              [sg.T("Input :", s=15, justification="r"), sg.I(
                  key="-IN-"), sg.FileBrowse(file_types=(("Excel Files", "*.xls*"),)), ],
              [sg.T("Output Folder:", s=15, justification="r"),
               sg.I(key="-OUT-"), sg.FolderBrowse()],
              [sg.T("Rows To Add :", s=15, justification="r"), sg.I(default_text="XX:YY",
                                                                    key="-ROWS-", s=8),
              sg.B("Add Rows", s=16), ]]
    window = sg.Window("Add Row to Excel", layout,
                       modal=True, use_custom_titlebar=True)
    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            break

    window.close()


def main_window():
    # GUI Definition
    layout = [
        [
            sg.B("Settings", s=16),
            sg.B("Add Rows To Excel", s=16),
            sg.B("Excel To CSV", s=16),
            sg.B("Analyse Data", s=16),
        ],

    ]
    # window_title = settings["GUI"]["title"]
    window = sg.Window("Temp title", layout)
    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            break
        if event == "Settings":
            settings_window(settings)
        if event == "Add Rows To Excel":
            add_row_window()
        if event == "Excel To CSV":
            excel_to_csv_window()

    window.close()


def process_csv(csv_data):
    # process csv data
    df_source = f"./data/{csv_data}"
    sample_data = pd.read_csv(df_source, skiprows=1)
    df = pd.DataFrame(sample_data)
    # print(df.head())
    return
# convert xlsx to csv format

# add excel rows/ sheet to csv data file


def excel_to_csv(excel_data):
    xlsx_source = f"./data/{excel_data}"
    csv_source = xlsx_source.replace(".xlsx", ".csv")
    read_file = pd.read_excel(xlsx_source)
    read_file.to_csv(csv_source, index=None, header=True)


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
