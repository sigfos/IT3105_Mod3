import math
import ANET
import copy


class Node:

    def __init__(self, state):
        self.visits = 0
        self.parent = None
        self.children = []
        self.wins = 0
        self.state = state


class MCTS:

    def __init__(self, state, verbose=True, anet=None):
        self.root_node = Node(state)
        self.print_out = verbose
        self.anet = anet
        self.last_time = False

    """
    Choose the node to expand based on node value (exploitation + exploration)
    """
    def selection(self):
        max_node = self.root_node
        if len(self.root_node.children) == self.root_node.state.Hex_to_list().count(0):
            max_value = -1
            for child in self.root_node.children:
                exploitation_value = child.wins/child.visits
                exploration_value = 1*math.sqrt(math.log(self.root_node.visits)/child.visits)
                if self.root_node.state.player == 1:
                    node_value = exploitation_value + exploration_value
                else:
                    node_value = -exploitation_value + exploration_value
                if node_value > max_value:
                    max_node = child
                    max_value = node_value
            return max_node
        else:
            return self.expansion(self.root_node)

    """
    Expand the node found in selection with a child. If the state is similar to one already explored, use 
    the saved node from the dictionary to increase speed
    """
    def expansion(self, leaf):
        num = len(leaf.children)
        generated_children = leaf.state.generate_children()
        expanded_node = Node(generated_children[num])
        expanded_node.parent = leaf
        leaf.children.append(expanded_node)
        return expanded_node

    """
    Simulate a result from the expanded node
    """
    def simulation(self, expanded_node):
        exp_node_state = copy.deepcopy(expanded_node.state)
        while not exp_node_state.check_finished():
            current_state = exp_node_state
            board = current_state.Hex_to_list()
            # board = [exp_node_copy.state.player] + board --> For server connection
            board.append(exp_node_state.player)
            net_board = current_state.list_to_net(board)
            index = ANET.get_expanded_index(board, self.anet, net_board)
            matrix_index_i = index//exp_node_state.dimension
            matrix_index_j = index % exp_node_state.dimension
            exp_node_state.board[matrix_index_i][matrix_index_j].state = exp_node_state.player
            exp_node_state.player = exp_node_state.change_player()
        return (exp_node_state.get_result() + 1) % 2

    """
    Save the result from the simulation in all the parent nodes of the expanded node
    """
    def backprop(self, expanded_node, result_from_simulation):
        current_node = expanded_node
        current_node.wins += result_from_simulation
        current_node.visits += 1
        while current_node.parent:
            current_node = current_node.parent
            current_node.wins += result_from_simulation
            current_node.visits += 1

    def run_one_simulation(self):
        selected = self.selection()
        res = self.simulation(selected)
        self.backprop(selected, res)

    def run(self, simulations):
        for i in range(simulations):
            self.run_one_simulation()
        selected = self.root_node
        best_child = None
        if selected.children:
            best_rate = -1
            for child in selected.children:
                if selected.state.player == 1:
                    win_rate = child.wins/child.visits
                else:
                    win_rate = 1 - child.wins/child.visits
                if win_rate >= best_rate:
                    best_rate = win_rate
                    best_child = child
            if self.print_out:
                selected.state.print_status(best_child.state)
        return best_child
