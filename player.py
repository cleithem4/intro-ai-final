class BasePlayer:
    def __init__(self, max_depth=3):
        self.max_depth = max_depth
        self.resolved = {}

    def heuristic(self, board):
        # Points for pieces borne off (the more pieces borne off, the better)
        borne_off_score = (board.off[0] - board.off[1]) * 10

        # Points for pieces on the bar (the fewer pieces on the bar, the better)
        bar_score = (board.bar[1] - board.bar[0]) * 15

        # Points for blocking (the fewer block points, the better)
        blocker_score = 0
        for point in range(24):
            if board.checkers[point] == 1:  # 1 means a single checker on this point
                blocker_score -= 5  # Penalize for block points (pieces that are alone and vulnerable)

        # Points for prime points (more prime points are better)
        prime_score = 0
        for point in range(24):
            if board.checkers[point] > 1:
                # Add points for a sequence of consecutive points occupied by the same player
                consecutive_count = 0
                while point + consecutive_count < 24 and board.checkers[point + consecutive_count] > 0:
                    consecutive_count += 1
                if consecutive_count >= 4:  # 4 or more consecutive points is a prime
                    prime_score += 10

        # Points for controlling the home board (points 18-24 for player 0)
        home_board_score = 0
        for point in range(18, 24):
            if board.checkers[point] > 0:
                home_board_score += 5  # Reward controlling the home board

        # Final heuristic score: combine all the factors
        return borne_off_score - bar_score + blocker_score + prime_score + home_board_score


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