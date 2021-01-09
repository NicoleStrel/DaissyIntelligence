import numpy as np
from typing import List, Dict, Optional, Tuple
import copy
import random
from site_location import SiteLocationPlayer, Store, SiteLocationMap, euclidian_distances, attractiveness_allocation


class QPlayer(SiteLocationPlayer):
   def place_stores(self, slmap: SiteLocationMap, 
                     store_locations: Dict[int, List[Store]],
                     current_funds: float):
    store_conf = self.config['store_config']
    #1 -----Find list of best choices randomly---

    #NEEED STORE TYPE
    # Choose largest store type possible:
    if current_funds >= store_conf['large']['capital_cost']:
        store_type = 'large'
    elif current_funds >= store_conf['medium']['capital_cost']:
        store_type = 'medium'
    else:
        store_type = 'small'

    #random 100 and find score
    sample_pos_and_scores = []
    num_rand = 100
    for i in range(num_rand):
      x = random.randint(0, slmap.size[0])
      y = random.randint(0, slmap.size[1])
      pos=(x,y)
      sample_store = Store(pos, store_type)
      temp_store_locations = copy.deepcopy(store_locations)
      temp_store_locations[self.player_id].append(sample_store)
      sample_alloc = attractiveness_allocation(slmap, temp_store_locations, store_conf)
      sample_score = (sample_alloc[self.player_id] * slmap.population_distribution).sum()
      sample_pos_and_scores.append((pos,sample_score))

    #sort and find max 10
    sorted_list=sorted(sample_pos_and_scores,key=lambda x: x[1], reverse=True)
    top_10= sorted_list[:9]
    print (top_10) #tuple of a tuple  
   
    #2 - randomly choose 2 stores- temporary

    #3 - build q table 
    #4

    return