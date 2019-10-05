'''
Requests NASA API to get Mars Rover photos on provided date
'''
import os
import json

import requests

MARS_API = "https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos"
STRING_EARTH_DATE = "earth_date"
STRING_API_KEY = "api_key"
STRING_PHOTOS = "photos"
STRING_IMGSRC = "img_src"
RESPONSE_OK = 200

class MarsRoverPhotos:
    '''Container for getting images from NASA open API: Mars Rover at the selected date'''
    def __init__(self, date, download_location, api_key, logger):
        self.date = date
        self.download_location = download_location
        self.api_key = api_key
        self.logger = logger

        self.create_date_directory()

    def create_date_directory(self):
        '''Creating directory at <DOWNLOAD_LOCATION>/<DATE> '''
        self.download_location = os.path.join(self.download_location, self.date)
        self.logger.log_info("Creating directory at " + self.download_location)
        os.makedirs(self.download_location, exist_ok=True)

    def get_json_data(self):
        '''
        Retrieve JSON data returned by NASA API:
        https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos?earth_date=<DATE>&api_key=<API_KEY>
        '''
        params = {STRING_EARTH_DATE: self.date, STRING_API_KEY: self.api_key}

        self.logger.log_info("Accessing the following API: ")
        self.logger.log_info("  URL: " + MARS_API)
        self.logger.log_info("  at date: " + self.date)
        self.logger.log_info("  using API key: " + self.api_key)

        try:
            response = requests.get(MARS_API, params=params)
        except requests.exceptions.ConnectionError:
            self.logger.log_err("Error occurred when connecting to NASA API: " + MARS_API)
            return []

        json_response = json.loads(response.text)

        if STRING_PHOTOS not in json_response:
            self.logger.log_err("Error occurred when getting response.")
            self.logger.log_err(json_response)
            return []
        return json_response[STRING_PHOTOS]

    def get_images(self):
        '''Retrieve images from the URLs in the retrieved JSON data (from get_json_data())    '''
        self.logger.log_info("Getting images on date: " + self.date)
        photos_uri = self.get_json_data()
        for photo_uri in photos_uri:
            photo_src = photo_uri[STRING_IMGSRC]

            #Get filename
            filename = photo_src
            if filename.find('/'):
                filename = filename.rsplit('/', 1)[1]

            self.logger.log_info("  Retrieving image " + filename)
            filename = os.path.join(self.download_location, filename)

            #If image does not yet exist in local directory, retrieve from the URL
            if not os.path.exists(filename):
                try:
                    photo_response = requests.get(photo_src, stream=True)
                except requests.exceptions.ConnectionError:
                    self.logger.log_err("Error occurred when connecting to URL: " + photo_src)
                    continue

                if photo_response.status_code == RESPONSE_OK:
                    with open(filename, 'wb') as file:
                        for chunk in photo_response:
                            file.write(chunk)
