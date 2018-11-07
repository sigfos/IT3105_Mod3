import math
import copy


class Hex:

    def __init__(self, board=[0, 0, 0, 0, 0, 0, 0, 0, 0], dimension=3, player=1):
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
        return Hex(lis, int(math.sqrt(len(lis))), player)

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
        return ''.join(str(x) for x in self.board)

    def print_start(self):
        print("Starting game with this board: ")
        self.display_board()

    def print_status(self, best_child):
        print("Player " + str(self.player) + " produces: \n", best_child.display_board())

    def initialize(self):
        board = [0 for i in range(self.dimension**2)]
        return board

    """"
    Metoder fra Ludvig
    """
    # sjekk
    def dfs_visit(self, cell, color):
        if cell.visited:
            return False
        if cell.color == BLUE and (cell.i == self.size - 1):
            return True
        elif cell.color == YELLOW and cell.j == self.size - 1:
            return True
        cell.visited = True
        if cell.color == color:
            l = list(filter(lambda c: c.color == color, cell.neighbours))
            for cell_n in l:
                if not cell_n.visited:
                    return_value = dfs_visit(cell_n, color)
                    if return_value:
                        return True
        return dfs_visit(cell, color)

    # sjekk
    def check_single_winner(self, player):
            for row in self.board:
                for c in row:
                    c.visited = False
            for i in range(len(self.board)):
                if player == 1:
                    if self.board[0][i].color == BLUE and self.dfs(self.board[0][i], BLUE):
                        return True
                elif player == 2:
                    if self.board[i][0].color == YELLOW and self.dfs(self.board[i][0], YELLOW):
                        return True
            return False

    # works
    def is_finished(self):
        if self.check_single_winner(1):
            return 1
        elif self.check_single_winner(2):
            return 2
        else:
            return 0

hex = Hex(dimension=4)
hex.initialize()
hex.display_board()
