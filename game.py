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
        """Calculate all possible moves for the current player based on dice rolls."""
        self.moves = []
        
        # Check if the player has checkers on the bar
        if self.board.bar[self.current_player] > 0:
            for die in self.dice:
                # Determine valid end points for moves from the bar
                if self.current_player == 1:
                    valid_end = die - 1  # Points 1-6 in game notation (0-5 in array indexing)
                else:
                    valid_end = 24 - die  # Points 19-24 in game notation (23-(6-die) in indexing)

                # Only add moves that are valid
                if self.board.is_valid_move(self.current_player, 999, valid_end):
                    self.moves.append((999, valid_end))
            return  # Return early as moves from the bar are the only allowed moves

        # If no checkers on the bar, calculate normal moves
        for die in self.dice:
            for start in range(24):
                # Only consider points with the current player's checkers
                if self.board.points[start] and self.board.points[start][0] == self.current_player:
                    end = start + die * self.current_player

                    # Check if the move is within bounds and valid
                    if 0 <= end < 24 and self.board.is_valid_move(self.current_player, start, end):
                        self.moves.append((start, end))

        # Handle bearing off
        if self.board.can_bear_off(self.current_player):
            for die in self.dice:
                for start in range(24):
                    # Check if the checker is in the home board
                    if self.board.points[start] and self.board.points[start][0] == self.current_player:
                        end = start + die * self.current_player
                        
                        # Valid end point for bearing off is 24 (off-board)
                        if end == 24 or (end > 23 if self.current_player == -1 else end < 0):
                            if self.board.is_valid_move(self.current_player, start, 24):
                                self.moves.append((start, 24))




    def apply_move(self, start, end):
        """Apply a move from start to end."""
        distance = abs(end - start)
        if start == 999:  # Moving from the bar
            self.board.bar[self.current_player] -= 1
            self.board.points[end] = (self.current_player, 1)
        elif end == 24:  # Bearing off
            if self.board.can_bear_off(self.current_player):
                self.board.move(self.current_player, start, end)
                print(f"Player {'White' if self.current_player == 1 else 'Black'} bore off a checker!")
            else:
                raise ValueError("Cannot bear off: Not all checkers are in the home board.")
        else:  # Normal move
            if distance in self.dice:
                self.board.move(self.current_player, start, end)
                self.dice.remove(distance)  # Decrement the used die
                print(f"Moved from {start + 1} to {end + 1}")
            else:
                raise ValueError("Invalid move: Dice value does not match.")



    def check_winner(self):
        """
        Check if the current player has borne off all their checkers.
        :return: 1 for White win, -1 for Black win, None otherwise
        """
        if self.board.off[self.current_player] == 15:
            return self.current_player
        return None


    def play_turn(self):
        """Execute a single turn for the current player."""
        self.roll_dice()
        self.calculate_moves()

        # Check if there are no moves available initially
        if not self.moves:
            print(f"No moves available for Player {'White' if self.current_player == 1 else 'Black'}.")
            self.current_player *= -1  # Switch to the next player
            return False  # End the turn immediately

        # While there are moves and dice left
        while self.moves and self.dice:
            print(f"Player {'White' if self.current_player == 1 else 'Black'}, it's your turn!")
            self.board.display()
            moves_display = [
                (start + 1 if start != 999 else "Bar", end + 1 if end != 24 else "Off")
                for start, end in self.moves
            ]
            print(f"Available moves: {moves_display}")

            if self.current_player == 1:  # Human (White)
                try:
                    if self.board.bar[self.current_player] > 0:
                        print("You have checkers on the bar. You must move one of them.")
                        start = 999
                        end = int(input("Enter the ending point (1-24): ")) - 1
                        self.apply_move(start, end)
                    else:
                        start = int(input("Enter the starting point (1-24): ")) - 1
                        end = int(input("Enter the ending point (1-24 or 24 for bearing off): ")) - 1
                        self.apply_move(start, end)

                    # Recalculate moves after applying one
                    self.calculate_moves()
                    if not self.moves:  # Check again after applying a move
                        print(f"No more moves available for Player {'White' if self.current_player == 1 else 'Black'}.")
                        break
                except ValueError as e:
                    print(f"Error: {e}")
            else:  # AI (Black)
                self.ai_move()
                self.calculate_moves()

        # Check for winner after all moves
        winner = self.check_winner()
        if winner:
            print(f"Player {'White' if winner == 1 else 'Black'} wins!")
            return True

        # Switch player turn
        self.current_player *= -1
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

