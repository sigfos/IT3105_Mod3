from keras.models import Sequential, model_from_json
from keras.layers import Dense
import numpy as np
import random


class Anet:

    def __init__(self, dims=[9, 5, 5, 9], input_act='relu', output_act='softmax', init='uniform',
                 epochs=2, batch_size=10, verbose=True, loss='mse', optimizer="adam", model=None):
        self.dims = dims
        self.input_act = input_act
        self.output_act = output_act
        self.init = init
        self.epochs = epochs
        self.batch_size = batch_size
        self.verbose = verbose
        self.loss = loss
        self.optimizer = optimizer
        self.model = model

    def create_layers(self, dims, input_act, output_act):
        layers = list()
        layers.append(Dense(dims[1], input_dim=dims[0], init=self.init, activation=input_act))
        if len(dims) > 3:
            for dim in dims[2:-1]:
                layers.append(Dense(dim, init=self.init, activation=input_act))
        layers.append(Dense(dims[-1], init=self.init, activation=output_act))
        return layers

    def create_anet(self):
        layers = self.create_layers(self.dims, self.input_act, self.output_act)
        model = Sequential()
        for layer in layers:
            model.add(layer)
        self.model = model

    def save_model(self, iteration):
        model_json = self.model.to_json()
        with open(iteration+"_model.json", "w") as json_file:
            json_file.write(model_json)
        # serialize weights to HDF5
        self.model.save_weights(iteration+"_model.h5")
        print("Saved model to disk")

    def train(self, x_train, y_train):
        self.model.compile(loss=self.loss, optimizer=self.optimizer, metrics=["accuracy"])
        self.model.fit(x_train, y_train, epochs=self.epochs, batch_size=self.batch_size, verbose=self.verbose)


def load_model(iteration):
    json_file = open(iteration+"_model.json", 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)
    # load weights into new model
    loaded_model.load_weights(iteration+"_model.h5")
    loaded_anet = Anet(model=loaded_model)
    print("Loaded model", iteration+"_model.json", "from disk")
    return loaded_anet


def check_valid_move(board, choice):
    if board[choice] == 0:
        return True
    return False


def get_expanded_index(board, anet):
    format_board = np.array([board])
    predicted = anet.model.predict_classes(format_board)[0]
    if check_valid_move(board, predicted):
        # count children before to find index of generated child
        return board[:predicted].count(0)
    else:
        move = random.randint(0, len(board)-1)
        while not check_valid_move(board, move):
            move = random.randint(0, len(board)-1)
        return board[:move].count(0)
