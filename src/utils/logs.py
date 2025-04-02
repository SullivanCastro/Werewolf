import json
import numpy as np
import os
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns
import argparse

def save_beliefs(game, round_num, log_dir='logs'):
    """
    Save the belief matrix for all agents to a JSON file.
    
    Args:
        game: Game instance containing all agents
        round_num: Current round number (-1 for initial state)
        log_dir: Directory to save logs
    """
    # Create logs directory if it doesn't exist
    os.makedirs(log_dir, exist_ok=True)
    
    # Get current datetime truncated to minutes with underscore format
    current_time = datetime.now().strftime("%Y_%m_%d_%H_%M")
    
    # Create belief matrix
    num_players = game.num_players
    belief_matrix = np.full((num_players, num_players), np.nan)
    
    # Fill in villagers' beliefs
    for vid, villager in game.villagers.items():
        belief_matrix[vid] = villager.beliefs
        
    # Fill in werewolves' beliefs
    for wid, werewolf in game.werewolfs.items():
        belief_matrix[wid] = werewolf.beliefs
        
    # Convert to nested list (JSON serializable)
    belief_matrix = belief_matrix.tolist()
    
    # Load existing data if file exists
    log_file = os.path.join(log_dir, f'game_{game.seed}_{current_time}_beliefs.json')
    try:
        with open(log_file, 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        data = {}
    

    # Update data with current round
    data[str(round_num)] = belief_matrix

    # calculate information propogation metrics
    info_metric = game.calc_inf_metric()

    data.update(info_metric)

    #calculate information entropy
    info_entropy = game.calc_info_entropy()

    data.update(info_entropy)
    
    # Save updated data
    with open(log_file, 'w') as f:
        json.dump(data, f, indent=2)

def visualize_beliefs(log_file):
    """
    Read a belief log file and display the sequence of belief matrices as heatmaps.
    Save the plot with the same base name as the JSON file.
    
    Args:
        log_file: Path to the JSON log file
    """
    # Read the JSON file
    with open(log_file, 'r') as f:
        data = json.load(f)
    
    # Sort rounds by integer value
    rounds = sorted([int(k) for k in data.keys()])
    n_rounds = len(rounds)
    n_players = len(data[str(rounds[0])])
    
    # Create a figure with subplots
    n_cols = min(5, n_rounds)  # Maximum 5 columns
    n_rows = (n_rounds + n_cols - 1) // n_cols
    fig, axes = plt.subplots(n_rows, n_cols, figsize=(4*n_cols, 4*n_rows))
    if n_rows == 1:
        axes = axes.reshape(1, -1)
    
    # Custom colormap: green to red with black for NaN
    colors = [(0, 0.8, 0), (1, 0, 0)]  # Green to red
    cmap = plt.matplotlib.colors.LinearSegmentedColormap.from_list("custom", colors)
    cmap.set_bad('black')  # Set NaN color to black
    
    # Plot each round
    for idx, round_num in enumerate(rounds):
        row = idx // n_cols
        col = idx % n_cols
        ax = axes[row, col]
        
        # Convert data to numpy array
        beliefs = np.array(data[str(round_num)])
        
        # Create heatmap
        sns.heatmap(beliefs, cmap=cmap, ax=ax, vmin=0, vmax=2,
                   cbar=True if col == n_cols-1 else False)
        ax.set_title(f'Round {round_num}')
        ax.set_xlabel('Target Player')
        ax.set_ylabel('Observer Player')
    
    # Remove empty subplots if any
    for idx in range(len(rounds), n_rows * n_cols):
        row = idx // n_cols
        col = idx % n_cols
        fig.delaxes(axes[row, col])
    
    plt.tight_layout()
    
    # Save plot with same name as JSON file but with .png extension
    plot_file = os.path.splitext(log_file)[0] + '.png'
    plt.savefig(plot_file, dpi=300, bbox_inches='tight')
    plt.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Visualize belief matrices from a game log.')
    parser.add_argument('--path', type=str, help='Path to the JSON log file')
    args = parser.parse_args()

    if args.path:
        if os.path.exists(args.path):
            visualize_beliefs(args.path)
        else:
            print(f"File not found: {args.path}")
    else:
        # Default behavior: find most recent log
        log_dir = 'logs'
        log_files = [f for f in os.listdir(log_dir) if f.endswith('_beliefs.json')]
        if log_files:
            latest_log = max(log_files)
            visualize_beliefs(os.path.join(log_dir, latest_log))
        else:
            print("No log files found")
