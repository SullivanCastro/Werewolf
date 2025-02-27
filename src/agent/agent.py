import numpy as np

class Agent:
    def __init__(self, is_leader, is_avenger):
        self.is_leader = is_leader
        self.is_avenger = is_avenger
        self.suspect_werewolf = None
        self.last_attacker = None

    def vote(self, suspects):
        # Draw randomly in the list of suspect
        return np.random.choice(suspects)

