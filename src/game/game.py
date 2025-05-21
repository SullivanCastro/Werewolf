from agent import Villager, Werewolf, LittleGirl
from utils import softmax
import numpy as np

class Game():

    def __init__(self, num_villagers=1, num_wolves=1, update_params = [15, 15, 2, 0.3], is_little_girl=True, seed=42): # [lambda, eta, beta, gamma]
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
        self.seed           = seed
        self.num_villagers  = num_villagers
        self.num_wolves     = num_wolves
        self.num_players    = self.num_villagers + self.num_wolves
        self.is_little_girl = is_little_girl
        self._eta, self._lambda, self._mu, self._gamma = update_params 
        

        #dictionaries containing active werewolves and villagers in the game
        self.werewolves = {}
        self.villagers = {}

        # lists including eliminated werewolves and villagers
        self.dead_werewolves = []
        self.dead_villagers = []
        
        self.villagers_id = range(self.num_villagers) #list ids of the villagers
        self.werewolves_id = range(self.num_villagers, self.num_players) #list ids of the werewolfes

        if is_little_girl:
            self.villagers[self.villagers_id[0]] = LittleGirl(self.villagers_id[0], self.num_players, self.seed)
            for i in self.villagers_id[1:]:
                self.villagers[i] = Villager(i, self.num_players, self.seed)
        else:    
            for i in self.villagers_id:
                self.villagers[i] = Villager(i, self.num_players, self.seed)

        for j in self.werewolves_id:
            self.werewolves[j] = Werewolf(j, self.num_players, self.werewolves_id, self.villagers_id, self.seed)

        # Alive dictionary
        self.alive = self.villagers.copy()
        self.alive.update(self.werewolves.copy())
        
    def get_villagers_count(self):
        """
        gets current number of villagers

        returns int
        """
        return self.num_villagers - len(self.dead_villagers)
    
    def get_wolves_count(self):
        """
        gets current number of werewolves

        returns int
        """
        return self.num_wolves - len(self.dead_werewolves)
    
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
        self.dead_werewolves.append(self.werewolves.pop(id))
        
        self.werewolves_id = list(self.werewolves.keys())
        
        self.alive.pop(id)

    def eliminate_villager(self, id):
        """
        eliminates a villager with specific id
        id: int  id of the villager to be eliminated
        """
        self.dead_villagers.append(self.villagers[id])
        self.villagers.pop(id)
        self.villagers_id = list(self.villagers.keys())
        self.alive.pop(id)

    def calc_inf_metric(self):
        """
        Calculates current sum of villagers mean kill will for werewolves and for villagers.
        information propogation metric

        returns {"s_werewolves": float, "s_villagers": float}
        """
        s_w = 0  #S_werewolves  for current round. See section 3.5 of report
        s_v = 0  #S_villagers  for current round. See section  3.6 of report
        for k, v in self.villagers:
            mean_w = np.nanmean(v.beliefs[self.werewolves_id])
            s_w = s_w + mean_w
            mean_v = np.nanmean(v.beliefs[self.villagers_id])
            s_v = s_v + mean_v
        return {"s_werewolves": s_w, "s_villagers": s_v}
    
    def calc_info_entropy(self):
        """
        calculates entropy in villagers' kill will

        Returns: {"entropy": float}

        """
        total_entropy = 0
        for k, v in self.villagers:
            filtered_belief = [x for x in v.beliefs if x is not None]
            if len(filtered_belief) == 0:
                continue
            belief_array = np.array(filtered_belief)
            entropy = -np.sum(belief_array * np.log(belief_array))
            total_entropy = total_entropy + entropy
        return {"entropy": total_entropy}

    def check_game_over(self):
        """
        Check if game is over and return winner
        
        Returns:
            None if game is not over
            "werewolves" if werewolves won
            "Villagers" if villagers won
        """
        if self.get_villagers_count() <= self.get_wolves_count():
            return "werewolves"
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

        # Update players' beliefs
        for player in self.alive.values():
            player.beliefs[eliminated_id] = np.nan

            # If the player is a villager
            if player in list(self.villagers.values()):

                if isinstance(player, LittleGirl) and np.isnan(player.beliefs).all():
                    alive_id = list(self.villagers.keys()) + list(self.werewolves.keys())
                    player.beliefs[alive_id] = 1
 
                for voter_id, vote in voters_dict.items():

                    if (voter_id == player.id) or (voter_id == eliminated_id):
                        continue
                    
                    old_belief = player.beliefs[voter_id]
                    new_belief = old_belief

                    """ Death vote """
                    new_belief += self._eta * ( (eliminated_type == player.type) - (eliminated_type != player.type) ) * (vote == eliminated_id)

                    """ Revenge vote """
                    new_belief += self._lambda * (vote == player.id) 

                    """ Friendship vote """
                    new_belief += -self._mu * (vote == voters_dict[player.id]) 

                    """ Clipping the belief """
                    player.beliefs[voter_id] = np.clip(new_belief,
                                                   old_belief - self._gamma * 1e24,
                                                   old_belief + self._gamma * 1e24)


            # If the player is a werewolf
            else:
                for voter_id, vote in voters_dict.items():
                    active_werewolves = list(self.werewolves.keys())
                    
                    if (voter_id == player.id) or (voter_id in active_werewolves) or (voter_id == eliminated_id):
                        continue

                    old_belief = player.beliefs[voter_id]
                    new_belief = old_belief

                    """ Death vote """
                    new_belief += self._eta * ( (vote in active_werewolves) - (vote not in active_werewolves) )

                    """ Revenge vote """
                    new_belief += self._lambda * (vote == player.id) 

                    """ Friendship vote """
                    new_belief += -self._mu * (vote == voters_dict[player.id]) 

                    """ Clipping the belief """
                    player.beliefs[voter_id] = np.clip(new_belief,
                                                   old_belief - self._gamma * 1e24,
                                                   old_belief + self._gamma * 1e24)
            
            # normalize the beliefs of the player
            player.beliefs = softmax(player.beliefs)


    def update_beliefs_after_night_vote(self, eliminated_id):
        """
        Updates beliefs of all agents after an elimination
        eliminated_id: int - ID of the eliminated player
        voters_dict: dict - Dictionary mapping voter IDs to their votes
        eliminated_type: str - "Werewolf" or "Villager"
        """

        # Update players' beliefs
        for player in self.alive.values():

            # If the player is the Little Girl and she cheated
            if isinstance(player, LittleGirl) and np.random.random() < player.p_focus and len(self.werewolves_id)>0:
                random_wolf_id = np.random.choice(self.werewolves_id)
                player.beliefs = np.ones_like(player.beliefs) * np.nan
                player.beliefs[random_wolf_id] = 1
            # Otherwise just take the new death into account
            else:
                player.beliefs[eliminated_id] = np.nan
                player.beliefs = softmax(player.beliefs)

           

    def day_shift(self):
        """
        During day shift, all players vote to eliminate one player.
        The player with most votes is eliminated.
        Returns the eliminated player or None if no one was eliminated.
        """
        # Collect votes from all players with voter IDs
        votes = {}
        for player in self.alive.values():
            votes[player.id] = player.vote()
        
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
            # print(f"werewolves_id: {self.werewolves_id}")
            # print(f"villagers_id: {self.villagers_id}")

            target_type = None
            dead_character = self.alive[eliminated_id]
            target_type, role = dead_character.type, dead_character.role
            
            if target_type == "Werewolf":
                self.eliminate_werewolf(eliminated_id)
            else:
                self.eliminate_villager(eliminated_id)

            # Update beliefs after elimination
            if target_type:
                self.update_beliefs_after_elimination(eliminated_id, votes, target_type)
            
            return eliminated_id, role
        
        return None

    def night_shift(self):
        """
        During night shift, werewolves collectively vote to eliminate one villager based on their combined beliefs
        Returns the ID of the eliminated villager or None if no one was eliminated
        """
        # Check if there are werewolves and villagers alive
        if len(self.werewolves) > 0 and len(self.villagers) > 0:
            # Sum up belief vectors of all werewolves
            combined_beliefs = np.zeros(self.num_players)
            for werewolf in self.werewolves.values():
                # Only consider beliefs for villagers
                for villager_id in self.villagers_id:
                    combined_beliefs[villager_id] += werewolf.beliefs[villager_id]
            
            # Find villagers with maximum combined belief value
            max_belief = np.max(combined_beliefs)
            candidates = np.where(combined_beliefs == max_belief)[0]
            # Filter candidates to only include alive villagers
            candidates = [c for c in candidates if c in self.villagers_id]
            
            if len(candidates) > 0:
                # Randomly select one among the candidates with highest belief
                eliminated_id = np.random.choice(candidates)
                eliminated_role = self.alive[eliminated_id].role
                self.eliminate_villager(eliminated_id)

                # update the beliefs to take the night shift into account
                self.update_beliefs_after_night_vote(eliminated_id)

                return eliminated_id, eliminated_role
            

        return None


if __name__ == "__main__":
    game = Game()
