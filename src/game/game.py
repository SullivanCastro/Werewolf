
from agent.villagers import Villager
from agent.werewolf import Werewolf
import numpy as np

class Game():

    def __init__(self, num_villagers=1, num_wolves=1):
        self.num_villagers = num_villagers
        self.num_wolves = num_wolves
        self.num_players =  self.num_villagers + self.num_wolves
        self.werewolves = {}
        self.villagers = {}
        self.dead_werewolves = []
        self.dead_villagers = []

        for i in range(self.num_villagers):
            self.villagers[i] = Villager(i, self.num_players)
        self.villagers_id = self.villagers.keys()

        self.werewolfs_id = range(self.num_villagers-1, self.num_players) #list ids of the werewolfes
        for j in self.werewolfs_id:
            self.werewolves[j] = Werewolf(j, self.num_players, self.werewolfs_id, self.villagers_id)

        
    

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
