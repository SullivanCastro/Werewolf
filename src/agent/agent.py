import numpy as np

class Agent:
    def __init__(self, id, game, is_werewolf=False):
        self.beliefs = np.ones(game.num_players)
        self.beliefs[id] = 0
        if is_werewolf:
            self.beliefs[game.werewolfs_id] = 0
        self.beliefs /= np.sum(self.beliefs)

    def vote(self, suspects):
        # Draw randomly in the list of suspect
        return np.random.choice(suspects)
    
    

