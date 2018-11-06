import math
import copy


class Hex:

    def __init__(self, board, dimension=4, player=1):
        self.board = board
        self.player = player
        self.dimension = dimension

    def display_board(self):
        print("\nIt is player", str(self.player) + "'s turn with current board: ")
        new_size = int(2*self.dimension-1)
        diamond_grid = [[" " for i in range(new_size)] for j in range(new_size)]
        for i in range (len(self.board)):
            newrow = int(i // self.dimension + i % self.dimension)
            newcol = int(self.dimension-1 + i % self.dimension - i // self.dimension)
            diamond_grid[newrow][newcol] = self.board[i]
        for i in range(len(diamond_grid)):
            outString = ""
            for element in diamond_grid[i]:
                outString += " "+str(element)+" "
            print(outString)

    def Hex_to_list(self):
        return self.board

    def list_to_Hex(self, lis, player):
        return Hex(list, int(math.sqrt(len(lis))), player)

    def check_finished(self):
        # Do DFS
        pass

    def generate_children(self):
        states = []
        for i in range(len(self.board)):
            copy_board = copy.deepcopy(self.board)
            if copy_board[i] == 0:
                if self.player == 1:
                    copy_board[i] = 1
                elif self.player == 2:
                    copy_board[i] = -1
                states.append(self.list_to_Hex(copy_board, self.player%2+1))
        return states

    def change_player(self):
        if self.player == 1:
            return 2
        return 1

    def get_result(self):
        if self.player == 1:
            return 1
        return 0

    def get_key(self):
        return self.board

    def print_start(self):
        print("Starting game with this board: ")
        self.display_board()

    def print_status(self, best_child):
        print("Player " + str(self.player) + " produces: \n", best_child.display_board())


def initialize(dim=4):
    board = [0 for i in range(dim**2)]
    return board

dim = 3
hex = Hex(initialize(dim), dim)
hex.display_board()
