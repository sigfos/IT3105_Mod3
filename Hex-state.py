
class Cell:

    def __init__(self, start_cell_p1=False, end_cell_p1=False, start_cell_p2=False,
                 end_cell_p2=False, state=0, neighbors=[], connected_cells=[]):
        self.state = 0
        self.neighbors = neighbors
        self.conn_cells = connected_cells
        self.start_cell_p1 = start_cell_p1
        self.end_cell_p1 = end_cell_p1
        self.start_cell_p2 = start_cell_p2
        self.end_cell_p2 = end_cell_p2

    def occupy_cell(self, player):
        if player == 1:
            self.state = 1
        else:
            self.state = -1
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

    def get_flat_board(self):
        flat_board = []
        for i in range(self.dimension):
            for j in range(self.dimension):
                flat_board.append(self.board[i][j])
        return flat_board

    def print_diamond_board(self, diamond_board):
        for i in range(len(diamond_board)):
            outString = ""
            for element in diamond_board[i]:
                outString += " "+element+" "
            print(outString)

    def display_board(self):
        print("It is player", str(self.player) + "'s turn with current board: ")
        new_size = 2*self.dimension-1
        diamond_grid = [[" " for i in range(new_size)] for j in range(new_size)]
        flat_board = self.get_flat_board()
        for cell in flat_board:
            newrow = int(flat_board.index(cell) // self.dimension + flat_board.index(cell) % self.dimension)
            newcol = int(self.dimension-1 + flat_board.index(cell) % self.dimension - flat_board.index(cell) // self.dimension)
            diamond_grid[newrow][newcol] = str(cell.state)
        self.print_diamond_board(diamond_grid)

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

    def board_to_list(self):
        outList = []
        flat = self.get_flat_board()
        for c in flat:
            outList.append(c.state)
        return outList

    def generate_children(self):
        states = []
        for i in range(len(self.board)):
            copy_board = self.board.deepcopy()
            if copy_board[i].state == 0:
                if self.player == 1:
                    copy_board.state[i] = 1
                elif self.player == 2:
                    copy_board.state[i] = -1
                states.append(copy_board)
        return states

    def get_key(self):
        return self.board

    def print_start(self):
        print("Starting game with this board: ")
        self.display_board()

    def print_status(self, best_child):
        print("Player " + str(self.player) + " produces: \n", best_child.display_board())


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
            # NB nå bestemmer vi eksakt hvilken side p1 og p2 skal starte
            # Skal den kunne velge selv blant sine to langsider?
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
                cell.neighbors.append(cell_board[i-1][j])
    return cell_board

dim = 4
hex = Hex(create_root_board(dim), dim)
hex.display_board()
