from ANET import *
from HEX import *
from MCTS import *
import os


class HexNN:

    def __init__(self, mcts, anet, save_int=50, buffer="RBUF.txt"):
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
            anet.train(self.buffer)
            if i % self.save_int == 0:
                self.anet.save_model()
                self.clear_buffer()

    def clear_buffer(self):
        open(self.buffer, 'w').close()

    def add_data(self, x, label):
        if not os.stat(self.buffer).st_size == 0:
            string = "\n"
        else:
            string = ""
        for i in range(len(x)-1):
            string += (str(x[i]) + ",")
        string += str(x[-1])
        string += ";"
        for i in range(len(label)-1):
            string += (str(label[i]) + ",")
        string += str(label[-1])
        file_obj = open(self.buffer, 'a')
        file_obj.write(string)


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
