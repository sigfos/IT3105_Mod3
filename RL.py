from ANET import *
from HEX import *
from MCTS import *
import random


class HexNN:

    def __init__(self, mcts, anet, save_int=10, buffer=list()):
        self.mcts = mcts
        self.anet = anet
        self.save_int = save_int
        self.buffer = buffer
        anet.create_anet()

    def run(self, mcts_sim, games):
        for i in range(games):
            best_path = self.mcts.run(mcts_sim)
            for node in best_path:
                label = create_distribution(node)
                if label.count(0) != node.state.dimension**2:
                    self.add_data(node.state.Hex_to_list(), label)
            x_train, y_train = self.random_minibatch()
            anet.train(x_train, y_train)
            if i % self.save_int == 0 and i != 0:
                self.anet.save_model()
                self.buffer.clear()
            print(self.buffer)

    def add_data(self, x, label):
        self.buffer.append([x, label])

    def random_minibatch(self):
        x_train = []
        y_train = []
        for i in range(self.anet.batch_size):
            case = random.choice(self.buffer)
            x_train.append(case[0])
            y_train.append(case[1])
        return np.array(x_train), np.array(y_train)


def create_distribution(parent):
    p_board = parent.state.Hex_to_list()
    distribution = [0 for i in range(len(p_board))]
    total = 0
    if parent.children:
        for child in parent.children:
            total += child.visits
        child_count = 0
        for i in range(len(p_board)):
            if p_board[i] == 0:
                if child_count < len(parent.children):
                    distribution[i] = parent.children[child_count].visits/total
                    child_count += 1
    return distribution


if __name__ == '__main__':
    anet = Anet([9, 5, 5, 9], batch_size=10)
    root_board = create_root_board(3)
    hex_state = Hex(root_board, dimension=3)
    mcts = MCTS(hex_state, 1, anet)
    hex_nn = HexNN(mcts, anet)
    hex_nn.clear_buffer()
    hex_nn.run(1000, 10)
