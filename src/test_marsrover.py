'''
Test cases for get_mars_pictures.py
'''
import os

import json
import pytest

API_KEY = "PuJoKjFhKV2yPfF8lSUmghJF6TUzgNIFC4zgaxCI"
LOG_FILE = "log.txt"
PYTHON_LOCATION = "/usr/bin/python3"

def create_config(put_location, location, put_key, key):
    '''Create configuration file containing download location and API key'''
    config_json = {}
    if put_location:
        config_json["DOWNLOAD_LOCATION"] = location
    if put_key:
        config_json["API_KEY"] = key

    with open("config.json", "w") as file:
        file.write(json.dumps(config_json, indent=4))

def create_date_file(filename, dates):
    with open(filename, "w") as file:
        for date in dates:
            file.write(date + "\n")

def remove_log_file():
    '''Remove existing log file'''
    remove_file(LOG_FILE)

def remove_file(filename):
    '''Remove file created by test code'''
    if os.path.exists(filename):
        os.remove(filename)
        print("Removed " + filename)

def check_if_log_exists(string_to_search):
    '''Check if log exists in log file'''
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE) as logs:
            if string_to_search in logs.read():
                return True
    return False

def test_001_normalscenario():
    remove_log_file()

    #Create input files
    create_config(True, "pictures", True, API_KEY)
    dates = ["02/27/17",
             "June 2, 2018",
             "Jul-13-2016",
             "April 30, 2018"]
    create_date_file("dates_001.txt", dates)

    #Execute command
    command = PYTHON_LOCATION + " get_mars_pictures.py dates_001.txt"
    os.system(command)

    #Test assertions
    assert check_if_log_exists("[START]")
    assert check_if_log_exists("[END]")

    #Post-processing
    remove_file("dates_001.txt")

def test_002_error_nodatefile():
    remove_log_file()

    #Create input files
    create_config(True, "pictures", True, API_KEY)

    #Execute command
    command = PYTHON_LOCATION + " get_mars_pictures.py"
    os.system(command)

    #Test assertions
    assert check_if_log_exists("[START]")
    assert check_if_log_exists("DATES TEXT FILE should be provided.")

def test_003_error_datefiledoesnotexist():
    remove_log_file()

    #Create input files
    create_config(True, "pictures", True, API_KEY)

    #Execute command
    command = PYTHON_LOCATION + " get_mars_pictures.py invaliddate.txt"
    os.system(command)

    #Test assertions
    assert check_if_log_exists("[START]")
    assert check_if_log_exists("invaliddate.txt does not exist.")

def test_004_error_invaliddates():
    remove_log_file()

    #Create input files
    create_config(True, "pictures", True, API_KEY)
    dates = ["02/27/17 #INVALID LINE",
             "June 2, 2018    06/03/18",
             "July/13/2016",
             "April 32, 2018"]
    create_date_file("dates_004.txt", dates)

    #Execute command
    command = PYTHON_LOCATION + " get_mars_pictures.py dates_004.txt"
    os.system(command)

    #Test assertions
    assert check_if_log_exists("[START]")
    assert check_if_log_exists("Invalid date: 02/27/17 #INVALID LINE")
    assert check_if_log_exists("Invalid date: June 2, 2018    06/03/18")
    assert check_if_log_exists("Invalid date: July/13/2016")
    assert check_if_log_exists("Invalid date: April 32, 2018")
    assert check_if_log_exists("No valid dates. Terminating application")

    #Post-processing
    remove_file("dates_004.txt")

def test_005_error_configfilenotfound():
    remove_log_file()
    remove_file("config.json")

    #Create input files
    dates = ["02/27/17",
             "June 2, 2018",
             "Jul-13-2016",
             "April 30, 2018"]
    create_date_file("dates_005.txt", dates)

    #Execute command
    command = PYTHON_LOCATION + " get_mars_pictures.py dates_005.txt"
    os.system(command)

    #Test assertions
    assert check_if_log_exists("[START]")
    assert check_if_log_exists("Configuration file not found.")

    #Post-processing
    remove_file("dates_005.txt")

def test_006_error_invalidconfigfile():
    remove_log_file()

    #Create input files
    with open("config.json", "w") as file:
        file.write("Invalid json file")

    dates = ["02/27/17",
             "June 2, 2018",
             "Jul-13-2016",
             "April 30, 2018"]
    create_date_file("dates_006.txt", dates)

    #Execute command
    command = PYTHON_LOCATION + " get_mars_pictures.py dates_006.txt"
    os.system(command)

    #Test assertions
    assert check_if_log_exists("[START]")
    assert check_if_log_exists("Invalid config.json file")

    #Post-processing
    remove_file("dates_006.txt")

def test_007_error_notdefineddownloadlocation():
    remove_log_file()

    #Create input files
    create_config(False, "", True, API_KEY)
    dates = ["04/27/17"]
    create_date_file("dates_007.txt", dates)

    #Execute command
    command = PYTHON_LOCATION + " get_mars_pictures.py dates_007.txt"
    os.system(command)

    #Test assertions
    assert check_if_log_exists("[START]")
    assert check_if_log_exists("Using current folder location as download location.")

    #Post-processing
    remove_file("dates_007.txt")

def test_008_error_downloadlocationdoesnotexist():
    remove_log_file()

    #Create input files
    create_config(True, "pictures/newfolder", True, API_KEY)
    dates = ["02/27/17",
             "June 2, 2018",
             "Jul-13-2016",
             "April 30, 2018"]
    create_date_file("dates_008.txt", dates)

    #Execute command
    command = PYTHON_LOCATION + " get_mars_pictures.py dates_008.txt"
    os.system(command)

    #Test assertions
    assert check_if_log_exists("[START]")
    assert not check_if_log_exists("Using current folder location as download location.")
    assert check_if_log_exists("[END]")

    #Post-processing
    remove_file("dates_008.txt")

def test_009_error_notdefinedapikey():
    remove_log_file()

    #Create input files
    create_config(True, "pictures", False, "")
    dates = ["02/27/17",
             "June 2, 2018",
             "Jul-13-2016",
             "April 30, 2018"]
    create_date_file("dates_009.txt", dates)

    #Execute command
    command = PYTHON_LOCATION + " get_mars_pictures.py dates_009.txt"
    os.system(command)

    #Test assertions
    assert check_if_log_exists("[START]")
    assert check_if_log_exists("API_KEY should be set.")

    #Post-processing
    remove_file("dates_009.txt")

def test_010_error_blankapikey():
    remove_log_file()

    #Create input files
    create_config(True, "pictures", True, "")
    dates = ["02/27/17",
             "June 2, 2018",
             "Jul-13-2016",
             "April 30, 2018"]
    create_date_file("dates_010.txt", dates)

    #Execute command
    command = PYTHON_LOCATION + " get_mars_pictures.py dates_010.txt"
    os.system(command)

    #Test assertions
    assert check_if_log_exists("[START]")
    assert check_if_log_exists("API Key should be defined. Terminating application.")

    #Post-processing
    remove_file("dates_010.txt")

def test_011_error_invalidapikey():
    remove_log_file()

    #Create input files
    create_config(True, "pictures", True, "INVALID_API_KEY")
    dates = ["02/27/17"]
    create_date_file("dates_011.txt", dates)

    #Execute command
    command = PYTHON_LOCATION + " get_mars_pictures.py dates_011.txt"
    os.system(command)

    #Test assertions
    assert check_if_log_exists("[START]")
    assert check_if_log_exists("Error occurred when getting response.")

    #Post-processing
    remove_file("dates_011.txt")
