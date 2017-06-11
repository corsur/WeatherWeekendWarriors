from historical_weather_vector import get_weather_vector

from random import randint

list_of_vectors = []

for day in range (1,2):
	for month in range(1,13):
		print day, month
		if month < 10:
			list_of_vectors += [[get_weather_vector("1644 Platte St, Denver, CO", "2016" + "0" + str(month) + "0" + str(day))] + [[randint(0,7)]]]
		else:
			list_of_vectors += [[get_weather_vector("1644 Platte St, Denver, CO", "2016" + str(month) + "0" + str(day))] + [[randint(0,7)]]]
		

for vector in list_of_vectors:
	print vector
