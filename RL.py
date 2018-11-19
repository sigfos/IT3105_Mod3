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
                    label = create_distribution(node)
                    if label.count(0) != node.state.dimension**2:
                        board = node.state.Hex_to_list()
                        board.append(node.state.player)
                        self.add_data(board, label)
                x_train, y_train = self.random_minibatch()
                mcts.anet.train(x_train, y_train)
                if i % self.save_int == 0 and i != 0:
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
    anet = Anet([26, 100, 25], batch_size=10)
    anet.create_anet()
    root_board = create_root_board(5)
    hex_state = Hex(root_board, dimension=5, player=1)
    anet2 = ANET.load_model("10_9", [26, 100, 25])
    # mcts = MCTS(hex_state, anet=anet2)
    anet1 = ANET.load_model("40_25")
    mcts = MCTS(hex_state, anet2=anet2)
    hex_nn = HexNN(mcts, tournament=True)
    hex_nn.run(100, 30)
    print("Player 1 wins:", hex_nn.p1_wins)
    print("Player 2 wins:", hex_nn.p2_wins)
