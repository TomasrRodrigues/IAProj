# GameTree.py
import copy

class GameTreeNode:
    def __init__(self, state, parent=None):
        self.state = state
        self.parent = parent
        self.children = []  # List of child GameTreeNode instances.
        self.value = None   # You can store evaluation values here later if needed.
        self.move = None    # The move that led to this state (optional).

    def add_child(self, child_state, move=None):
        child_node = GameTreeNode(child_state, parent=self)
        child_node.move = move
        self.children.append(child_node)
        return child_node

    def get_children(self):
        return self.children

    def get_parent(self):
        return self.parent

    def is_leaf(self):
        return len(self.children) == 0

    def __str__(self):
        return f"GameTreeNode(state={self.state}, move={self.move}, children={len(self.children)})"

    def print_tree(self, level=0):
        indent = " " * (level * 2)
        print(f"{indent}{self}")
        for child in self.children:
            child.print_tree(level + 1)
