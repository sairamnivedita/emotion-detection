#!/usr/bin/python
from pyfann import libfann
import copy

connection_rate = 1
learning_rate = 0.3
num_input = 72
num_neurons_hidden = 80
num_output = 1

desired_error = 0.0
max_iterations = 10000
iterations_between_reports = 10

#creation du neural network
ann = libfann.neural_net()
ann.create_sparse_array(connection_rate, (num_input, num_neurons_hidden, num_output))
ann.set_learning_rate(learning_rate)
ann.set_activation_function_output(libfann.SIGMOID_SYMMETRIC_STEPWISE)
ann.set_bit_fail_limit(0.8)
print ann.get_num_layers()
# lecture des donnees
train_data = libfann.training_data()
train_data.read_train_from_file("./test2.data")
train_data.shuffle_train_data()

test_data = libfann.training_data()
test_data.read_train_from_file("./test2.data")
test_data.shuffle_train_data()


# Separation en entrainement/test
l = train_data.length_train_data()
tiers = l / 3
train_data.subset_train_data(0, tiers)
test_data.subset_train_data(tiers, 2*tiers)

# entrainement
taux_erreur = 2.0 # c'est arbitrairement grand
for i in range(1000) :
    print i
    ann.train_epoch(train_data)
    tmp = ann.test_data(test_data)
    print tmp
    if tmp < taux_erreur :
        ann.save("./emo_detect2.net")
        taux_erreur = tmp
#sauvegarde
ann.save("./emo_detect3.net")



