import numpy as np

def loadData(filename):
	content = [];
	#Load Data into list	
	with open(filename) as f:
		content = f.readlines()
	content = [x.strip() for x in content] 

	num_columns = len(content[1].split(","));
	num_rows = len(content);

	x_data = np.zeros(shape=(num_rows, num_columns-1));
	y_data = np.zeros(shape=(num_rows, 1));


	#Load Data into numpy array	
	for i in range(0, len(content)):
		line = content[i].split(",");
		activity = line[num_columns-1]; #assuming end column is key
		for j in range(0, num_columns-1):
			x_val = line[j];
			x_data[i,j] = x_val;

	return [x_data, y_data];