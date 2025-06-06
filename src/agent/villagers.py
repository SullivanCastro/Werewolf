import numpy as np

from .agent import Agent
from utils import softmax

class Villager(Agent):
    def __init__(self, id, num_players, seed=42):
        super().__init__(id, num_players, seed)
        self.beliefs = softmax(self.beliefs)
        self.id = id
        self.type = "Villager"
        self.role = self.type