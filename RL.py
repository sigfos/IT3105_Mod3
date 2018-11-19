from ANET import *
from HEX import *
from MCTS import *
import random


class HexNN:

    def __init__(self, mcts, save_int=10, buffer=list(), tournament=False):
        self.mcts = mcts
        self.save_int = save_int
        self.buffer = buffer
        self.tournament = tournament
        self.p1_wins = 0
        self.p2_wins = 0

    def run(self, mcts_sim, games):
        for i in range(games):
            print("Game number", i+1)
            best_path = list()
            mcts_current = self.mcts
            state = mcts_current.root_node.state
            while not state.check_finished():  # Game has no winner
                next_node = mcts_current.run(mcts_sim)
                best_path.append(next_node)
                if not self.tournament:
                    mcts_current = MCTS(next_node.state, anet=self.mcts.anet)
                else:
                    mcts_current = MCTS(next_node.state, anet=self.mcts.anet, anet2=self.mcts.anet2)
                state = next_node.state
            winner = state.player % 2 + 1
            if winner == 1:
                self.p1_wins += 1
            else:
                self.p2_wins += 1
            print("Player", winner, "won!!")
            if not self.tournament:
                for node in best_path:
                    label = create_distribution(node.parent)
                    if label.count(0) != node.state.dimension**2:
                        board = node.parent.state.Hex_to_list()
                        board.append(node.parent.state.player)
                        self.add_data(board, label)
                x_train, y_train = self.random_minibatch()
                mcts.anet.train(x_train, y_train)
                if i % self.save_int == 0 and i != 0:
                    print_cases_to_file(self.buffer)
                    self.mcts.anet.save_model(str(i))
                    self.buffer.clear()

    def add_data(self, x, label):
        self.buffer.append([x, label])

    def random_minibatch(self):
        x_train = []
        y_train = []
        for i in range(self.mcts.anet.batch_size):
            case = random.choice(self.buffer)
            x_train.append(case[0])
            y_train.append(case[1])
        return np.array(x_train), np.array(y_train)


def create_distribution(parent):
    p_board = parent.state.Hex_to_list()
    distribution = [0 for i in range(len(p_board))]
    if parent.children:
        for i in range(len(p_board)):
            if p_board[i] == 0:
                for child in parent.children:
                    if child.state.Hex_to_list()[i] != 0:
                        distribution[i] = child.wins / child.visits
    return distribution


def print_cases_to_file(cases):
    file = open("cases.txt", 'a')
    for case in cases:
        file.write(''.join(str(c)+"-" for c in case[0]) + " " + ''.join(str(c)+"-" for c in case[1]) + "\n")


if __name__ == '__main__':
    anet = Anet([26, 1024, 1024, 1024, 25], batch_size=32)
    anet.create_anet()
    root_board = create_root_board(5)
    hex_state = Hex(root_board, dimension=5, player=1)
    # anet2 = ANET.load_model("10_9", [26, 100, 25])
    # mcts = MCTS(hex_state, anet=anet2)
    # anet1 = ANET.load_model("40_25")
    mcts = MCTS(hex_state, anet=anet)
    hex_nn = HexNN(mcts, tournament=False)
    hex_nn.run(100, 101)
    print("Player 1 wins:", hex_nn.p1_wins)
    print("Player 2 wins:", hex_nn.p2_wins)
