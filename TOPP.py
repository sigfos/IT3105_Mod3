from TOURNAMENT import *
from HEX import *


class TOPP:

    def __init__(self, players=list(), games=list(), board_dim=5, epsilon=95):
        self.players = players
        self.games = games
        self.board_dim = board_dim
        self.wins = [0 for i in range(len(self.players))]
        self.epsilon = epsilon

    def play_tournament(self):
        for i in range(len(self.players)):
            for j in range(len(self.players)-i):
                player1 = self.players[i]
                player2 = self.players[j+i]
                if player1 == player2:
                   continue
                matrix_board = [[0 for i in range(self.board_dim)]for i in range(self.board_dim)]
                hex = Hex(matrix_board, self.board_dim, random.randint(1,2))
                match = Tournament(hex, self.games, anet2=player1, anet1=player2, epsilon=95, mix=True)
                if match.wins_p1 > match.wins_p2:
                    self.wins[i] += 1
                else:
                    self.wins[-i] += 1
        self.print_result()

    def print_result(self):
        print("..........RESULTS..........")
        result_list = copy.copy(self.wins)
        result_list.sort()
        for i in range(len(result_list)):
            player = self.wins.index(result_list[-(i+1)])
            print(i+1, ". Player", player, "wins = ", result_list[-(i+1)])
