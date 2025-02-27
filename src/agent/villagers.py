import numpy as np

from .agent import Agent

class Villager(Agent):
    def __init__(self, name, is_leader, is_avenger):
        super().__init__(is_leader, is_avenger)
        self.name = name
        self.type = "Villager"

    def _draw_suspect(self, suspects, game):
        if self.is_avenger and game.is_alive(self.last_attacker):
            return np.arange(len(suspects)) == self.last_attacker
        return suspects
    
    def choose_vote(self, suspects):
        return self.vote(self._draw_suspect(suspects))