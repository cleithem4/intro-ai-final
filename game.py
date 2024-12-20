from board import Board

class Game:
    def __init__(self, player1, player2):
        self.board = Board()
        self.player1 = player1
        self.player2 = player2

    def play(self):
        while not self.board.is_game_over():
            current_player = self.player1 if self.board.turn == 0 else self.player2

            # Roll dice at the start of the turn
            self.board.roll_dice()
            print(f"Player {self.board.turn + 1}'s turn. Dice rolled: {self.board.dice}")
            #self.board.display_board()  # Show the board before the player's move

            # Get the current player's move
            move = current_player.findMove(self.board)
            if move:
                self.board.apply_move(move)
                print(f"Player {self.board.turn + 1} chose move: {move}")
                #self.board.display_board()  # Show the updated board
            else:
                print(f"No valid moves for Player {self.board.turn + 1}")
            
            # Switch turn
            self.board.turn = 1 - self.board.turn

        # End of game
        winner = self.board.evaluate_winner()
        if winner == 0:
            print("Player 1 wins!")
        elif winner == 1:
            print("Player 2 wins!")
        else:
            print("It's a draw!")

