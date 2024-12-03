class Player:
    def __init__(self, name, player_id):
        """
        Initialize a Player.
        """
        self.name = name
        self.id = player_id
        self.off_checkers = 0

    def __str__(self):
        """
        String representation of the player.
        """
        return f"Player {self.name} ({'White' if self.id == 1 else 'Black'})"
