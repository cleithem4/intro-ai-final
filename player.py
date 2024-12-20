class BasePlayer:
    def __init__(self, max_depth=3):
        self.max_depth = max_depth
        self.resolved = {}

    def heuristic(self, board):
        # Points for pieces borne off (bearing off more pieces is better)
        borne_off_score = (board.off[1] - board.off[0]) * 20  # Increased weight for bearing off

        # Points for pieces on the bar (fewer pieces on the bar is better)
        bar_score = (board.bar[0] - board.bar[1]) * 15

        # Points for blocking and primes (encourage prime formation and avoid being blocked)
        blocker_score = 0
        for point in range(24):
            if board.p1_pieces[point] == 1:  # Player 1 single checker
                blocker_score -= 5
            if board.p2_pieces[point] == 1:  # Player 2 single checker
                blocker_score += 5

            # Prime points
            if board.p2_pieces[point] > 1:
                consecutive_count = 0
                while point + consecutive_count < 24 and board.p2_pieces[point + consecutive_count] > 0:
                    consecutive_count += 1
                if consecutive_count >= 4:  # Forming a prime
                    blocker_score += 10

        # Encourage control of Player 2's home board
        home_board_score = 0
        for point in range(0, 6):
            home_board_score += board.p2_pieces[point] * 10  # Higher weight for home board control

        # Penalty for stranded pieces outside home board
        stranded_penalty = 0
        for point in range(6, 24):
            if board.p2_pieces[point] == 1:
                stranded_penalty += 15 * (24 - point)  # Encourage moving toward home board

        # Final heuristic score: combine all the factors
        return (
            borne_off_score + bar_score + blocker_score + home_board_score - stranded_penalty
        )

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