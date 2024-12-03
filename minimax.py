from player import BasePlayer

class PlayerMM(BasePlayer):
    def findMove(self, board):
        best_move = None
        best_value = float('-inf') if board.turn == 0 else float('inf')

        # Get all valid moves for the current player
        valid_moves = board.get_valid_moves(board.turn)

        for move in valid_moves:
            board.apply_move(move)
            # Use the minimax algorithm to evaluate this move
            value = self.minimax(board, self.max_depth - 1, board.turn == 1)
            board.undo_move(move)

            # Update the best move based on the maximizing or minimizing player
            if board.turn == 0 and value > best_value:  # Maximizing for Player 1
                best_value = value
                best_move = move
            elif board.turn == 1 and value < best_value:  # Minimizing for Player 2
                best_value = value
                best_move = move

        return best_move

    def minimax(self, board, depth, maximizing_player):
        if depth == 0 or board.is_game_over():
            return self.heuristic(board)

        valid_moves = board.get_valid_moves(board.turn)
        if maximizing_player:
            max_eval = float('-inf')
            for move in valid_moves:
                board.apply_move(move)
                eval = self.minimax(board, depth - 1, False)
                board.undo_move(move)
                max_eval = max(max_eval, eval)
            return max_eval
        else:
            min_eval = float('inf')
            for move in valid_moves:
                board.apply_move(move)
                eval = self.minimax(board, depth - 1, True)
                board.undo_move(move)
                min_eval = min(min_eval, eval)
            return min_eval
