class Board:
    def __init__(self):
        """
        Initialize the Backgammon board.
        """
        self.points = [None] * 24
        self.bar = {1: 0, -1: 0}
        self.off = {1: 0, -1: 0}
        self.initialize_board()

    def initialize_board(self):
        """
        Set up the board with the standard initial configuration.
        """
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
        Draw a visual representation of the Backgammon board.
        """
        def format_point(point):
            if not point:
                return " -"
            player, count = point
            symbol = "W" if player == 1 else "B"
            return f"{symbol}{count}" if count < 10 else f"{symbol}9+"

        top_row = "  ".join(f"{24 - i:>2}" for i in range(12))
        bottom_row = "  ".join(f"{i + 1:>2}" for i in range(12))
        top_points = "  ".join(format_point(self.points[23 - i]) for i in range(12))
        bottom_points = "  ".join(format_point(self.points[i]) for i in range(12))
        bar_display = f"Bar: W={self.bar[1]} B={self.bar[-1]}"
        off_display = f"Off: W={self.off[1]} B={self.off[-1]}"

        print(f"\n{'-' * 41}")
        print(f"Top Row Points (Black Home):\n{top_row}\n{top_points}")
        print(f"\n{bar_display}\n{off_display}")
        print(f"\nBottom Row Points (White Home):\n{bottom_points}\n{bottom_row}")
        print(f"{'-' * 41}\n")

    def is_valid_move(self, player, start, end):
        """
        Validate if a move is allowed.
        """
        # Moving from the bar
        if start == 999:
            if self.bar[player] <= 0:
                return False
            if player == 1 and not (0 <= end <= 5):
                return False
            if player == -1 and not (17 <= end <= 23):
                print("returning false end is not between 17 and 23")
                return False

        # Moving from the board
        elif self.points[start] is None or self.points[start][0] != player:
            return False

        # If moving to an occupied point
        if self.points[end]:
            target_player, target_count = self.points[end]
            if target_player != player and target_count > 1:
                print("retrning false, point {self.points[end]} is taken")
                return False

        return True

    def move(self, player, start, end):
        """
        Execute a move for the player.
        """
        if not self.is_valid_move(player, start, end):
            raise ValueError("Invalid move")
        count = self.points[start][1]
        self.points[start] = None if count == 1 else (player, count - 1)
        if end < 24:
            if self.points[end] is None:
                self.points[end] = (player, 1)
            elif self.points[end][0] == player:
                self.points[end] = (player, self.points[end][1] + 1)
            else:
                self.bar[-player] += 1
                self.points[end] = (player, 1)
        else:
            self.off[player] += 1

    def can_bear_off(self, player):
        """
        Check if the player can bear off.
        """
        home_range = range(0, 6) if player == 1 else range(18, 24)
        for i in range(24):
            if self.points[i] and self.points[i][0] == player:
                if i not in home_range:
                    return False
        return True
