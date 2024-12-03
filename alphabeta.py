from minimax import PlayerMM

class PlayerAB(PlayerMM):
    def findMove(self, board):
        best_move = None
        best_value = float('-inf') if board.turn == 0 else float('inf')
        alpha = float('-inf')
        beta = float('inf')
        for move in board.get_valid_moves(board.turn):
            board.apply_move(move)
            value = self.alphaBeta(board, self.max_depth - 1, alpha, beta, board.turn == 1)
            board.undo_move(move)
            if (board.turn == 0 and value > best_value) or (board.turn == 1 and value < best_value):
                best_value = value
                best_move = move
            if board.turn == 0:
                alpha = max(alpha, value)
            else:
                beta = min(beta, value)
            if beta <= alpha:
                break
        return best_move

    def alphaBeta(self, board, depth, alpha, beta, minimizing_player):
        if depth == 0 or board.is_game_over():
            return self.heuristic(board)

        if minimizing_player:
            min_eval = float('inf')
            for move in board.get_valid_moves(board.turn):
                board.apply_move(move)
                eval = self.alphaBeta(board, depth - 1, alpha, beta, False)
                board.undo_move(move)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval
        else:
            max_eval = float('-inf')
            for move in board.get_valid_moves(board.turn):
                board.apply_move(move)
                eval = self.alphaBeta(board, depth - 1, alpha, beta, True)
                board.undo_move(move)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
