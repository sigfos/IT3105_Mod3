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

    def __init__(self, state, verbose=True, anet=None, anet1=None, anet2=None):
        self.root_node = Node(state)
        self.print_out = verbose
        self.anet = anet
        self.anet1 = anet1
        self.anet2 = anet2

    """
    Choose the node to expand based on node value (exploitation + exploration)
    """
    def selection(self):
        current_node = self.root_node
        max_node = self.root_node

        while len(current_node.children) == len(
                current_node.state.generate_children()) and not current_node.state.check_finished():
            max_value = -100
            for child in current_node.children:
                child.parent = current_node
                exploitation_value = child.wins/child.visits
                exploration_value = math.sqrt(2)*math.sqrt(math.log(child.parent.visits)/child.visits)
                if current_node.state.player == 1:
                    node_value = exploitation_value + exploration_value
                else:
                    node_value = (1-exploitation_value) + exploration_value
                if node_value > max_value:
                    max_node = child
                    max_value = node_value
            current_node = max_node
        return current_node

    """
    Expand the node found in selection with a child. If the state is similar to one already explored, use 
    the saved node from the dictionary to increase speed
    """
    def expansion(self, leaf):
        num = len(leaf.children)
        generated_children = leaf.state.generate_children()
        if leaf.state.check_finished():
            return leaf
        expanded_node = Node(generated_children[num])
        expanded_node.parent = leaf
        leaf.children.append(expanded_node)
        return expanded_node

    """
    Simulate a result from the expanded node
    """
    def simulation(self, expanded_node):
        exp_node_copy = copy.deepcopy(expanded_node)
        while not exp_node_copy.state.check_finished():
            current_state = exp_node_copy.state
            board = current_state.Hex_to_list()
            board.append(expanded_node.state.player)
            if self.anet2:
                if current_state.player == 1:
                    index = ANET.get_expanded_index(board, self.anet1)
                else:
                    index = ANET.get_expanded_index(board, self.anet2)
            else:
                index = ANET.get_expanded_index(board, self.anet)
            matrix_index_i = index//exp_node_copy.state.dimension
            matrix_index_j = index % exp_node_copy.state.dimension
            exp_node_copy.state.board[matrix_index_i][matrix_index_j].state = exp_node_copy.state.player
            exp_node_copy.state.player = exp_node_copy.state.change_player()
        return (exp_node_copy.state.get_result()+1) % 2

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
        expanded_node = self.expansion(selected)
        res = self.simulation(expanded_node)
        self.backprop(expanded_node, res)

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
