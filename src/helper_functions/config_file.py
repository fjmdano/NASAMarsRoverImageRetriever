'''
Reads config.json to get DOWNLOAD LOCATION and API KEY
'''
import json
import os

KEY_DOWNLOAD_LOCATION = "DOWNLOAD_LOCATION"
KEY_API_KEY = "API_KEY"

class ConfigFile:
    '''Container for the configuration file'''
    def __init__(self, file_name, logger):
        self.file_name = file_name
        self.has_error = False
        self.download_location = ""
        self.api_key = ""
        self.logger = logger

    def read_file(self):
        '''
        Reads configuration file and retrieves relevant values
             i.e. DOWNLOAD_LOCATION and API_KEY
        '''
        config_data = {}
        try:
            with open(self.file_name) as config_file:
                config_data = json.load(config_file)
        except FileNotFoundError:
            self.logger.log_err("Configuration file not found.")
            self.has_error = True
            return
        except json.decoder.JSONDecodeError:
            self.logger.log_err("Invalid config.json file.")
            self.has_error = True
            return


        #Get DOWNLOAD_LOCATION from configuration file
        try:
            self.download_location = config_data[KEY_DOWNLOAD_LOCATION]
        except KeyError:
            self.logger.log_warn("Using current folder location as download location.")

        #Get API_KEY from configuration file
        try:
            self.api_key = config_data[KEY_API_KEY]
        except KeyError:
            self.logger.log_err("API_KEY should be set.")
            self.has_error = True

        return

    def create_download_location(self):
        '''Creates directory at DOWNLOAD_LOCATION'''
        os.makedirs(self.download_location, exist_ok=True)

    def check_error(self):
        '''Checks if error occurred when reading configuration file'''
        if self.has_error is True:
            self.logger.log_err("Error occurred. Terminating application.")
        if len(self.api_key) == 0:
            self.logger.log_err("API Key should be defined. Terminating application.")
            self.has_error = True
        return self.has_error

    def get_download_location(self):
        '''Getter function for the DOWNLOAD LOCATION'''
        return self.download_location

    def get_api_key(self):
        '''Getter function for the API KEY'''
        return self.api_key
