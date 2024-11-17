import random
from board import Board

class Game:
    def __init__(self):
        """Initialize the game with a board and player-specific attributes."""
        self.board = Board()
        self.current_player = 1  # 1 for white, -1 for black
        self.dice = []  # Stores the dice rolls
        self.moves = []  # Stores the possible moves for the turn

    def roll_dice(self):
        """Roll two dice at the start of a player's turn."""
        self.dice = [random.randint(1, 6), random.randint(1, 6)]
        if self.dice[0] == self.dice[1]:  # Handle doubles
            self.dice.extend(self.dice)
        print(f"Player {'White' if self.current_player == 1 else 'Black'} rolled: {self.dice}")

    def calculate_moves(self):
        #"""Calculate all possible moves for the current player based on dice rolls."""
        self.moves = []
        if self.board.bar[self.current_player] > 0:
            # If the player has checkers on the bar, they can only move those checkers
            for die in self.dice:
                for start in [999]:  # The starting point for pieces on the bar is 999
                    if self.current_player == 1:
                        # White player (1) can only move to points 0-5 (1-6)
                        valid_ends = range(0, 6)  # Points 1 to 6
                    else:
                        # Black player (-1) can only move to points 17-23 (18-24)
                        valid_ends = range(17, 24)  # Points 18 to 24
                    
                    for end in valid_ends:
                        if self.board.is_valid_move(self.current_player, start, end):
                            self.moves.append((start, end))
        else:
            # Normal moves for when there are no checkers on the bar
            for die in self.dice:
                for start in range(24):
                    if self.board.points[start] and self.board.points[start][0] == self.current_player:
                        end = start + die * self.current_player
                        if self.board.is_valid_move(self.current_player, start, end):
                            self.moves.append((start, end))


    def apply_move(self, start, end):
        """Apply a move from start to end."""
        if start == 999:  # Moving from the bar
            self.board.bar[self.current_player] -= 1  # Move a checker off the bar
            self.board.points[end] = (self.current_player, 1)  # Place the checker on the point
        else:
            distance = abs(end - start)
            if distance in self.dice:
                self.board.move(self.current_player, start, end)
                self.dice.remove(distance)  # Remove the used dice roll
                print(f"Moved from {start + 1} to {end + 1}")
            else:
                raise ValueError("Invalid move: Dice value does not match.")

    def check_winner(self):
        """Check if the current player has borne off all their checkers."""
        if self.board.off[self.current_player] == 15:
            return self.current_player
        return None

    def play_turn(self):
        """Execute a single turn for the current player."""
        self.roll_dice()
        self.calculate_moves()
        
        
        while self.moves:
            print(f"Player {'White' if self.current_player == 1 else 'Black'}, it's your turn!")
            self.board.display()
            moves_display = [(start + 1, end + 1) for start, end in self.moves]
            print(f"Available moves: {moves_display}")

            if self.current_player == 1:
                # White player's turn (human)
                try:
                    if self.board.bar[self.current_player] > 0:
                        # If there are checkers on the bar, the player can only move them
                        print("You have checkers on the bar. You must move one of them.")
                        start = 999  # Always start from the bar
                        end = int(input("Enter the ending point (1-24): ")) - 1  # User input for where to move
                        self.apply_move(start, end)
                    else:
                        # If no checkers on the bar, normal moves are available
                        start = int(input("Enter the starting point (1-24): ")) - 1
                        end = int(input("Enter the ending point (1-24 or 24 for bearing off): ")) - 1
                        self.apply_move(start, end)
                    self.calculate_moves()  # Recalculate moves after applying the move
                except ValueError as e:
                    print(f"Error: {e}")
            else:
                # Black player's turn (AI)
                self.ai_move()
                self.calculate_moves()  # Recalculate moves after AI move

        winner = self.check_winner()
        if winner:
            print(f"Player {'White' if winner == 1 else 'Black'} wins!")
            return True

        self.current_player *= -1  # Switch player turn
        return False

    def ai_move(self):
        """AI for Black: Randomly select a valid move."""
        # Randomly select a move from the available moves
        if self.moves:
            move = random.choice(self.moves)
            start, end = move
            self.apply_move(start, end)
            print(f"AI (Black) moves from {start + 1} to {end + 1}")

    def play_game(self):
        """Start the game loop and alternate player turns until a winner is found."""
        print("Welcome to Backgammon!")
        self.board.display()

        while True:
            if self.play_turn():
                break
        print("Game over!")

