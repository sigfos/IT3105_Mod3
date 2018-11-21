import ANET
import copy
import numpy as np
import random
import math


class Tournament:

    def __init__(self, hex_state, games=10, anet1=None, anet2=None, epsilon=80):
        self.hex_state = hex_state
        self.anet1 = anet1
        self.anet2 = anet2
        self.wins_p1 = 0
        self.wins_p2 = 0
        self.games = games
        self.epsilon = epsilon

    def play_tournament(self):
        for i in range(self.games):
            result_one_game = self.play_one_game()
            if result_one_game == 1:
                print("Player 1 wins!")
                self.wins_p1 += 1
            else:
                print("Player 2 wins!")
                self.wins_p2 += 1
        self.print_result()

    def play_one_game(self):
        current_state = copy.deepcopy(self.hex_state)
        while not current_state.check_finished():
            print("It is player", str(current_state.player)+"'s turn")
            current_state.display_board()
            board = current_state.Hex_to_list()
            # board = [exp_node_copy.state.player] + board --> For server connection
            board.append(current_state.player)
            net_board = list_to_net(board)
            if current_state.player == 1:
                index = ANET.get_expanded_index(board, self.anet1, net_board)
            else:
                index = ANET.get_expanded_index(board, self.anet2, net_board)
            matrix_index_i = index // current_state.dimension
            matrix_index_j = index % current_state.dimension
            current_state.board[matrix_index_i][matrix_index_j].state = current_state.player
            current_state.player = current_state.change_player()
        current_state.display_board()
        return (current_state.get_result() + 1) % 2

    def print_result(self):
        print("Player 1 wins:", self.wins_p1, "with win rate ", self.wins_p1 / self.games)
        print("Player 2 wins:", self.wins_p2, "with win rate ", self.wins_p2 / self.games)


def list_to_net(list_board):
    one_hot_list = list()
    for element in list_board:
        if element == 1:
            one_hot_list += [1, 0]
        elif element == 2:
            one_hot_list += [0, 1]
        else:
            one_hot_list += [0, 0]
    return one_hot_list
