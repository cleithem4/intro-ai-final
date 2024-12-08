from alphabeta import PlayerAB
from minimax import PlayerMM
from game import Game

if __name__ == "__main__":
    from random import seed

    # Optional: Seed random number generator for reproducible results
    seed(3532535)

    # Initialize players
    player1 = PlayerMM(max_depth=4)  # AI using Alpha-Beta Pruning
    player2 = PlayerAB(max_depth=3)  # AI using MiniMax

    # Create and start the game
    game = Game(player1, player2)
    game.play()