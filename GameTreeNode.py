# GameTree.py
import copy

class GameTreeNode:
    def __init__(self, state, parent=None, move=None):
        """
        Initialize a game tree node.
        :param state: An instance of GameState representing the game state at this node.
        :param parent: The parent GameTreeNode (None for root).
        :param move: The move that produced this state (for tracking purposes).
        """
        self.state = state
        self.parent = parent
        self.children = []  # List of child GameTreeNode objects.
        self.move = move    # The move that produced this state.
        self.value = None   # Evaluation value (can be set during minimax).

    def add_child(self, child_state, move=None):
        """
        Create a child node for this node and add it to the children.
        :param child_state: The game state for the child node.
        :param move: The move that led to the child state.
        :return: The newly created GameTreeNode.
        """
        child = GameTreeNode(child_state, parent=self, move=move)
        self.children.append(child)
        return child

    def get_children(self):
        """Return the list of child nodes."""
        return self.children

    def get_parent(self):
        """Return the parent node."""
        return self.parent

    def is_leaf(self):
        """Return True if this node has no children."""
        return len(self.children) == 0

    def __str__(self):
        return f"GameTreeNode(move={self.move}, value={self.value}, children={len(self.children)})"

    def print_tree(self, level=0):
        """Recursively prints the tree (for debugging)."""
        indent = "  " * level
        print(f"{indent}{self}")
        for child in self.children:
            child.print_tree(level + 1)

class GameTree:
    def __init__(self, root_state):
        """
        Initialize the persistent game tree with the given root state.
        :param root_state: An instance of GameState.
        """
        self.root = GameTreeNode(root_state)

    def build_tree(self, node, depth, player_color):
        if depth == 0:
            return

        valid_moves = node.state.get_valid_plays()  # e.g., [("move", index, tile), ("place", tile), ...]
        print(valid_moves)
        for move in valid_moves:
            # Create a deep copy of the current state
            new_state = copy.deepcopy(node.state)
            move_type = move[0]
            print(move)

            if move_type == "move":
                # Movement moves: use make_move() which triggers flipping
                new_state = new_state.make_move(move)
            elif move_type == "place":
                # Placement moves: use place_piece() which does NOT trigger flipping
                new_state.place_piece(move[1], new_state.current_player)
            else:
                continue  # Skip unknown move types

            # Create a child node using this new state and record the move.
            child_node = node.add_child(new_state, move)

            # Recursively build tree from the new child node
            self.build_tree(child_node, depth - 1, player_color)

    def update_root(self, move):
        """
        After a move is played in the game, update the persistent tree so that the child node corresponding
        to that move becomes the new root. If no matching child is found, rebuild the tree from the new state.
        :param move: The move that was played.
        """
        for child in self.root.children:
            if child.move == move:
                self.root = child
                self.root.parent = None
                return
        # If no matching child is found, create a new root from the new state.
        new_state = self.root.state.make_move(move)
        self.root = GameTreeNode(new_state)

    def minimax(self, node, depth, alpha, beta, maximizingPlayer, player_color):
        """
        Perform a minimax search with alpha–beta pruning on the persistent tree.
        :param node: The current GameTreeNode.
        :param depth: The search depth.
        :param alpha: Alpha value.
        :param beta: Beta value.
        :param maximizingPlayer: True if the current level is maximizing, False if minimizing.
        :param player_color: The AI's color.
        :return: A tuple (evaluation, best_move) where best_move is stored in the node's move field.
        """
        # Terminal condition: if depth is 0 or node is a leaf.
        if depth == 0 or node.is_leaf():
            node.value = node.state.evaluate_board(last_play_was_movement=True)
            return node.value, node.move

        if maximizingPlayer:
            maxEval = -float("inf")
            best_move = None
            for child in node.children:
                eval_val, _ = self.minimax(child, depth - 1, alpha, beta, False, player_color)
                if eval_val > maxEval:
                    maxEval = eval_val
                    best_move = child.move
                alpha = max(alpha, eval_val)
                if beta <= alpha:
                    break  # Beta cutoff.
            node.value = maxEval
            return maxEval, best_move
        else:
            minEval = float("inf")
            best_move = None
            for child in node.children:
                eval_val, _ = self.minimax(child, depth - 1, alpha, beta, True, player_color)
                if eval_val < minEval:
                    minEval = eval_val
                    best_move = child.move
                beta = min(beta, eval_val)
                if beta <= alpha:
                    break  # Alpha cutoff.
            node.value = minEval
            return minEval, best_move
