import numpy as np
from typing import List, Dict, Optional, Tuple
import copy
import random
import os
from site_location import SiteLocationPlayer, Store, SiteLocationMap, euclidian_distances, attractiveness_allocation

class CDLCPlayer(SiteLocationPlayer):
    def place_stores(self, slmap: SiteLocationMap, 
                     store_locations: Dict[int, List[Store]],
                     current_funds: float):

      store_conf = self.config['store_config']

      #1-----find store type---
      #NEEED STORE TYPE
      # Choose largest store type possible:
      if current_funds >= store_conf['large']['capital_cost']:
          store_type = 'large'
      elif current_funds >= store_conf['medium']['capital_cost']:
          store_type = 'medium'
      else:
          store_type = 'small'
      
      #2-----Find the attractiveness values---
      sample_pos = []
      for x in range(10):
        for y in range(10):
          sample_pos.append((x*40,y*40))
      best_score = 0
      best_pos = []
      score = []
      for pos in sample_pos:
        sample_store = Store(pos, store_type)
        temp_store_locations = copy.deepcopy(store_locations)
        temp_store_locations[self.player_id].append(sample_store)
        sample_alloc = attractiveness_allocation(slmap, temp_store_locations, store_conf)
        sample_score = (sample_alloc[self.player_id] * slmap.population_distribution).sum()

        best_pos.append(pos)
        score.append(sample_score)
      sorted_score = sorted(score) # sorted rewards
      sorted_10 = sorted_score[-11:-1]

      # Get the state and indices
      '''
      rewardfile = "data/q_rewards.txt"
      rewards = correctingrewards(rewardfile)
      statefile = "data/q_states.txt"
      states = state_values(statefile)
      actionfile = "data/q_action.txt"
      actions = action_values(actionfile)
      q_table = q_table(states, actions, rewards)
      '''

      ansFile = open("data/MLdata.txt", 'r')
      lines = ansFile.readlines()
      # lines = data.split("\n")
      answer = {}
      for line in lines:
        num = line.split(" ")
        answer[int(num[0])]=[int(num[1]), int(num[2])]

      # Get indicies
      stores_num = len(store_locations)
      indices = answer[stores_num] # [2, 3]
      attract0 = sorted_10[indices[0]] #top 1 score
      attract1 = sorted_10[indices[1]] #top 2 score
      
      index0 = score.index(attract0)
      index1 = score.index(attract1)

      loc0 = best_pos[index0]
      loc1 = best_pos[index1]
      loc = best_pos[score.index(max(attract0, attract1))]

      if current_funds > (store_conf[store_type]['capital_cost'])*2:
        self.stores_to_place = [Store(loc0, store_type), Store(loc1, store_type)]
      else:
        self.stores_to_place = [Store(loc, store_type)]
      return