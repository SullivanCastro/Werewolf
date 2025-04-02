import numpy as np

class Agent:
    def __init__(self, id, num_players, seed=42):
        np.random.seed(seed + id)  # Different seed for each agent based on their ID
        # Initialize beliefs array with random values from normal distribution
        self.beliefs = np.random.normal(loc=1.0, scale=0.1, size=num_players)
        self.beliefs[id] = None

    def vote(self):
        # Get indices and beliefs of valid suspects (not None and not nan)
        valid_suspects = [(i, b) for i, b in enumerate(self.beliefs) 
                         if b is not None and not np.isnan(b)]
        
        if not valid_suspects:
            return None  # Return None if no valid suspects
            
        # Find the maximum belief value
        max_belief = max(b for _, b in valid_suspects)
        # Get all indices with maximum belief
        max_indices = [i for i, b in valid_suspects if b == max_belief]
        # Randomly choose among the players with maximum belief
        return np.random.choice(max_indices)
        
    def update_beliefs(self, beliefs):
        self.beliefs = beliefs

    def remove_dead_player(self, dead_id):
        """Update beliefs when a player dies by setting their belief to None"""
        self.beliefs[dead_id] = None

