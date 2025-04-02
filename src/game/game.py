from agent.villagers import Villager
from agent.werewolf import Werewolf
import numpy as np

class Game():

    def __init__(self, num_villagers=1, num_wolves=1, update_params = [0.15, 0.15, 0.2, 0.3], seed=42): # [lambda, eta, beta, gamma]
        """
        init a game instance.
        num_villagers:  int     number of villagers in the game
        num_wolves:     int     number of wolves in the game
        update_params:  list    [lambda, eta, beta, gamma] where:
                                lambda: belief update for werewolf elimination
                                eta: belief update for villager elimination
                                beta: revenge factor for being voted against
                                gamma: maximum allowed kill will shift
        seed:           int     random seed for reproducibility
        """
        np.random.seed(seed)  # Set random seed
        self.seed = seed
        self.num_villagers = num_villagers
        self.num_wolves = num_wolves
        self.num_players =  self.num_villagers + self.num_wolves
        self.update_params = update_params 

        #dictionaries containing active werewolfs and villagers in the game
        self.werewolfs = {}
        self.villagers = {}

        # lists including eliminated werewolfs and villagers
        self.dead_werewolfs = []
        self.dead_villagers = []
        
        self.villagers_id = range(self.num_villagers) #list ids of the villagers
        self.werewolfs_id = range(self.num_villagers, self.num_players) #list ids of the werewolfes

        for i in self.villagers_id:
            self.villagers[i] = Villager(i, self.num_players, self.seed)

        for j in self.werewolfs_id:
            self.werewolfs[j] = Werewolf(j, self.num_players, self.werewolfs_id, self.villagers_id, self.seed)
        
    def get_villagers_count(self):
        """
        gets current number of villagers

        returns int
        """
        return self.num_villagers - len(self.dead_villagers)
    
    def get_wolves_count(self):
        """
        gets current number of werewolfs

        returns int
        """
        return self.num_wolves - len(self.dead_werewolfs)
    
    def get_agents_count(self):
        """
        gets current total number of agents

        returns int
        """
        return self.get_villagers_count() + self.get_wolves_count()

    def eliminate_werewolf(self, id):
        """
        elimintes a werewolf with specified id
        id: int  id of the werewolf to be eliminted
        """
        self.dead_werewolfs.append(self.werewolfs.pop(id))
        
        self.werewolfs_id = self.werewolfs.keys()
        
        # Update beliefs of remaining agents
        for villager in self.villagers.values():
            villager.remove_dead_player(id)
        for werewolf in self.werewolfs.values():
            werewolf.remove_dead_player(id)

    def eliminate_villager(self, id):
        """
        eliminates a villager with specific id
        id: int  id of the villager to be eliminated
        """
        self.dead_villagers.append(self.villagers[id])
        self.villagers.pop(id)
        self.villagers_id = self.villagers.keys()
        
        # Update beliefs of remaining agents
        for villager in self.villagers.values():
            villager.remove_dead_player(id)
        for werewolf in self.werewolfs.values():
            werewolf.remove_dead_player(id)

    def calc_inf_metric(self):
        """
        #TODO  this is currently incomplete. see section 3.4 in report
        Calculates current sum of villagers mean kill will for werewolfs
        information propogation metric

        returns float
        """
        total_sum = 0
        for k, v in self.villagers:
            mean_b = np.mean(v.beliefs[self.werewolfs_id])
            total_sum + mean_b
        return total_sum

    def check_game_over(self):
        """
        Check if game is over and return winner
        
        Returns:
            None if game is not over
            "werewolfs" if werewolfs won
            "Villagers" if villagers won
        """
        if self.get_villagers_count() <= self.get_wolves_count():
            return "werewolfs"
        elif self.get_wolves_count() == 0:
            return "Villagers"
        return None

    def update_beliefs_after_elimination(self, eliminated_id, voters_dict, eliminated_type):
        """
        Updates beliefs of all agents after an elimination
        eliminated_id: int - ID of the eliminated player
        voters_dict: dict - Dictionary mapping voter IDs to their votes
        eliminated_type: str - "Werewolf" or "Villager"
        """
        voted_for_eliminated = {voter_id for voter_id, vote in voters_dict.items() if vote == eliminated_id}
        
        # Update villagers' beliefs
        for villager in self.villagers.values():
            # Store previous beliefs for clipping
            previous_beliefs = villager.beliefs.copy()
            
            # Apply revenge update - increase kill will for players who voted against this villager
            for voter_id, vote in voters_dict.items():
                if vote == villager.id and villager.beliefs[voter_id] is not None:
                    old_belief = villager.beliefs[voter_id]
                    new_belief = old_belief + self.update_params[2]
                    villager.beliefs[voter_id] = np.clip(new_belief, 
                                                       old_belief - self.update_params[3],
                                                       old_belief + self.update_params[3])
            
            for other_id in range(self.num_players):
                # Skip if the belief is None (dead player, self, or werewolf-werewolf)
                if villager.beliefs[other_id] is None:
                    continue
                
                old_belief = villager.beliefs[other_id]
                # Case 1: Eliminated player was a villager
                if eliminated_type == "Villager":
                    if other_id in voted_for_eliminated:
                        new_belief = old_belief + self.update_params[1]
                    else:
                        new_belief = old_belief - self.update_params[1]
                
                # Case 2: Eliminated player was a werewolf
                elif eliminated_type == "Werewolf":
                    if other_id in voted_for_eliminated:
                        new_belief = old_belief - self.update_params[0]
                    else:
                        new_belief = old_belief + self.update_params[0]
                
                # Clip the belief change based on gamma
                villager.beliefs[other_id] = np.clip(new_belief,
                                                   old_belief - self.update_params[3],
                                                   old_belief + self.update_params[3])

    def day_shift(self):
        """
        During day shift, all players vote to eliminate one player.
        The player with most votes is eliminated.
        Returns the eliminated player or None if no one was eliminated.
        """
        # Collect votes from all players with voter IDs
        votes = {}
        for villager in self.villagers.values():
            # print(f"Villager {villager.id} beliefs: {np.around(villager.beliefs, decimals=1)}")
            votes[villager.id] = villager.vote()
        for werewolf in self.werewolfs.values():
            # print(f"Werewolf {werewolf.id} beliefs: {np.around(werewolf.beliefs, decimals=1)}")
            votes[werewolf.id] = werewolf.vote()
        
        # Count votes and eliminate player with most votes
        if len(votes) > 0:
            vote_counts = np.bincount([v for v in votes.values()])
            max_votes = np.max(vote_counts)
            # Get all players with maximum votes
            candidates = np.where(vote_counts == max_votes)[0]
            # Randomly select one among the candidates
            eliminated_id = np.random.choice(candidates)
            # print(f"Candidates: {candidates}")
            # print(f"Eliminated ID: {eliminated_id}")
            # print(f"werewolfs_id: {self.werewolfs_id}")
            # print(f"villagers_id: {self.villagers_id}")
            target_type = None
            
            if eliminated_id in self.werewolfs_id:
                self.eliminate_werewolf(eliminated_id)
                target_type = "Werewolf"
            elif eliminated_id in self.villagers_id:
                self.eliminate_villager(eliminated_id)
                target_type = "Villager"
            # print(votes)
            # Update beliefs after elimination
            if target_type:
                self.update_beliefs_after_elimination(eliminated_id, votes, target_type)
            
            return eliminated_id, target_type
        return None

    def night_shift(self):
        """
        During night shift, werewolfs collectively vote to eliminate one villager
        Returns the ID of the eliminated villager or None if no one was eliminated
        """
        # Collect votes from werewolfs
        if len(self.werewolfs) > 0 and len(self.villagers) > 0:
            votes = []
            for werewolf in self.werewolfs.values():
                votes.append(werewolf.night_vote(self.villagers_id))
            
            # Count votes and get all villagers with maximum votes
            vote_counts = np.bincount(votes)
            max_votes = np.max(vote_counts)
            candidates = np.where(vote_counts == max_votes)[0]
            # Randomly select one among the candidates
            eliminated_id = np.random.choice(candidates)

            # Eliminate the chosen villager if they exist
            if eliminated_id in self.villagers_id:
                self.eliminate_villager(eliminated_id)
                return eliminated_id
        return None


if __name__ == "__main__":
    game = Game()
