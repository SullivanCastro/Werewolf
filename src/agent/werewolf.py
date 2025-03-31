import numpy as np

from .agent import Agent

class Werewolf(Agent):
    def __init__(self, id, num_players, werewolves_id, villagers_id):
        """
        id: int                 unique integer among werewolves
        num_players: int        total number of players in the game
        werewolves_id: list     list of ids of all werewolves in game
        villagers_id:  list     list of ids of all villagers in game
        """
        super().__init__(id, num_players)
        self.beliefs = np.ones(len(villagers_id))
        self.beliefs[id] = 0
        self.beliefs /= np.sum(self.beliefs)
        self.id = id
        self.type = "Werewolf"

        # a werewolf knows who are the villagers
        self.villagers_id = villagers_id

    def night_vote(self,):

        pass