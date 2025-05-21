import numpy as np
from main import main
import argparse
from tqdm import tqdm
import matplotlib.pyplot as plt
import seaborn as sns
import os

def simulation(nb_players=100, ratio_werewolf=0.1, nb_iter=1000, update_params=[0.15, 0.15, 0.2, 0.3], is_little_girl=False, verbose=False):
    """
    Run multiple simulations of werewolf games and analyze results.
    
    Args:
        nb_players (int): Total number of players in each game
        ratio_werewolf (float): Ratio of werewolves to total players
        nb_iter (int): Number of games to simulate
        update_params (list): Parameters for belief updates [lambda, eta, _lambda, gamma]
        verbose (bool): Whether to show progress bar
    
    Returns:
        tuple: (villager_win_ratio, mean_rounds)
    """
    # Calculate number of werewolves and villagers
    num_werewolves = int(nb_players * ratio_werewolf)
    num_villagers = nb_players - num_werewolves
    
    # Stats tracking
    villager_wins = 0
    total_rounds = 0
    
    # Create iterator with optional progress bar
    iterator = tqdm(range(nb_iter)) if verbose else range(nb_iter)
    
    # Run simulations
    for i in iterator:
        stats = main(
            Players=[num_werewolves, num_villagers],
            verbose=False,
            seed=i,
            save_logs=False,
            update_params=update_params,
            is_little_girl=is_little_girl
        )
        
        if stats['winner'] == "Villagers":
            villager_wins += 1
        total_rounds += stats['rounds']
    
    villager_win_ratio = villager_wins / nb_iter
    mean_rounds = total_rounds / nb_iter

    return villager_win_ratio, mean_rounds

def plot_phase_eta_lambda(nb_players=100, ratio_werewolf=0.1, nb_iter=100, is_little_girl=False):
    """
    Create a phase diagram showing villager win rates for different eta and _lambda values.
    
    Args:
        nb_players (int): Total number of players in each game
        ratio_werewolf (float): Ratio of werewolves to total players
        nb_iter (int): Number of games to simulate per parameter combination
    """
    # Create parameter ranges
    eta_range = np.arange(0, 30, 0.5)
    _lambda_range = np.arange(0, 30, 0.5)
    
    # Initialize results matrix
    results = np.zeros((len(_lambda_range), len(eta_range)))
    
    # Run simulations for each parameter combination
    total_combinations = len(eta_range) * len(_lambda_range)
    with tqdm(total=total_combinations, desc="Running parameter combinations") as pbar:
        for i, _lambda in enumerate(_lambda_range):
            for j, eta in enumerate(eta_range):
                # Set parameters: [eta, eta, _lambda, 0.3]
                update_params = [eta, _lambda, _lambda, 0.3]
                
                # Run simulation with these parameters
                win_ratio, _ = simulation(
                    nb_players=nb_players,
                    ratio_werewolf=ratio_werewolf,
                    nb_iter=nb_iter,
                    update_params=update_params,
                    is_little_girl=is_little_girl
                )
                
                # Store result
                results[i, j] = win_ratio
                pbar.update(1)
    
    # Create heatmap
    plt.figure(figsize=(10, 8))
    sns.heatmap(
        results,
        xticklabels=[f"{x:.2f}" for x in eta_range],
        yticklabels=[f"{x:.2f}" for x in _lambda_range],
        cmap='RdYlBu',
        vmin=0,
        vmax=1,   
    )
    
    plt.xlabel('η (eta)')
    plt.ylabel('λ (lambda)')
    plt.xticks(rotation=90)
    plt.title('Villager Win Rate Phase Diagram')
    
    # Create logs directory if it doesn't exist
    os.makedirs('logs', exist_ok=True)
    
    # Save plot
    plt.savefig('logs/phase_diagram.png', dpi=300, bbox_inches='tight')
    plt.close()


def plot_phase_ratio(nb_players=100, nb_iter=100):
    """
    Create a phase diagram showing villager win rates for different eta and _lambda values.
    
    Args:
        nb_players (int): Total number of players in each game
        ratio_werewolf (float): Ratio of werewolves to total players
        nb_iter (int): Number of games to simulate per parameter combination
    """
    # Create parameter ranges
    total_players = np.arange(10, nb_players)
    ratio = np.linspace(0.1, 1, 10)
    
    # Initialize results matrix
    results = np.zeros((len(total_players), len(ratio)))
    
    # Run simulations for each parameter combination
    total_combinations = len(total_players) * len(ratio)
    with tqdm(total=total_combinations, desc="Running parameter combinations") as pbar:
        for i, werewolf_ratio in enumerate(ratio):
            for j, player_number in enumerate(total_players):
                # Set parameters: [eta, eta, _lambda, 0.3]
                update_params = [player_number, player_number, werewolf_ratio, 0.3]
                
                # Run simulation with these parameters
                win_ratio, _ = simulation(
                    nb_players=nb_players,
                    ratio_werewolf=werewolf_ratio,
                    nb_iter=nb_iter
                )
                
                # Store result
                results[i, j] = win_ratio
                pbar.update(1)
    
    # Create heatmap
    plt.figure(figsize=(10, 8))
    sns.heatmap(
        results,
        xticklabels=[f"{x:.2f}" for x in total_players],
        yticklabels=[f"{x:.2f}" for x in ratio],
        cmap='RdYlBu',
        vmin=0,
        vmax=1
    )
    
    plt.xlabel('Total players')
    plt.ylabel('Werewolf ratio')
    plt.title('Villager Win Rate Phase Diagram')
    
    # Create logs directory if it doesn't exist
    os.makedirs('logs', exist_ok=True)
    
    # Save plot
    plt.savefig('logs/phase_ratio.png', dpi=300, bbox_inches='tight')
    plt.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run multiple Werewolf game simulations.')
    parser.add_argument('--players', type=int, default=100, help='Total number of players')
    parser.add_argument('--ratio', type=float, default=0.1, help='Ratio of werewolves to total players')
    parser.add_argument('--is_little_girl', action='store_true', help='Add 1 Little Girl among the Villagers', default=False)
    parser.add_argument('--iterations', type=int, default=1000, help='Number of games to simulate')
    parser.add_argument('--phase-plot', action='store_true', help='Generate phase plot', default=False)
    args = parser.parse_args()
    
    if args.phase_plot:
        plot_phase_eta_lambda(
            nb_players=args.players,
            ratio_werewolf=args.ratio,
            nb_iter=args.iterations,
            is_little_girl=args.is_little_girl
        )
    # if args.ratio_plot:
    #     plot_phase_ratio(
    #         nb_players=args.players,
    #         nb_iter=args.iterations
    #     )
    else:
        win_ratio, avg_rounds = simulation(
            nb_players=args.players,
            ratio_werewolf=args.ratio,
            nb_iter=args.iterations,
            verbose=True
        )
        
        print(f"Results from {args.iterations} simulations:")
        print(f"Village win ratio: {win_ratio:.2%}")
        print(f"Average rounds per game: {avg_rounds:.1f}")
