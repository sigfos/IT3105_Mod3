from ANET import *
from HEX import *
from MCTS import *


class HexNN:

    def __init__(self, mcts, anet, save_int=50):
        self.mcts = mcts
        self.anet = anet
        self.save_int = save_int
        anet.create_anet()

    def run(self, mcts_sim, games):
        for i in range(games):
            best_path = self.mcts.run(mcts_sim)
            for node in best_path:
                # add to RBUF x - label
                pass
            anet.train("RBUF.txt")
            if i % self.save_int == 0:
                ANET.save_model(anet.model)


if __name__ == '__main__':
        anet = Anet()
        hex_state = Hex([0,0,0,0,0,0,0,0,0])
        mcts = MCTS(hex_state, 1, anet)
        hex_nn = HexNN(mcts, anet)
        hex_nn.run(1000, 100)
