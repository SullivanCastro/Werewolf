import numpy as np

from .agent import Agent

class Werewolf(Agent):
    def __init__(self, id, num_players, werewolves_id, villagers_id, seed=42):
        """
        id: int                 unique integer among werewolves
        num_players: int        total number of players in the game
        werewolves_id: list     list of ids of all werewolves in game
        villagers_id:  list     list of ids of all villagers in game
        seed: int               random seed for reproducibility
        """
        super().__init__(id, num_players, seed)
        # Set beliefs towards other werewolves to None
        self.beliefs[werewolves_id] = None
        self.id = id
        self.type = "Werewolf"

        # a werewolf knows who are the villagers
        self.villagers_id = villagers_id

    def night_vote(self, villagers_id):
        """
        Vote for a villager to eliminate during night phase.
        Returns the ID of the chosen villager.
        """
        self.villagers_id = villagers_id # Update the list of villagers
        # Simply choose a random villager from the remaining ones
        if len(self.villagers_id) > 0:
            return np.random.choice(list(self.villagers_id))
        return 0
