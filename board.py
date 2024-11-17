class Board:
    def __init__(self):
        """
        Initialize the backgammon board.
        The board is represented as a list of 24 points.
        Each point contains a tuple (player, count) where:
        - player: 1 or -1 (representing the two players)
        - count: the number of checkers on that point
        """
        self.points = [None] * 24
        self.bar = {1: 0, -1: 0}  # Captured checkers for each player
        self.off = {1: 0, -1: 0}  # Checkers borne off for each player

        # Standard initial configuration
        self.points[0] = (1, 2)
        self.points[5] = (-1, 5)
        self.points[7] = (-1, 3)
        self.points[11] = (1, 5)
        self.points[12] = (-1, 5)
        self.points[16] = (1, 3)
        self.points[18] = (1, 5)
        self.points[23] = (-1, 2)

    def display(self):
        """
        Draws a visual representation of the Backgammon board.
        """
        def format_point(point):
            """Helper to format a point with checkers."""
            if not point:
                return " -"
            player, count = point
            symbol = "W" if player == 1 else "B"
            return f"{symbol}{count}" if count < 10 else f"{symbol}9+"

        top_row = "  ".join(f"{24 - i:>2}" for i in range(12))  # Point numbers for the top row
        bottom_row = "  ".join(f"{i + 1:>2}" for i in range(12))  # Point numbers for the bottom row

        # Format the points for both rows
        top_points = "  ".join(format_point(self.points[23 - i]) for i in range(12))
        bottom_points = "  ".join(format_point(self.points[i]) for i in range(12))

        # Display bar and off counters
        bar_display = f"Bar: W={self.bar[1]} B={self.bar[-1]}"
        off_display = f"Off: W={self.off[1]} B={self.off[-1]}"

        # Print the board representation
        print(f"\n{'-' * 41}")
        print(f"Top Row Points (Black Home):")
        print(f"{top_row}")
        print(f"{top_points}")
        print(f"\n{bar_display}")
        print(f"{off_display}")
        print(f"\nBottom Row Points (White Home):")
        print(f"{bottom_points}")
        print(f"{bottom_row}")
        print(f"{'-' * 41}\n")

    def is_valid_move(self, player, start, end):
        """
        Check if a move is valid.
        :param player: The current player (1 or -1)
        :param start: The starting point (0-indexed or 999 for the bar)
        :param end: The ending point (0-indexed)
        :return: True if the move is valid, False otherwise
        """
        # Ensure start is either valid index (0-23) or the bar (999)
        if not (start == 999 or (0 <= start < 24)):
            return False  # Invalid start point

        # Ensure end is within valid points (0-23)
        if not (0 <= end < 24):
            return False  # Invalid end point

        if start != 999 and (self.points[start] is None or self.points[start][0] != player):
            return False  # Starting point doesn't belong to the player

        if self.bar[player] > 0 and start != 999:
            return False  # Player must move from the bar if they have checkers on the bar

        # Player moving from the bar
        if self.bar[player] > 0:
            if player == 1:
                # White player (1) can only move to points 0-5 (1-6 in Backgammon)
                if not (0 <= end <= 5):
                    return False
            elif player == -1:
                # Black player (-1) can only move to points 17-23 (18-24 in Backgammon)
                if not (17 <= end <= 23):
                    return False

        # Normal move (not from the bar)
        if not (self.bar[player] > 0) and end < 24:  # Not bearing off
            if self.points[end] is None:
                return True  # Ending point is empty
            if self.points[end][0] == player:
                return True  # Ending point has player's checkers
            if self.points[end][1] == 1:
                return True  # Ending point has one opponent checker (can hit)
        else:  # Bearing off
            return self.can_bear_off(player)

        return False




    def move(self, player, start, end):
        """
        Execute a move.
        :param player: The current player (1 or -1)
        :param start: The starting point (0-indexed)
        :param end: The ending point (0-indexed or 24 for off-board)
        """
        if not self.is_valid_move(player, start, end):
            raise ValueError("Invalid move")

        count = self.points[start][1]
        if count == 1:
            self.points[start] = None  # Remove last checker
        else:
            self.points[start] = (player, count - 1)  # Decrease checker count

        if end < 24:
            if self.points[end] is None:
                self.points[end] = (player, 1)  # Place checker on empty point
            elif self.points[end][0] == player:
                self.points[end] = (player, self.points[end][1] + 1)  # Stack checkers
            else:
                self.bar[-player] += 1  # Hit opponent checker
                self.points[end] = (player, 1)  # Place checker
        else:
            self.off[player] += 1  # Bear off

    def can_bear_off(self, player):
        """
        Check if the player is allowed to bear off checkers.
        :param player: The current player (1 or -1)
        :return: True if bearing off is allowed, False otherwise
        """
        # Ensure all checkers are in the home quadrant
        start = 0 if player == 1 else 18
        end = 6 if player == 1 else 24
        for i in range(start, end):
            if self.points[i] and self.points[i][0] == player:
                return False
        return True
