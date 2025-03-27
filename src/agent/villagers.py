import numpy as np

from .agent import Agent

class Villager(Agent):
    def __init__(self, id, num_players):
        super().__init__(id, num_players)
        self.beliefs /= np.sum(self.beliefs)
        self.id = id
        self.type = "Villager"