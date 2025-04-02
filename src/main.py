from game.game import Game
import argparse
import numpy as np
import random
import os
from utils.logs import save_beliefs

def main(Players = [2, 10], verbose=False, seed=None, log_dir='logs', save_logs=True):
    """
    Run a complete werewolf game simulation.
    
    ARGUMENTS:
    Players: list of integers, number of players in each team.
    Team 1: Werewolves
    Team 2: Villagers
    verbose: bool, whether to print detailed game progress
    seed: int, random seed for reproducibility (optional)
    log_dir: str, directory to save belief logs
    save_logs: bool, whether to save belief logs
    
    RETURNS:
    dict: Game statistics
    """
    # Generate random seed if none provided
    if seed is None:
        seed = random.randint(0, 999999)
        if verbose:
            print(f"Using random seed: {seed}")
            
    # Initialize game
    if save_logs:
        os.makedirs(log_dir, exist_ok=True)
    game = Game(num_villagers=Players[1], num_wolves=Players[0], seed=seed, update_params=[0.15, 0.15, 0.2, 0.3])
    # Log initial beliefs
    if save_logs:
        save_beliefs(game, 0)

    # Game stats
    stats = {
        'rounds': 0,
        'winner': None,
        'initial_wolves': Players[0],
        'initial_villagers': Players[1]
    }
    
    # Game loop
    while True:
        if verbose:
            print(f"\n=== Round {stats['rounds'] + 1} ===")
            print(f"Night phase - {game.get_wolves_count()} werewolves, {game.get_villagers_count()} villagers")
        
        # Night phase
        eliminated_night = game.night_shift()
        if verbose:
            print(f"🌙 Werewolves eliminated villager {eliminated_night}")
        
        # Check win condition after night
        winner = game.check_game_over()
        if winner:
            stats['winner'] = winner
            break
            
        if verbose:
            print(f"Day phase - {game.get_wolves_count()} werewolves, {game.get_villagers_count()} villagers")
        
        # Day phase
        eliminated_day, target_type = game.day_shift()
        if verbose:
            print(f"☀️ Village eliminated player {eliminated_day} who was a {target_type} !")
        
        # Save beliefs after each round
        if save_logs:
            save_beliefs(game, stats['rounds'] + 1, log_dir=log_dir)

        # Check win condition after day
        winner = game.check_game_over()
        if winner:
            stats['winner'] = winner
            break
            
        stats['rounds'] += 1
    
    if verbose:
        print("\n=== Game Over ===")
        print(f"Game ended after {stats['rounds']+1} rounds")
        print(f"Winner: {stats['winner']}")
        print(f"Remaining villagers: {game.get_villagers_count()}")
        print(f"Remaining werewolves: {game.get_wolves_count()}")
    
    return stats

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run a Werewolf game simulation.')
    parser.add_argument('--verbose', '-v', action='store_true', help='Print detailed game progress')
    parser.add_argument('--seed', type=int, help='Random seed for reproducibility', default=None)
    parser.add_argument('--log_dir', type=str, help='Directory to save belief logs', default='logs')
    parser.add_argument('--save_logs', '-s', action='store_true', help='Save belief logs', default=False)
    args = parser.parse_args()
    
    main(verbose=args.verbose, seed=args.seed, log_dir=args.log_dir, save_logs=args.save_logs)