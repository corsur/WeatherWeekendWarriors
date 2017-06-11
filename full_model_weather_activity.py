################################################################################
##################################### DATA #####################################
################################################################################

# Get training data
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
import csv

my_apikey = 'f43934a981fc48f5926e5929d3ee0760'

from geopy.geocoders import Nominatim # module to convert an address into latitude and longitude values

def forecast_vector(r):
	'''
	url = "http://api.weather.com/v1/geocode/" + str(lat) + "/" + str(lon)+ \
		"/observations/historical.json?apiKey=" + my_apikey + \
		"&units=" + units + "&language=en-US" + \
		"&startDate="+str(startDate) + \
		"&endDate="+str(endDate)
	'''

	temperature = (r["day"]["temp"]+30)//5
	relative_humidity = r["day"]["rh"]//10

	precipitation = r["day"]["pop"]
	if precipitation >= .25:
		precipitation = 50
	else:
		precipitation = 0

	precipitation = precipitation//10

	snow = r["snow_range"]
	if not snow or snow < 1:
		snow = 0
	else:
		snow = 1

	weather_vector = [temperature, relative_humidity, precipitation, snow]

	#print(json.dumps(r, indent=2))

	#for item in weather_vector:
	#	print item

	return weather_vector

input_file = open('C:\Users\corsur\Documents\sdk_machine_learning\code\SampleTrainingData.csv', 'r')
csv_reader = csv.reader(input_file, delimiter=',', quotechar='"')

activities = ["hunting", "paragliding", "chess", "camping", "hiking", "biking", "boating", "fishing"]

list_of_questions = []

for row in csv_reader:
	list_of_questions += [row]

#print list_of_questions[1]

list_of_questions = list_of_questions[1:]
list_of_vectors = []
temp_vector = []
temp_weather_vector = []
temp_activity = 0
temp_list = []

for question in list_of_questions:
	#json_string = temp_vector[1]
	#json_vector = json.loads(json_string)#format into json temp_vector[1]
	json_dictionary = eval(question[1])
	temp_weather_vector = forecast_vector(json_dictionary)
	temp_activity = int(activities.index(question[-1]))
	list_of_vectors += [[temp_weather_vector] + [[temp_activity]]]

'''
for vector in list_of_vectors:
	print vector
'''

################################################################################
#################################### MODEL #####################################
################################################################################

training_data = list_of_vectors

'''
from csv_to_array import loadData
training_data = loadData(filename)
'''
x_names = ["temperature","humididty","precipitation","snow"]
y_names = activities

x_train = []
y_train = []
for observations in training_data:
    x_train += [observations[0]]
    y_train += observations[1]

# Make model
from sklearn import tree

clf = tree.DecisionTreeClassifier()
clf = clf.fit(x_train, y_train)

# Get testing data
#x_test = []

# Predict y from x
#clf.predict(x_test)

# Save model
with open("weather.dot", 'w') as f:
    f = tree.export_graphviz(clf, out_file=f)

#import pickle
#s = pickle.dumps(clf)
#clf2 = pickle.loads(s)

# Visualize result
from sklearn.externals.six import StringIO
import pydotplus
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
%matplotlib inline

def visualize_plot(decisiontree, X,rowval, filename):
    dot_data = StringIO()
    out=tree.export_graphviz(clf,feature_names=X, out_file=dot_data,class_names=rowval,
                         filled=True, rounded=True, node_ids=True,proportion=True,
                         special_characters=True,impurity=False,label="all",leaves_parallel=False)
    graph = pydotplus.graph_from_dot_data(dot_data.getvalue())
    graph.write_png(filename)
    img = mpimg.imread(filename)
    fig=plt.figure(figsize=(55,25), dpi= 50, facecolor='w', edgecolor='k')
    #plt.figure(figsize=(55, 25))
    plt.imshow(img)

visualize_plot(clf, x_names, y_names, "decisiontree.png")
