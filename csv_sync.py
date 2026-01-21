import csv
from pathlib import Path
import subprocess
import pyfiglet
import pymysql
import json

def load_db_config() -> dict:
    if not (Path(script_dir) / "db_config.json").exists():
        print("No db_config.json detected. Exiting.")
    db_config = {}
    with open("db_config.json", "r") as f:
        data = json.load(f)
        return data

def grab_csv() -> str:
    # Create path to default "csv" directory 
    csv_file_path = str(Path(script_dir) / "csv")

    csv_files = subprocess.run(["ls", csv_file_path], capture_output=True, text=True)

    # Seperate all csv files into a list
    csv_list = str(csv_files.stdout).split()

    # Assign index position variables with file {1: 'csv1', 2: 'csv2'}
    csv_dict = {}
    for i, c in enumerate(csv_list, start=1):
        if c:
            csv_dict.update({i: c})
    max_index = len(csv_dict)
    if csv_dict:
        print(csv_dict)

    # Print Header
    ascii_art = pyfiglet.figlet_format("/csv sync/")
    print(ascii_art)
    # Show all files that were found in the csv directory
    print(" Sync csv files in realtime to a SQL database\n")
    if not csv_dict:
        print("No files found in the csv directory. Exiting..")
        exit()
    print(f"Available files:\n{csv_dict}")
    try:
        # Prompt user to choose an existing csv file
        while True:
            user_answer = int(input(f"Select a CSV file 1-{max_index}: "))
            if user_answer <= max_index and user_answer >= 0:
                break
        csv_path = f"{csv_file_path}/{csv_dict.get(user_answer)}"
        # Warn user if the selected file does not have a .csv file extention
        if not ".csv" in csv_path:
            print(f"[Warning] The selected file '{csv_dict.get(user_answer)}' does not have a .csv file extention. This script may not work as intended.")
        return csv_path
    except KeyboardInterrupt:
        print("\nExiting script..")

# Generates the table_config.json. This file is needed so the script knows the table structure 
def generate_table_config():
    table_dict = {}
    table_columns = {}
    table_name = input(f"Enter desired table name: ")
    column_number = 1
    while True:
        column_name = input(f"Enter column name for column {column_number}: ")
        table_columns[f"column_{column_number}"] = column_name
        column_number += 1
        print(table_columns)
        answer = input("Would you like to add another column? y/n or q to exit: ")
        if "q" in answer.lower():
            exit()
        if "n" in answer.lower():
            break
    # Build the config JSON
    table_dict["table_name"] = table_name
    table_dict["header"] = table_columns
    table_config = json.dumps(table_dict, indent=4)

    # Now write the JSON file
    with open("table_config.json", "w") as f:
        f.write(table_config)

def setup_mysql_table():
    # Was the table_config.json already generated?
    if not (Path(script_dir) / "table_config.json").exists():
        # table_config.json does not exist. Generate one now
        generate_table_config()
    # Create table 

# Get location of this script
script_dir = Path(__file__).resolve().parent

db_config = load_db_config()

setup_mysql_table()
csv_file = grab_csv()

with open(csv_file, 'r') as csv:
    csvdata = csv.readlines()
    # Get rid of the \n in every list object
    clean_csv_data = [ x.strip("\n") for x in csvdata ]
    if clean_csv_data:
        print(clean_csv_data)
    # TODO: now iterate from the clean_csv_data list and sync to SQL db
