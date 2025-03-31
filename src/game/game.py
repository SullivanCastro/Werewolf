
from agent.villagers import Villager
from agent.werewolf import Werewolf
import numpy as np

class Game():

    def __init__(self, num_villagers=1, num_wolves=1):
        """
        init a game instance.
        num_villagers:  int     number of villagers in the game
        num_wolves:     int     number of wolves in the game
        """
        self.num_villagers = num_villagers
        self.num_wolves = num_wolves
        self.num_players =  self.num_villagers + self.num_wolves

        #dictionaries containing active werewolves and villagers in the game
        self.werewolves = {}
        self.villagers = {}

        # lists including eliminated werewolves and villagers
        self.dead_werewolves = []
        self.dead_villagers = []

        for i in range(self.num_villagers):
            self.villagers[i] = Villager(i, self.num_players)
        self.villagers_id = self.villagers.keys()

        self.werewolfs_id = range(self.num_villagers-1, self.num_players) #list ids of the werewolfes
        for j in self.werewolfs_id:
            self.werewolves[j] = Werewolf(j, self.num_players, self.werewolfs_id, self.villagers_id)

        
    def get_villagers_count(self):
        """
        gets current number of villagers

        returns int
        """
        return len(self.villagers_id)
    
    def get_wolves_count(self):
        """
        gets current number of werewolves

        returns int
        """
        return len(self.werewolfs_id)
    
    def get_agents_count(self):
        """
        gets current total number of agents

        returns int
        """
        return len(self.werewolfs_id) + len(self.villagers_id)

    def eliminate_werewolf(self, id):
        """
        elimintes a werewolf with specified id
        id: int  id of the werewolf to be eliminted
        """
        self.dead_werewolves.append(self.werewolves[id])
        self.werewolves.pop(id)
        self.werewolfs_id = self.werewolves.keys()

    def eliminate_villager(self, id):
        """
        eliminates a villager with specific id
        id: int  id of the villager to be eliminated
        """
        self.dead_villagers.append(self.villagers[id])
        self.villagers.pop(id)
        self.villagers_id = self.villagers.keys()


    def calc_inf_metric(self):
        """
        #TODO  this is currently incomplete. see section 3.4 in report
        Calculates current sum of villagers mean kill will for werewolves
        information propogation metric

        returns float
        """
        total_sum = 0
        for k, v in self.villagers:
            mean_b = np.mean(v.beliefs[self.werewolfs_id])
            total_sum + mean_b
        return total_sum

    def day_shift(self,):

        pass
        #do the day shift

    def night_shift(self,):
        pass
        #do the night shift


if __name__ == "__main__":
    game = Game()
