import csv
from pathlib import Path
import subprocess
import pyfiglet
import pymysql

def grab_csv() -> str:
    # Get location of this script
    script_dir = Path(__file__).resolve().parent

    # Create path to default "csv" directory 
    csv_file_path = str(Path(script_dir) / "csv")

    csv_files = subprocess.run(["ls", csv_file_path], capture_output=True, text=True)

    # Seperate all csv files into a list
    csv_list = str(csv_files.stdout).split()

    # Assign index position variables with file {1: 'csv1', 2: 'csv2'}
    csv_dict = {}
    for i, c in enumerate(csv_list):
        if c:
            csv_dict.update({i: c})
    max_index = len(csv_dict) - 1
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
            user_answer = int(input(f"Select a CSV file 0-{max_index}: "))
            if user_answer <= max_index and user_answer >= 0:
                break
        csv_path = f"{csv_file_path}/{csv_dict.get(user_answer)}"
        # Warn user if the selected file does not have a .csv file extention
        if not ".csv" in csv_path:
            print(f"[Warning] The selected file '{csv_dict.get(user_answer)}' does not have a .csv file extention. This script may not work as intended.")
        return csv_path
    except KeyboardInterrupt:
        print("\nExiting script..")

def setup_mysql_table():
    pass

csv_file = grab_csv()

with open(csv_file, 'r') as csv:
    csvdata = csv.readlines()
    # Get rid of the \n in every list object
    clean_csv_data = [ x.strip("\n") for x in csvdata ]
    if clean_csv_data:
        print(clean_csv_data)
    # TODO: now iterate from the clean_csv_data list and sync to SQL db
