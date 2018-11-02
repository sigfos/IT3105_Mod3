
class Cell:
    # Three possible cell states: (0,0) empty, (1,0) filled by player 1, (0,1) filled by player 2

    def __init__(self, start_cell_p1=False, end_cell_p1=False, start_cell_p2=False,
                 end_cell_p2=False, state=(0, 0), neighbors=[], connected_cells=[]):
        self.state = state
        self.neighbors = neighbors
        self.conn_cells = connected_cells
        self.start_cell_p1 = start_cell_p1
        self.end_cell_p1 = end_cell_p1
        self.start_cell_p2 = start_cell_p2
        self.end_cell_p2 = end_cell_p2

    def occupy_cell(self, player):
        if player == 1:
            self.state = (1, 0)
        else:
            self.state = (0, 1)
        if len(self.neighbors) > 0:
            for neighbor in self.neighbors:
                if neighbor.state == self.state:
                    copy_conn_cells = self.conn_cells.copy()
                    self.conn_cells.append(neighbor)
                    self.conn_cells += neighbor.conn_cells
                    neighbor.conn_cells.append(self)
                    neighbor.conn_cells += copy_conn_cells

    def __str__(self):
        return str(self.state)


class Hex:

    def __init__(self, board, dimension=4, player=1):
        self.board = board
        self.player = player
        self.dimension = dimension

    def display_board(self):
        print("It is player", str(self.player) + "'s turn with current board: ")
        i = 0
        k = 1
        reached_max = False
        while i > -1:
            row = ""
            for j in range(i+1):
                if not reached_max:
                    row += str(self.board[i-j][j])
                else:
                    row += str(self.board[self.dimension-1-j][j+k]) + " "
            if reached_max:
                k += 1
            print((self.dimension-i)*"\t", row)
            if i == (self.dimension-1):
                reached_max = True
            if reached_max:
                i -= 1
            else:
                i += 1

    def change_player(self):
        if self.player == 1:
            return 2
        return 1

    def get_result(self):
        if self.player == 1:
            return 1
        return 0

    def check_finished(self):
        for row in self.board:
            for entry in row:
                start_p1 = False
                end_p1 = False
                start_p2 = False
                end_p2 = False
                for connected_cell in entry.conn_cells:
                    if connected_cell.start_cell_p1:
                        start_p1 = True
                    elif connected_cell.end_cell_p1:
                        end_p1 = True
                    if connected_cell.start_cell_p2:
                        start_p2 = True
                    elif connected_cell.end_cell_p2:
                        end_p2 = True
                if start_p1 and end_p1 or start_p2 and end_p2:
                    return True
        return False

    def generate_children(self):
        states = []
        for row in self.board:
            for cell in row:
                if cell.state == (0, 0):
                    # Her genereres ikke barn på riktig måte. Må endre cellen kun for hex_child. Kanskje lage en
                    # update cell metode eller noe
                    new_board = self.board.copy()
                    hex_child = Hex(new_board, player=self.change_player())
                    cell.occupy_cell(self.player)
                    states.append(hex_child)
        return states

    def get_key(self):
        return self.board

    def print_start(self):
        print("Starting game with this board: ")
        self.display_board()

    def print_status(self, best_child):
        print("Player " + str(self.player) + " produces: \n", best_child.display_board())


def create_root_board(dim=4):
    root_board = [[Cell() for i in range(dim)] for y in range(dim)]
    for i in range(dim):
        for j in range(dim):
            if i == 0:
                root_board[i][j].start_cell_p2 = True
            if i == dim-1:
                root_board[i][j].end_cell_p2 = True
            if j == 0:
                root_board[i][j].start_cell_p1 = True
            if j == dim-1:
                root_board[i][j].end_cell_p1 = True
            # Her må neighbors legges til, men det skjer ikke på rett måte. Indeks skal være rett, men alle legges til
            # i alle celler
            try:
                root_board[i][j].neighbors.append(root_board[i][j+1])
                root_board[i][j+1].neighbors.append(root_board[i][j])
            except IndexError:
                pass
            try:
                root_board[i][j].neighbors.append(root_board[i+1][j])
                root_board[i+1][j].neighbors.append(root_board[i][j])
            except IndexError:
                pass
            try:
                root_board[i][j].neighbors.append(root_board[i+1][j-1])
                root_board[i+1][j-1].neighbors.append(root_board[i][j])
            except IndexError:
                pass
    return root_board


hex = Hex(create_root_board())
hex.display_board()
