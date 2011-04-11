import sys

# TODO before using :
#export CLASSPATH=$CLASSPATH/usr/share/java/weka.jar
#java weka.classifiers.functions.MultilayerPerceptron -l model/mlp_seuil.model -T save_arff/test_classifier_.arff -p 0

import java.io.FileReader as FileReader
import weka.core.Instances as Instances
import weka.classifiers.trees.J48 as J48
import weka.classifiers.functions.MultilayerPerceptron as MLP

# load data file
file = FileReader("./div_8.arff")
data = Instances(file)
data.setClassIndex(data.numAttributes() - 1)

# create the model
j48 = J48()
j48.buildClassifier(data)

# print out the built model
print j48
