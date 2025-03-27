import numpy as np

class Agent:
    def __init__(self, id, game):
        self.beliefs = np.ones(game.num_players)
        self.beliefs[id] = 0

    def _draw_suspects(self, beliefs):
        # Draw suspects from the beliefs
        return np.random.choice(np.argmax(beliefs))

    def vote(self):
        # Draw randomly in the list of suspect
        return np.random.choice(self._draw_suspects(self.beliefs))

