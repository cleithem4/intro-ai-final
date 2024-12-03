import random
from board import Board
from player import Player

class Game:
    def __init__(self):
        """
        Initialize the game.
        """
        self.board = Board()
        self.players = [Player("White", 1), Player("Black", -1)]
        self.current_player = self.players[0]
        self.dice = []

    def roll_dice(self):
        """
        Roll the dice for the current player.
        """
        self.dice = [random.randint(1, 6), random.randint(1, 6)]
        if self.dice[0] == self.dice[1]:
            self.dice *= 2
        print(f"{self.current_player} rolled: {self.dice}")

    def calculate_moves(self):
        """
        Calculate all valid moves for the current player.
        """
        moves = []
        player_id = self.current_player.id

        # Check if the player has checkers on the bar
        if self.board.bar[player_id] > 0:
            for die in self.dice:
                if player_id == 1:
                    # White moves from the bar to points 0-5 (indexing: 0-5)
                    end = die - 1
                else:
                    # Black moves from the bar to points 18-23 (indexing: 18-23)
                    end = 24 - die

                if 0 <= end < 24 and self.board.is_valid_move(player_id, 999, end):
                    moves.append((999, end))
            return moves  # Bar moves take priority

        # Generate normal moves
        for start in range(24):
            if self.board.points[start] and self.board.points[start][0] == player_id:
                for die in self.dice:
                    end = start + die * (1 if player_id == 1 else -1)
                    if 0 <= end < 24 and self.board.is_valid_move(player_id, start, end):
                        moves.append((start, end))

        # Generate bearing-off moves
        if self.board.can_bear_off(player_id):
            for start in range(24):
                if self.board.points[start] and self.board.points[start][0] == player_id:
                    for die in self.dice:
                        end = start + die * (1 if player_id == 1 else -1)
                        if (player_id == 1 and end >= 24) or (player_id == -1 and end < 0):
                            if self.board.is_valid_move(player_id, start, 24):
                                moves.append((start, 24))
        return moves


    def play_turn(self):
        """
        Play a single turn for the current player.
        """
        self.roll_dice()
        moves = self.calculate_moves()
        if not moves:
            print(f"No valid moves for {self.current_player}.")
            self.switch_player()
            return False

        for move in moves:
            print(f"Move: {move}")
            self.board.move(self.current_player.id, *move)
            self.dice.remove(abs(move[1] - move[0]))

        if self.board.off[self.current_player.id] == 15:
            print(f"{self.current_player} wins!")
            return True
        self.switch_player()
        return False

    def switch_player(self):
        """
        Switch to the next player.
        """
        self.current_player = self.players[1] if self.current_player == self.players[0] else self.players[0]

    def play_game(self):
        """
        Start the game loop.
        """
        print("Starting Backgammon!")
        self.board.display()
        while True:
            if self.play_turn():
                break
            self.board.display()
