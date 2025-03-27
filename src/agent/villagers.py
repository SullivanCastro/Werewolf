import numpy as np

from .agent import Agent

class Villager(Agent):
    def __init__(self, id, game):
        super().__init__(id, game, is_werewolf=False)
        self.beliefs /= np.sum(self.beliefs)
        self.id = id
        self.type = "Villager"