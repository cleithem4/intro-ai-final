class BasePlayer:
    def __init__(self, max_depth=3):
        self.max_depth = max_depth
        self.resolved = {}

    def heuristic(self, board):
        # Example heuristic: difference in borne-off pieces and pieces on the bar
        return (board.off[0] - board.off[1]) * 10 - (board.bar[0] - board.bar[1]) * 5

    def findMove(self, board):
        raise NotImplementedError("This method should be implemented in subclasses.")
"""
class PlayerMM(BasePlayer):
    def findMove(self, board):
        best_move = None
        best_value = float('-inf') if board.turn == 0 else float('inf')
        for move in board.get_valid_moves(board.turn):
            board.apply_move(move)
            value = self.minimax(board, self.max_depth - 1, board.turn == 1)
            board.undo_move(move)
            if (board.turn == 0 and value > best_value) or (board.turn == 1 and value < best_value):
                best_value = value
                best_move = move
        return best_move

    def minimax(self, board, depth, minimizing_player):
        if depth == 0 or board.is_game_over():
            return self.heuristic(board)

        if minimizing_player:
            min_eval = float('inf')
            for move in board.get_valid_moves(board.turn):
                board.apply_move(move)
                eval = self.minimax(board, depth - 1, False)
                board.undo_move(move)
                min_eval = min(min_eval, eval)
            return min_eval
        else:
            max_eval = float('-inf')
            for move in board.get_valid_moves(board.turn):
                board.apply_move(move)
                eval = self.minimax(board, depth - 1, True)
                board.undo_move(move)
                max_eval = max(max_eval, eval)
            return max_eval
"""