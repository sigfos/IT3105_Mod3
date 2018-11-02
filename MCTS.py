import math
import random


class Node:

    def __init__(self, state):
        self.visits = 0
        self.parent = None
        self.children = []
        self.wins = 0
        self.state = state


class MCTS:

    def __init__(self, state, verbose):
        self.root_node = Node(state)
        self.nodes = {(state.get_key(), state.player): self.root_node}
        self.print_out = verbose

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
        if len(generated_children) == 0:
            return leaf
        key = (generated_children[num].N, generated_children[num].player)
        if key in self.nodes.keys():
            expanded_node = self.nodes.get(key)
        else:
            expanded_node = Node(generated_children[num])
            self.nodes[key] = expanded_node
        expanded_node.parent = leaf
        leaf.children.append(expanded_node)
        return expanded_node

    """
    Simulate a result from the expanded node
    """
    def simulation(self, expanded_node):
        current_state = expanded_node.state
        while not current_state.check_finished():
            children = current_state.generate_children()
            # Pick this through ANET instead
            child = random.choice(children)
            current_state = child
        return (current_state.get_result()+1) % 2

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
        best_path = [self.root_node]
        selected = self.root_node
        if self.print_out:
            selected.state.print_start()
        while selected.children:
            best_rate = -1
            for child in selected.children:
                if selected.state.player == 1:
                    win_rate = child.wins/child.visits
                else:
                    win_rate = 1 - child.wins/child.visits
                if win_rate >= best_rate:
                    best_rate = win_rate
                    best_child = child
            best_path.append(best_child)
            if self.print_out:
                selected.state.print_status(best_child.state)
            selected = best_child
        return best_path
