from board import BoardState

from board import BoardUtils

import random

class Evaluator:
    @staticmethod
    def evaluate_board(state, is_white_turn):
        """
        A heuristic evaluation function. Customize as needed.
        """
        white_score = sum(state.get_counts_array()[:12])
        black_score = sum(state.get_counts_array()[12:])
        return white_score - black_score if is_white_turn else black_score - white_score


class MoveUtils:
    @staticmethod
    def get_all_possible_moves(board_state, dice_rolls, is_white_turn):
        """
        Generate all possible legal moves for the current player.
        Returns a list of (new_board_state, move) tuples.
        """
        moves = []
        for roll in dice_rolls:
            for i in range(BoardUtils.BOARD_SIZE):
                if (is_white_turn and board_state.is_position_white(i)) or (not is_white_turn and board_state.is_position_black(i)):
                    new_state = BoardUtils.get_board_after_moving_single_piece(board_state, i, roll)
                    moves.append((new_state, (i, roll)))
        return moves

class BackgammonAI:
    MAX_DEPTH = 3

    @staticmethod
    def alpha_beta_search(board_state, depth, alpha, beta, maximizing_player, is_white_turn):
        if depth == 0 or BackgammonAI.is_terminal_state(board_state):
            return Evaluator.evaluate_board(board_state, is_white_turn), None

        best_move = None
        if maximizing_player:
            max_eval = float('-inf')
            moves = MoveUtils.get_all_possible_moves(board_state, [1, 2, 3, 4, 5, 6], is_white_turn)
            for new_state, move in moves:
                eval_score, _ = BackgammonAI.alpha_beta_search(new_state, depth - 1, alpha, beta, False, is_white_turn)
                if eval_score > max_eval:
                    max_eval = eval_score
                    best_move = move
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break
            return max_eval, best_move
        else:
            min_eval = float('inf')
            moves = MoveUtils.get_all_possible_moves(board_state, [1, 2, 3, 4, 5, 6], not is_white_turn)
            for new_state, move in moves:
                eval_score, _ = BackgammonAI.alpha_beta_search(new_state, depth - 1, alpha, beta, True, is_white_turn)
                if eval_score < min_eval:
                    min_eval = eval_score
                    best_move = move
                beta = min(beta, eval_score)
                if beta <= alpha:
                    break
            return min_eval, best_move

    @staticmethod
    def is_terminal_state(board_state):
        """
        #Checks if the game is in a terminal state (win/loss condition).
        #Customize according to Backgammon's rules.
        """
        return board_state.get_num_dead(True) == board_state.NUM_PIECES or board_state.get_num_dead(False) == board_state.NUM_PIECES

    @staticmethod
    def find_best_move(board_state, is_white_turn):
        _, best_move = BackgammonAI.alpha_beta_search(board_state, BackgammonAI.MAX_DEPTH, float('-inf'), float('inf'), True, is_white_turn)
        return best_move


# Example of running the AI
if __name__ == "__main__":
    starting_board = BoardUtils.get_starting_position_board()
    print("Starting board:")
    print(starting_board)

    ai_move = BackgammonAI.find_best_move(starting_board, is_white_turn=True)
    print(f"AI recommends move: {ai_move}")
