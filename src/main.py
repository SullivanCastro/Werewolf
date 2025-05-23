from game.game import Game
import argparse
import numpy as np
import random
import os
from utils.logs import save_beliefs
from agent import LittleGirl

def main(Players = [4, 16], verbose=False, seed=None, log_dir='logs', update_params=[25, 6, 6, 0.3], p_focus=None, save_logs=True):
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
    game = Game(num_villagers=Players[1], num_wolves=Players[0], seed=seed, update_params=update_params, p_focus=p_focus)
    # Log initial beliefs
    if save_logs:
        save_beliefs(game, 0)

    # Game stats
    stats = {
        'rounds': 0,
        'winner': None,
        'initial_wolves': Players[0],
        'initial_villagers': Players[1],
        'last_turn_little_girl': 0,
        'avg_belief_villagers_on_werewolves': [],
        'avg_belief_werewolves_on_little_girl': [],
        'avg_belief_villagers_on_little_girl': []
    }
    
    # Game loop
    while True:
        if verbose:
            print(f"\n=== Round {stats['rounds'] + 1} ===")
            print(f"Night phase - {game.get_wolves_count()} werewolves, {game.get_villagers_count()} villagers")
        
        # Night phase
        eliminated_night, eliminated_role = game.night_shift()
        if verbose:
            print(f"🌙 Werewolves eliminated villager {eliminated_night} who was a {eliminated_role}")

        # Check if the little girl is alive
        if isinstance(game.alive.get(0, False), LittleGirl):
            stats["last_turn_little_girl"] += 1
        
        # Check win condition after night
        winner = game.check_game_over()
        if winner:
            stats['winner'] = winner
            break

        # Average beliefs on werewolves
        beliefs_werewolves = np.zeros(len(game.werewolves_id))
        for villager_id in game.villagers_id:

            if isinstance(game.alive[villager_id], LittleGirl):
                continue

            beliefs_werewolves += game.alive[villager_id].beliefs[game.werewolves_id] / len(game.villagers_id)
        stats["avg_belief_villagers_on_werewolves"].append(np.mean(beliefs_werewolves))

        # Average beliefs on Little Girl
        belief_werewolves_on_little_girl = []
        belief_villagers_on_little_girl  = []
        for alive_player_id, alive_player in game.alive.items():

            if isinstance(alive_player, LittleGirl):
                continue
            
            if alive_player_id in game.werewolves_id:
                belief_werewolves_on_little_girl.append(alive_player.beliefs[0])
            else:
                belief_villagers_on_little_girl.append(alive_player.beliefs[0])

        stats["avg_belief_werewolves_on_little_girl"].append(np.mean(belief_werewolves_on_little_girl))
        stats["avg_belief_villagers_on_little_girl"].append(np.mean(belief_villagers_on_little_girl))
            
        if verbose:
            print(f"Day phase - {game.get_wolves_count()} werewolves, {game.get_villagers_count()} villagers")
        
        # Day phase
        eliminated_day, target_type = game.day_shift()
        if verbose:
            print(f"☀️ Village eliminated player {eliminated_day} who was a {target_type} !")

        # Check if the little girl is alive
        if isinstance(game.alive.get(0, False), LittleGirl):
            stats["last_turn_little_girl"] += 1

        # Check win condition after day
        winner = game.check_game_over()
        if winner:
            stats['winner'] = winner
            break

        # Average beliefs on werewolves
        beliefs_werewolves = np.zeros(len(game.werewolves_id))
        for villager_id in game.villagers_id:
            
            if isinstance(game.alive[villager_id], LittleGirl):
                continue

            beliefs_werewolves += game.alive[villager_id].beliefs[game.werewolves_id] / len(game.villagers_id)
        stats["avg_belief_villagers_on_werewolves"].append(np.mean(beliefs_werewolves))

        # Average beliefs on Little Girl
        belief_werewolves_on_little_girl = []
        belief_villagers_on_little_girl  = []
        for alive_player_id, alive_player in game.alive.items():

            if isinstance(alive_player, LittleGirl):
                continue
            
            if alive_player_id in game.werewolves_id:
                belief_werewolves_on_little_girl.append(alive_player.beliefs[0])
            else:
                belief_villagers_on_little_girl.append(alive_player.beliefs[0])

        stats["avg_belief_werewolves_on_little_girl"].append(np.mean(belief_werewolves_on_little_girl))
        stats["avg_belief_villagers_on_little_girl"].append(np.mean(belief_villagers_on_little_girl))
    
        # Save beliefs after each round
        if save_logs:
            save_beliefs(game, stats['rounds'] + 1, log_dir=log_dir)
            
        stats['rounds'] += 1
    
    if verbose:
        print("\n=== Game Over ===")
        print(f"Game ended after {stats['rounds']+1} rounds")
        print(f"Winner: {stats['winner']}")
        print(f"Remaining villagers: {game.get_villagers_count()}")
        print(f"Remaining werewolves: {game.get_wolves_count()}")
        print(f"Last turn little girl: {stats['last_turn_little_girl']}")
        print(f"Average beliefs villagers on werewolf: {stats["avg_belief_villagers_on_werewolves"][-1]}")
        print(f"Average belief werewolves on little_girl: {stats["avg_belief_werewolves_on_little_girl"][-1]}")
        print(f"Average belief villagers on little_girl: {stats["avg_belief_villagers_on_little_girl"][-1]}")
    
    return stats

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run a Werewolf game simulation.')
    parser.add_argument('--players', type=int, default=100, help='Total number of players')
    parser.add_argument('--ratio', type=float, default=0.1, help='Ratio of werewolves to total players')
    parser.add_argument('--p-focus', type=float, help="Add a Little Girl among Villagers with a p_focus", default=None)
    parser.add_argument('--verbose', '-v', action='store_true', help='Print detailed game progress')
    parser.add_argument('--seed', type=int, help='Random seed for reproducibility', default=None)
    parser.add_argument('--log_dir', type=str, help='Directory to save belief logs', default='logs')
    parser.add_argument('--save_logs', '-s', action='store_true', help='Save belief logs', default=False)
    args = parser.parse_args()
    
    main(Players=[int(args.players * args.ratio), args.players], verbose=args.verbose, seed=args.seed, log_dir=args.log_dir, save_logs=args.save_logs, p_focus=args.p_focus)