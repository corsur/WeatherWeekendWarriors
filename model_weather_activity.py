# Get training data
x_names = ["temperature","humididty","precipitation","snow"]
y_names = ["hunting", "paragliding", "skiing", "camping", "hiking", "biking", "boating", "fishing"]
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

# Save model
with open("weather.dot", 'w') as f:
    f = tree.export_graphviz(clf, out_file=f)

#import pickle
#s = pickle.dumps(clf)
#clf2 = pickle.loads(s)
