import json
import csv
import pandas as pd
import datetime
from datetime import timedelta, date
import time
import requests
import shutil
import os
import sys
import requests
from math import floor

my_apikey = 'f43934a981fc48f5926e5929d3ee0760'

from geopy.geocoders import Nominatim # module to convert an address into latitude and longitude values


def get_weather_vector(address, date):
	#address = "1644 Platte St, Denver, CO"
	#address = sys.argv[1]

	geolocator = Nominatim()
	location = geolocator.geocode(address)
	latitude, longitude = location.latitude, location.longitude


	lat = latitude
	lon = longitude
	units = "m"

	#days_from_now = sys.argv[2]

	#startDate = "20170608"
	#startDate = sys.argv[2]
	startDate = date

	endDate = str(int(date)+1)
	#endDate = "20170609"
	#endDate = sys.argv[3]

	#url = "http://api.weather.com/v1/geocode/" + str(lat) + "/" + str(lon) + "/forecast/daily/10day.json?apiKey=" + my_apikey + "&units=m"

	url = "http://api.weather.com/v1/geocode/" + str(lat) + "/" + str(lon)+ \
		"/observations/historical.json?apiKey=" + my_apikey + \
		"&units=" + units + "&language=en-US" + \
		"&startDate="+str(startDate) + \
		"&endDate="+str(endDate)

	r = requests.get(url).json()

	r_copy = requests.get(url).json()["observations"]#[int(floor(len(requests.get(url).json()["observations"])/2))]

	'''
	temperature = r_copy["temp"]
	max_temperature = r_copy["max_temp"]
	min_temperature = r_copy["min_temp"]
	relative_humidity = r_copy["rh"]
	'''

	acc_temp = 0
	acc_rh = 0
	acc_snow = 0
	acc_prec = 0
	for observation in r_copy:
		acc_temp += observation["temp"]
		acc_rh += observation["rh"]
		acc_snow += 0 if not observation["snow_hrly"] else observation["snow_hrly"]
		acc_prec += 0 if not observation["precip_total"] else observation["precip_total"]

	temperature = acc_temp/len(r_copy)
	relative_humidity = acc_rh/len(r_copy)
	precipitation = acc_prec/len(r_copy)

	#snow must be binary for fit with forecast
	snow = acc_snow
	if snow >= 1:
		snow = 1
	else:
		snow = 0

	'''
	precipitation goes from 0 to 9
	relative humidity goes from 0 to 9
	snow is binary
	temperature goes from 0 to 12
	'''

	weather_vector = [(temperature+30)//5, relative_humidity//10, precipitation//10, snow]

	#print(json.dumps(r, indent=2))

	return weather_vector
