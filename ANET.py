from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam
import numpy as np


def get_data():
    # The data uses ROW vectors for a data point, that's what Keras assumes.
    data = list()
    _, d = data.shape
    X_train = data[:, 0:d - 1]
    Y = data[:, d - 1:d]
    y_train = Y.T[0]
    return X_train, y_train


def run_keras(X_train, y_train, layers, epochs, batch_size=32, verbose=True, loss='categorical_crossentropy',
              optimizer=Adam()):
    # Model specification
    model = Sequential()
    for layer in layers:
        model.add(layer)
    # Define the optimization
    model.compile(loss=loss, optimizer=optimizer, metrics=["accuracy"])
    N = X_train.shape[0]
    # Fit the model
    model.fit(X_train, y_train, epochs=epochs, batch_size=batch_size, verbose=verbose)
    return model


def create_layers(dims, input_act, output_act):
    layers = list()
    layers.append(Dense(dims[1], input_dim=dims[0], activation=input_act))
    if len(dims) > 2:
        for dim in dims[2:-1]:
            layers.append(Dense(dim, activation=input_act))
    layers.append(Dense(dims[-1], activation=output_act))
    return layers


x_train = np.random.random((100, 100, 100, 3))
print(x_train)

# layers = create_layers([10, 5, 2, 10], 'relu', 'sigmoid')
