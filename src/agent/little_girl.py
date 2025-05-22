import numpy as np

from .agent import Agent
from utils import softmax

class LittleGirl(Agent):
    def __init__(self, id, num_players, p_focus=0.3, seed=42):
        super().__init__(id, num_players, seed)
        self.beliefs = softmax(self.beliefs)
        self.id = id
        self.type = "Villager"
        self.role = "LittleGirl"
        self.p_focus = p_focus
        self.focus = False
        self.save_beliefs = None