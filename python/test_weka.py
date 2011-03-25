import sys

# TODO before using :
#export CLASSPATH=$CLASSPATH/usr/share/java/weka.jar


import java.io.FileReader as FileReader
import weka.core.Instances as Instances
import weka.classifiers.trees.J48 as J48

# load data file
file = FileReader("./div_8.arff")
data = Instances(file)
data.setClassIndex(data.numAttributes() - 1)

# create the model
j48 = J48()
j48.buildClassifier(data)

# print out the built model
print j48
