class Board:
    def __init__(self):
        # Initialize the board with standard Backgammon starting positions
        self.p1_pieces = [0] * 24
        self.p2_pieces = [0] * 24

        # Set starting positions for Player 1
        self.p1_pieces[0] = 2
        self.p1_pieces[11] = 5
        self.p1_pieces[16] = 3
        self.p1_pieces[18] = 5

        # Set starting positions for Player 2
        self.p2_pieces[23] = 2
        self.p2_pieces[12] = 5
        self.p2_pieces[7] = 3
        self.p2_pieces[5] = 5

        # Initialize bar and off positions
        self.bar = [0, 0]
        self.off = [0, 0]

        # Player 1 starts the game
        self.turn = 0
        self.dice = []        
    def roll_dice(self):
        from random import randint
        self.dice = [randint(1, 6), randint(1, 6)]
    def get_valid_moves(self, player):
        moves = []
        pieces = self.p1_pieces if player == 0 else self.p2_pieces
        opponent_pieces = self.p2_pieces if player == 0 else self.p1_pieces
        bar_pieces = self.bar[player]

        # Check if all pieces are in the home board
        if player == 0:
            in_home = all(pieces[i] == 0 for i in range(0, 18))
        else:
            in_home = all(pieces[i] == 0 for i in range(6, 24))


        # If there are pieces on the bar, only allow moves to bring them in
        if bar_pieces > 0:
            for roll in self.dice:
                target = roll - 1 if player == 0 else 24 - roll
                if 0 <= target < 24 and opponent_pieces[target] <= 1:
                    moves.append(("bar", target))
            return moves

        # Normal moves
        for i in range(24):
            if pieces[i] > 0:
                for roll in self.dice:
                    target = i + roll if player == 0 else i - roll
                    if 0 <= target < 24 and opponent_pieces[target] <= 1:
                        moves.append((i, target))

        # Bear-off moves (only if all pieces are in home board)
        if in_home:
            home_start = 18 if player == 0 else 0
            home_end = 24 if player == 0 else 6
            for i in range(home_start, home_end):
                if pieces[i] > 0:
                    moves.append((i, "off"))

        return moves


    def apply_move(self, move):
        source, target = move
        player = self.turn
        pieces = self.p1_pieces if player == 0 else self.p2_pieces

        # Handle moving from the bar
        if source == "bar":
            pieces[target] += 1
            self.bar[player] -= 1

        # Handle bearing off
        elif target == "off":
            if player == 0:
                in_home = all(pieces[i] == 0 for i in range(0, 18))  # Player 1's home check
            else:
                in_home = all(pieces[i] == 0 for i in range(6, 24))  # Player 2's home check

            if in_home:
                pieces[source] -= 1
                self.off[player] += 1
            else:
                raise ValueError("Invalid move: Cannot bear off unless all pieces are in home board.")

        # Normal move
        else:
            pieces[source] -= 1
            pieces[target] += 1



    def undo_move(self, move):
        # Undo a move by reversing the apply_move logic
        target, source = move[::-1]
        player = self.turn
        pieces = self.p1_pieces if player == 0 else self.p2_pieces
        opponent_pieces = self.p2_pieces if player == 0 else self.p1_pieces

        # Handle undoing a move from the bar
        if source == "bar":
            pieces[target] -= 1
            self.bar[player] += 1
            if opponent_pieces[target] == 0 and self.bar[1 - player] > 0:
                opponent_pieces[target] = 1
                self.bar[1 - player] -= 1
        elif target == "off":
            pieces[source] += 1
            self.off[player] -= 1
        else:
            pieces[target] -= 1
            pieces[source] += 1
            if opponent_pieces[target] == 0 and self.bar[1 - player] > 0:
                opponent_pieces[target] = 1
                self.bar[1 - player] -= 1

    def is_game_over(self):
        return self.off[0] == 15 or self.off[1] == 15

    def evaluate_winner(self):
        if self.off[0] == 15:
            return 0  # Player 1 wins
        elif self.off[1] == 15:
            return 1  # Player 2 wins
        return -1  # Game is not over
