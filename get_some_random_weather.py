#generate date/activity pair random list and assign random yes/no
from geopy.geocoders import Nominatim # module to convert an address into latitude and longitude values
import os
import json
import csv
import numpy
import pandas as pd
import requests
import shutil
import requests
from random import *
import random
import datetime
from datetime import timedelta, date
import time
from io import BytesIO
import pandas as pd

#global variables
my_apikey = 'f43934a981fc48f5926e5929d3ee0760' #designated the Cognitive Builder Faire
units = "e" #use m for metric, e for english
#myWxURL = 'GET https://<username>:<password>@twcservice.mybluemix.net:443/api/weather/v1/geocode/45.42/75.69/forecast/daily/10day.json?units=m&language=en-US'

#set location of data pull \/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/
address = "1644 Platte St, Denver, CO"
geolocator = Nominatim()
location = geolocator.geocode(address)
myLat, myLon = location.latitude, location.longitude
#lat = latitude #39.75764085 #lon = longitude #-105.0069346
#print myLat, myLong

#list of activity types for asking the user \/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/
myActivityPool = ["hunting", "paragliding", "skiing", "camping", "hiking", "biking", "boating", "fishing"]
seedDate = "1/1/16" #for training data, we're picking random weather from the year 2016

#myRand = random() #this only seems to work with "from random import *"
#myRandInt = 1
myList = [] #this will be a list of integer day and activity

#iterate and generate a full list of pseudo random weather data \/\/\/\/\/\/\/\/\/\/\/\/\/\/
for x in range(0,200):
  #get a random XY location
  myLat = float(25) + (float(randint(0,100)) / float(100)) * float(24) #usa Latitude ranges from approx 25 to 49
  myLong = float(64) + (float(randint(0,100)) / float(100)) * float(60) #usa Longitude ranges from approx 64 to 124

  #As it turns out, we can't use random date to get common language forecast data!
  #myRandInt = randint(1,365) #days of the year, excluding leap year issue
  #myDate = datetime.datetime.strptime(seedDate, "%m/%d/%y") + datetime.timedelta(days=myRandInt)

  myActivity = random.choice(myActivityPool)


  #getting 3day, 5day, 7day, 10day
  #there is no archive of the "common language" forecasts, so in lieu of that, we'll randomly select locations across the USA
  #this will generate, hopefully, some "good" and some "bad" weather, though in June we will certainly be biased towards "hotter"
  #since we're doing 10 day forecast data, we'll go ahead and pick randomly from 1-10 days out
  myDay = randint(1,8) #change this to 3 for example if you're doing the 3 day forecast, use 1-8 to prevent using day 0 which, after 3pm, won't have a "day" forecast
  myLat = 27 + (float(randint(0,100)) / 100) * 20 #usa Latitude ranges from approx 25 to 49
  myLong = 66 + (float(randint(0,100)) / 100) * 56 #usa Longitude ranges from approx 64 to 124
  url = "http://api.weather.com/v1/geocode/" + str(myLat) + "/" + str(myLon)+ \
    "/forecast/daily/10day.json?apiKey=" + my_apikey + \
    "&units=" + units
  r = requests.get(url).json()
  #print r

  #output the result
  try:
    resultRaw = r['forecasts'][myDay]
    resultDay = r['forecasts'][myDay]['day']['narrative'] #this is the raw result
    resultNight = r['forecasts'][myDay]['night']['narrative'] #this is the raw result
    #userFriendly = 'Would you go ' + myActivity + '?' + ' Today ' + resultDay + ' Tonight ' + resultNight
    userFriendly = 'What sounds best?' + ' Today ' + resultDay + ' Tonight ' + resultNight
    #print userFriendly
    resultRawJSON = (json.dumps(resultRaw, indent=2)).replace('\n', '')
    #userFriendly = str.replace(",","...")
    #myTuple = (myRandInt, myActivity, myDate.strftime('%Y%m%d'))
    myTuple = (myActivity, myLat, myLong, userFriendly, resultRawJSON)
    #myTuple = (myActivity, myLat, myLong, userFriendly[0:40]) #use the [0:x] to get just the left x number of chars, for testing
    #print userFriendly
    myList.append(myTuple)
except KeyError:
    print "error"


  #myRandIntList.append(myRandInt)

#myList
myDF = pd.DataFrame(myList)
myDF
myDF.to_csv('trainingData.csv',index=False)
put_file(myDataCreds,'trainingData.csv')

myDF
#with open('filename', 'w') as myFile:
#    myFile.write(myList)

#Miscellaneous snippets, unused \/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/
#another way to do random
#myActivity = (myActivityList[random.randint(0,len(myActivityList)-1)])
