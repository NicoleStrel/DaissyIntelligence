import numpy as np
from typing import List, Dict, Optional, Tuple
import copy
import random
from site_location import SiteLocationPlayer, Store, SiteLocationMap, euclidian_distances, attractiveness_allocation


class NewPlayer(SiteLocationPlayer):
    def place_stores(self, slmap: SiteLocationMap, 
                     store_locations: Dict[int, List[Store]],
                     current_funds: float):
        store_conf = self.config['store_config']
        sample_pos = []

        # Choose largest store type possible:
        if current_funds >= store_conf['large']['capital_cost']:
            store_type = 'large'
        elif current_funds >= store_conf['medium']['capital_cost']:
            store_type = 'medium'
        else:
            store_type = 'small'
        
        #try to delete all taken points and radius?
        # use store_locations 
        # store_conf[store_type]['attractiveness']
        coords = [(x,y) for x in range(20) for y in range(20)]
        all_stores_pos = []
        for player, player_stores in store_locations.items():
            for player_store in player_stores:
                all_stores_pos.append(player_store.pos)
                # need to add radius 
                r=store_conf[store_type]['attractiveness']
                radcircle=player_store.pos[0]**2 + player_store.pos[1]**2
                a= np.array(coord)
                b = np.where(radcircle < r)
                
        sample_pos= set(coords).symmetric_difference(all_stores_pos)
        #print ("sample pos: ",sample_pos)


        best_score = 0
        best_pos = []
        for pos in sample_pos:
            sample_store = Store(pos, store_type)
            temp_store_locations = copy.deepcopy(store_locations)
            temp_store_locations[self.player_id].append(sample_store)
            sample_alloc = attractiveness_allocation(slmap, temp_store_locations, store_conf)
            sample_score = (sample_alloc[self.player_id] * slmap.population_distribution).sum()
            if sample_score > best_score:
                best_score = sample_score
                best_pos = [pos]
            elif sample_score == best_score:
                best_pos.append(pos)
        print("best pos: " + str(best_pos))

        # max_alloc_positons = np.argwhere(alloc[self.player_id] == np.amax(alloc[self.player_id]))
        # pos = random.choice(max_alloc_positons)
        self.stores_to_place = [Store(random.choice(best_pos), store_type)]
        return