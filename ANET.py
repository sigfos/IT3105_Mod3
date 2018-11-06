from keras.models import Sequential, model_from_json
from keras.layers import Dense
from keras.optimizers import Adam
import numpy as np
import random


def get_data(filename):
    # The data uses ROW vectors for a data point, that's what Keras assumes.
    file_obj = open(filename, 'r')
    data = list()
    for line in file_obj.readlines():
        line_vec = line.split(';')
        input_vec = line_vec[0].split(',')
        label = line_vec[1].split(',')
        data.append([list(map(float, input_vec)), list(map(float, label))])
    return data


def random_minibatch(cases, batch_size):
    batch_cases = []
    for i in range(batch_size):
        rand = random.randint(0, len(cases)-1)
        batch_cases.append(cases[rand])
    X_train = [batch_cases[i][0] for i in range(len(batch_cases))]
    y_train = [batch_cases[i][1] for i in range(len(batch_cases))]
    return np.array(X_train), np.array(y_train)


def add_data(x, label, filename):
    string = "\n"
    for value in x:
        string += (str(value) + ",")
    string += str(label)
    file_obj = open(filename, 'a')
    file_obj.write(string)


def init_keras(layers):
    # Model specification
    model = Sequential()
    for layer in layers:
        model.add(layer)
    return model


def create_layers(dims, input_act, output_act):
    layers = list()
    layers.append(Dense(dims[1], input_dim=dims[0], activation=input_act))
    if len(dims) > 2:
        for dim in dims[2:-1]:
            layers.append(Dense(dim, activation=input_act))
    layers.append(Dense(dims[-1], activation=output_act))
    layers.append(Dense(5))
    return layers


def save_model(model):
    model_json = model.to_json()
    with open("model.json", "w") as json_file:
        json_file.write(model_json)
    # serialize weights to HDF5
    model.save_weights("model.h5")
    print("Saved model to disk")


def load_model():
    json_file = open('model.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)
    # load weights into new model
    loaded_model.load_weights("model.h5")
    print("Loaded model from disk")
    return loaded_model


# må formatere slik at board håndteres rett
def check_valid_move(board, choice):
    flat_board = flatten_board(board)
    if flat_board[choice] == 0:
        return True
    return False


def flatten_board(board):
    return np.array(board).flatten().tolist()


# må formatere slik at board håndteres rett
def get_expanded_index(board):
    # data_input = flatten_board(board)
    data_input = board
    anet = load_model()
    predicted = anet.predict_classes(data_input)[0]
    if check_valid_move(data_input, predicted):
        return predicted
    else:
        while True:
            move = random.randint(0, len(board)-1)
            if check_valid_move(board, move):
                return move


def create_anet(dim=[9, 5, 5, 2, 2, 9], input_act='relu', output_act='sigmoid'):
    layers = create_layers(dim, input_act, output_act)
    model = init_keras(layers)
    save_model(model)


def train(epochs=10, batch_size=1, verbose=True, loss='sparse_categorical_crossentropy', optimizer=Adam()):
    model = load_model()
    cases = get_data("RBUF.txt")
    x_train, y_train = random_minibatch(cases, batch_size)
    # Define the optimization
    model.compile(loss=loss, optimizer=optimizer, metrics=["accuracy"])
    print(y_train.shape)
    model.fit(x_train, y_train, epochs=epochs, batch_size=batch_size, verbose=verbose)
    save_model(model)


create_anet()
train()
test = [0, 1, -1, 0, -1, 0, 0, 1, 0]
print(test, "predicted", get_expanded_index(np.array([test])))
