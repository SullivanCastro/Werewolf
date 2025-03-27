import numpy as np

from .agent import Agent

class Villager(Agent):
    def __init__(self, name, game):
        super().__init__()
        self.name = name
        self.type = "Villager"
        self.beliefs = np.ones(game.num_players)
        self.beliefs[game.player_id] = 0

    def _draw_suspect(self):
        return np.argmax(self.beliefs)
    
    def choose_vote(self, suspects):
        return self.vote(self._draw_suspect(suspects))