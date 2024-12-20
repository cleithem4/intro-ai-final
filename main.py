from alphabeta import PlayerAB
from minimax import PlayerMM
from game import Game

if __name__ == "__main__":
    from random import seed

    # Optional: Seed random number generator for reproducible results
  
    seed(212)

    # Initialize players
    player1 = PlayerAB(max_depth=2)  # AI using Alpha-Beta Pruning with depth 2
    player2 = PlayerAB(max_depth=4)  # AI using Alpha-Beta Pruning with depth 4

    # Create and start the game
    game = Game(player1, player2)
    game.play()