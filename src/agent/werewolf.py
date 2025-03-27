import numpy as np

from .agent import Agent

class Werewolf(Agent):
    def __init__(self, id, game):
        super().__init__(id, game, is_werewolf=True)
        self.beliefs[game.werewolfs_id] = 0
        self.beliefs /= np.sum(self.beliefs)
        self.id = id
        self.type = "Werewolf"