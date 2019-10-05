# NASAMarsRoverImageRetriever
DevTestProject using NASA Mars Rover API
Retrieve images captured by Mars Rover on the provided date(s) Using NASA API
This application is implemented using Python 3.6.8

## Prerequisites:
	1. The following modules are used:
	    - os
	    - json
	    - logging
	    - requests
	    - webbrowser
	    - pytest-5.2.0
	2. API Key can be obtained from [NASA site](https://api.nasa.gov/)
	3. The following input files are needed:
	   - configuration file (filename: config.json) e.g.
	   	 '''
			{
			    "DOWNLOAD_LOCATION": "pictures",
			    "API_KEY": "PuJoKjFhKV2yPfF8lSUmghJF6TUzgNIFC4zgaxCI"
			}
	   	 '''
	   - dates txt file e.g.
   		'''
			02/27/17
			June 2, 2018
			Jul-13-2016
			April 30, 2018
   		'''

## Running source code:
	To run, call the following command in src/ folder:
	 $ python get_mars_pictures.py dates.txt

## Execute test cases:
	To execute unit tests, call the following in the src/ folder:
	 $ py.test test_marsrover.py

## Notes
	Bootstrap is used for HTML formatting. Copy of .css and .js files are in bootstrap/ folder
