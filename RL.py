from ANET import *
from HEX import *
from MCTS import *
from TOURNAMENT import *
import random
import os


class HexNN:

    def __init__(self, mcts, save_int=10, buffer=list(), buffer_int=1000, preload=False, file_add=""):
        self.mcts = mcts
        self.save_int = save_int
        self.buffer = buffer
        self.p1_wins = 0
        self.p2_wins = 0
        self.buffer_clear = buffer_int
        self.preload = preload
        self.file_add = file_add

    def run(self, mcts_sim, games):
        for i in range(games):
            print("Game number", i+1)
            best_path = list()
            mcts_current = self.mcts
            state = mcts_current.root_node.state
            game_sim = mcts_sim
            while not state.check_finished():  # Game has no winner
                next_node = mcts_current.run(game_sim)
                best_path.append(next_node)
                mcts_current = MCTS(next_node.state, anet=self.mcts.anet)
                state = next_node.state
                game_sim += 600
            winner = state.player % 2 + 1
            if winner == 1:
                self.p1_wins += 1
            else:
                self.p2_wins += 1
            print("Player", winner, "won!!")
            for node in best_path:
                label = create_distribution(node.parent)
                board = node.parent.state.Hex_to_list()
                net_board = node.parent.state.list_to_net(board)
                self.add_data(net_board, label)
            self.train()
            if i % self.save_int == 0 and i != 0:
                if self.preload:
                    for case in self.buffer:
                        self.add_data_to_file("RBUF.txt", case[0], case[1])
                self.mcts.anet.save_model(self.file_add+str(i))
            if i % self.buffer_clear == 0 and i != 0:
                if len(self.buffer) > 500:
                    self.buffer = self.buffer[500:]
            self.mcts.root_node.state.player = mcts_current.root_node.state.change_player()

    def add_data(self, x, label):
        self.buffer.append([x, label])

    def random_minibatch(self):
        x_train = []
        y_train = []
        if self.mcts.anet:
            for i in range(self.mcts.anet.batch_size):
                case = random.choice(self.buffer)
                x_train.append(case[0])
                y_train.append(case[1])
        else:
            for i in range(64):
                case = random.choice(self.buffer)
                x_train.append(case[0])
                y_train.append(case[1])
        return np.array(x_train), np.array(y_train)

    def training_buffer(self):
            x_train = []
            y_train = []
            if self.mcts.anet:
                for case in self.buffer:
                    x_train.append(case[0])
                    y_train.append(case[1])
            return np.array(x_train), np.array(y_train)

    def add_data_to_file(self, filename, x, label):
        if not os.stat(filename).st_size == 0:
            string = "\n"
        else:
            string = ""
        for i in range(len(x) - 1):
            string += (str(x[i]) + ",")
        string += str(x[-1])
        string += ";"
        for i in range(len(label) - 1):
            string += (str(label[i]) + ",")
        string += str(label[-1])
        file_obj = open(filename, 'a')
        file_obj.write(string)

    def train(self, training_sessions=1):
        for i in range(training_sessions):
            x_train, y_train = self.random_minibatch()
            self.mcts.anet.train(x_train, y_train)


def create_distribution(parent):
    p_board = parent.state.Hex_to_list()
    distribution = [0 for i in range(len(p_board))]
    if parent.children:
        for i in range(len(p_board)):
            if p_board[i] == 0:
                for child in parent.children:
                    if child.state.Hex_to_list()[i] != 0 and parent.wins != 0:
                        distribution[i] = child.wins / parent.wins
    return distribution


def preload_data(filename):
    # The data uses ROW vectors for a data point, that's what Keras assumes.
    file_obj = open(filename, 'r')
    data = list()
    for line in file_obj.readlines():
        line_vec = line.split(';')
        input_vec = line_vec[0].split(',')
        label = line_vec[1].split(',')
        data.append([list(map(float, input_vec)), list(map(float, label))])
    return data


if __name__ == '__main__':
    anet = Anet([20, 100, 9], batch_size=128)
    anet.create_anet()
    # prebuffer = preload_data("buffer_night.txt")
    root_board = create_root_board(3)
    hex_state = Hex(root_board, dimension=3, player=1)
    test1 = ANET.load_model("Test_10_9")
    test2 = ANET.load_model("Test_20_9")
    # anet1 = ANET.load_model("Demo_25_25")
    # anet2 = ANET.load_model("Demo_50_25")
    # anet3 = ANET.load_model("Demo_75_25")
    # anet4 = ANET.load_model("Demo_125_25")
    tournament = Tournament(hex_state, games=500, anet1=test1, anet2=test2, mix=True)
    tournament.play_tournament()
    # mcts = MCTS(hex_state, anet=anet)
    # anet1 = ANET.load_model("70_25", batch_size=32)
    mcts = MCTS(hex_state, anet=anet)
    hex_nn = HexNN(mcts, preload=False, file_add="Test_")
    # hex_nn.train(201)
    # hex_nn.run(2000, 101)
