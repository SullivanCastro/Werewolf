import numpy as np

from .agent import Agent

class Villager(Agent):
    def __init__(self, id, num_players, seed=42):
        super().__init__(id, num_players, seed)
        self.id = id
        self.type = "Villager"