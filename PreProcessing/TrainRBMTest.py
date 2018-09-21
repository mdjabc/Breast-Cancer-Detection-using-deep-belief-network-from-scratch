import numpy as np
from random import randrange
from PreProcessing.Activation import sigmoid


def trainRBM(dataset, weights, num_hidden, max_epoch=300, learning_rate=0.1):
    # Insert bias units of 1 into the first column.
    # train_data = np.insert(train_data, 0, 1, axis=1)
    dataset = np.insert(dataset, 0, 1, axis=1)
    # train_datas = mini_batch(dataset, 10)
    for epoch in range(max_epoch):
        reconstructed_data = list()

        # creating mini batch of size 30
        for i in range(0, dataset.shape[0], 30):
            train_data = dataset[i:i + 30]
            num_examples = train_data.shape[0]

            # (This is the "positive CD phase", aka the reality phase.)
            pos_hidden_activations = np.dot(train_data, weights)
            pos_hidden_probs = sigmoid(pos_hidden_activations)
            pos_hidden_probs[:, 0] = 1
            pos_hidden_states = pos_hidden_probs > np.random.rand(num_examples, num_hidden + 1)
            pos_associations = np.dot(train_data.T, pos_hidden_probs)

            # (This is the "negative CD phase", aka the daydreaming phase.)
            neg_visible_activations = np.dot(pos_hidden_states, weights.T)
            neg_visible_probs = sigmoid(neg_visible_activations)
            neg_visible_probs[:, 0] = 1

            neg_hidden_activations = np.dot(neg_visible_probs, weights)
            neg_hidden_probs = sigmoid(neg_hidden_activations)

            # adding batch data in reconstructed_data list to pass to next RBM layer
            reconstructed_data[i:i+30] = neg_hidden_probs

            neg_hidden_probs[:, 0] = 1

            neg_associations = np.dot(neg_visible_probs.T, neg_hidden_probs)

            # Update weights.
            weights += learning_rate * ((pos_associations - neg_associations) / num_examples)

            error = np.sum((train_data - neg_visible_probs) ** 2)
        if True:
            print("\t\t>>Epoch {}: error is {}".format(epoch, error))
    print("\t\t\n\n-----****Pre-Training Model Trained ***----\n\n")
    # print("Epoch %s: error is %s" % (epoch, error))

    return weights, reconstructed_data



