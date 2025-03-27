
from agent.villagers import Villager
from agent.werewolf import Werewolf
class Game():

    def __init__(self, num_villagers=1, num_wolves=1):
        self.num_villagers = num_villagers
        self.num_wolves = num_wolves
        self.num_players =  self.num_villagers + self.num_wolves
        self.werewolves = {}
        self.villagers = {}
        for i in range(self.num_villagers):
            self.villagers[i] = Villager(i, self.num_players)

        self.werewolfs_id = range(self.num_villagers-1, self.num_players) #list ids of the werewolfes
        for j in range(self.werewolfs_id):
            self.werewolves[j] = Werewolf(j, self.num_players, self.werewolfs_id)
    
    def day_shift(self,):
        pass
        #do the day shift

    def night_shift(self,):
        pass
        #do the night shift


if __name__ == "__main__":
    game = Game()
