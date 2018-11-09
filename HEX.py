import copy
import math


class Cell:

    def __init__(self, start_cell_p1=False, end_cell_p1=False, start_cell_p2=False,
                 end_cell_p2=False, state=0, neighbors=[]):
        self.state = state
        self.neighbors = neighbors
        self.start_cell_p1 = start_cell_p1
        self.end_cell_p1 = end_cell_p1
        self.start_cell_p2 = start_cell_p2
        self.end_cell_p2 = end_cell_p2

    def occupy_cell(self, player):
        if player == 1:
            self.state = 1
        else:
            self.state = 2

    def __str__(self):
        return str(self.state)


class Hex:

    def __init__(self, board, dimension=4, player=1):
        self.board = board # matrix
        self.player = player
        self.dimension = dimension

    def get_flat_board(self):
        flat_board = []
        for i in range(self.dimension):
            for j in range(self.dimension):
                flat_board.append(self.board[i][j])
        return flat_board

    def display_board(self):
        print("It is player", str(self.player) + "'s turn with current board: ")
        new_size = 2*self.dimension-1
        diamond_grid = [[" " for i in range(new_size)] for j in range(new_size)]
        flat_board = self.get_flat_board()
        for cell in flat_board:
            newrow = int(flat_board.index(cell) // self.dimension + flat_board.index(cell) % self.dimension)
            newcol = int(self.dimension-1 + flat_board.index(cell) % self.dimension - flat_board.index(cell) // self.dimension)
            diamond_grid[newrow][newcol] = str(cell.state)
        for i in range(len(diamond_grid)):
            outString = ""
            for element in diamond_grid[i]:
                if element == "0":
                    element = "-"
                outString += " "+element+" "
            print(outString)

    def check_finished(self):
        if self.check_single_winner(1) or self.check_single_winner(2):
            return True
        return False

    def check_single_winner(self, player):
        for i in range(self.dimension):
            if player == 1:
                if self.board[i][0].state == 1:
                    if self.dfs(self.board[i][0], 1, []):
                        return True
            elif player == 2:
                if self.board[0][i].state == 2:
                    if self.dfs(self.board[0][i], 2, []):
                        return True
        return False

    def dfs(self, cell, player, visited=[]):
        if cell not in visited:
            visited.append(cell)
            actual_neighbors = []
            for n in cell.neighbors:
                if n.state == player:
                    actual_neighbors.append(n)
            for an in actual_neighbors:
                self.dfs(an, player, visited)
        for cell in visited:
            if player == 1 and cell.end_cell_p1:
                return True
            if player == 2 and cell.end_cell_p2:
                return True
        return False

    def Hex_to_list(self):
        outList = []
        flat = self.get_flat_board()
        for c in flat:
            outList.append(c.state)
        return outList

    def list_to_Hex(self, lis, player):
        cell_list = [Cell() for i in range(len(lis))]
        for i in range (len(lis)):
            cell_list[i].state = lis[i]
        dim = int(len(cell_list))
        dim = int(math.sqrt(dim))
        return Hex(cell_list, dim, player)

    def generate_children(self):
        states = []
        for i in range(self.dimension):
            for j in range(self.dimension):
                copy_hex = copy.deepcopy(self)
                if copy_hex.board[i][j].state == 0:
                    if self.player == 1:
                        copy_hex.board[i][j].state = 1
                    elif self.player == 2:
                        copy_hex.board[i][j].state = 2
                    copy_hex.player = copy_hex.change_player()
                    states.append(copy_hex)
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
        board_list = self.Hex_to_list()
        return ''.join(str(x) for x in board_list)

    def print_status(self, best_child):
        print("Player " + str(self.player) + " produces: \n")
        best_child.display_board()

    def print_start(self):
        print("Player " + str(self.player) + " starts with: \n")
        self.display_board()


def create_root_board(dim=4):
    cell_board = [[Cell() for i in range(dim)] for j in range(dim)]
    for i in range(dim):
        for j in range(dim):
            cell = cell_board[i][j]
            # Set fields to initialized value (why does it not work otherwise?)
            cell.neighbors = []
            cell.start_cell_p1 = False
            cell.start_cell_p2 = False
            cell.end_cell_p1 = False
            cell.end_cell_p2 = False
            if i == 0:
                cell.start_cell_p2 = True
            if i == dim-1:
                cell.end_cell_p2 = True
            if j == 0:
                cell.start_cell_p1 = True
            if j == dim-1:
                cell.end_cell_p1 = True
            if not i == 0:
                cell.neighbors.append(cell_board[i-1][j])
            if not j == 0:
                cell.neighbors.append(cell_board[i][j-1])
            if not i == dim-1:
                cell.neighbors.append(cell_board[i+1][j])
            if not j == dim-1:
                cell.neighbors.append(cell_board[i][j+1])
            if not (i == 0 or j == dim-1):
                cell.neighbors.append(cell_board[i-1][j+1])
            if not (i == dim-1 or j == 0):
                cell.neighbors.append(cell_board[i+1][j-1])
    return cell_board
