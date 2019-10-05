'''
Main function for getting Mars Rover images using NASA API on the specified dates
'''

import os
import sys
from datetime import datetime

from helper_functions.config_file import ConfigFile
from helper_functions.mars_rover_photos import MarsRoverPhotos
from helper_functions.webpage_handler import create_webpage, open_webpage
from helper_functions.logger import Logger

CONFIG_FILE_NAME = "config.json"
MINIMUM_ARG_LENGTH = 2

POSSIBLE_DATE_FORMATS = ['%m/%d/%y',
                         '%B %-d, %Y',
                         '%B %d, %Y',
                         '%b-%d-%Y']

NEEDED_DATE_FORMAT = '%Y-%m-%d'

def read_dates(date_file, logger):
    '''Read the dates in date_file'''
    logger.log_info("[START] Checking dates at " + date_file)
    dates = []
    if not os.path.exists(date_file):
        logger.log_warn(date_file + " does not exist.")
        return []

    with open(date_file) as dates_list:
        for line in dates_list.readlines():
            line = line.replace("\n", "")
            tried_formats = 0
            for date_format in POSSIBLE_DATE_FORMATS:
                try:
                    datetime_obj = datetime.strptime(line, date_format)
                    break
                except ValueError:
                    tried_formats += 1
                    continue
            if tried_formats == len(POSSIBLE_DATE_FORMATS):
                #date was not properly formatted. Line must be invalid therefore ignored
                logger.log_warn("Invalid date: " + line)
            else:
                dates.append(datetime_obj.strftime(NEEDED_DATE_FORMAT))
    logger.log_info("[END] Valid dates retrieved: " + str(dates))
    return dates

def main(args):
    '''Main function of get_mars_pictures'''

    #Create Logger
    logger = Logger("log.txt")

    logger.log_info("[START]")
    if len(args) < MINIMUM_ARG_LENGTH:
        logger.log_err("DATES TEXT FILE should be provided.")
        logger.log_err("How to use:")
        logger.log_err("  $ python get_mars_pictures.py <DATES TEXT FILE>")
        return

    #Check configuration file
    config = ConfigFile(CONFIG_FILE_NAME, logger)
    config.read_file()
    config.create_download_location()
    if config.check_error() is True:
        logger.log_err("Error occurred when reading configuration file. Terminating application.")
        return

    #Get dates from dates.txt
    dates_to_check = read_dates(args[1], logger)

    if len(dates_to_check) == 0:
        logger.log_warn("No valid dates. Terminating application")
        return
    #Get photos on the specified dates

    for date in dates_to_check:
        mars = MarsRoverPhotos(date, config.get_download_location(),
                               config.get_api_key(), logger)
        mars.get_images()

    logger.log_info("Opening retrieved images in browser")
    create_webpage(config.get_download_location(), dates_to_check)
    open_webpage()

    logger.log_info("[END]")
    return

if __name__ == '__main__':
    main(sys.argv)
