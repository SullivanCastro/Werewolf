import numpy as np

from .agent import Agent

class Werewolf(Agent):
    def __init__(self, id, num_players, werewolves_id):
        super().__init__(id, num_players)
        self.beliefs[werewolves_id] = 0
        self.beliefs /= np.sum(self.beliefs)
        self.id = id
        self.type = "Werewolf"