from board import BoardUtils
from backgammon_ai import BackgammonAI

def run_game():
    # Initialize the board
    board_state = BoardUtils.get_starting_position_board()
    is_white_turn = True

    print("Starting Board:")
    print(board_state)

    while not BackgammonAI.is_terminal_state(board_state):
        print(f"\n{'White' if is_white_turn else 'Black'}'s turn:")
        best_move = BackgammonAI.find_best_move(board_state, is_white_turn)

        if best_move:
            print(f"Best move chosen: {best_move}")
            board_state = BoardUtils.get_board_after_moving_single_piece(
                board_state, best_move[0], best_move[1]
            )
        else:
            print(f"No legal moves for {'White' if is_white_turn else 'Black'}.")

        print(board_state)
        is_white_turn = not is_white_turn

    print("\nGame Over!")
    if board_state.get_num_dead(True) == BoardUtils.NUM_PIECES:
        print("White wins!")
    elif board_state.get_num_dead(False) == BoardUtils.NUM_PIECES:
        print("Black wins!")

if __name__ == "__main__":
    run_game()
