# Get training data
from csv_to_array import loadData
training_data = loadData(filename)

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
