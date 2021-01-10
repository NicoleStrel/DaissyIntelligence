import numpy as np
from typing import List, Dict, Optional, Tuple
import copy
import random
import os
import math
from site_location import SiteLocationPlayer, Store, SiteLocationMap, euclidian_distances, attractiveness_allocation

#https://repl.it/join/rqtofedp-nicole799

class QPlayer(SiteLocationPlayer):
    def place_stores(self, slmap: SiteLocationMap, 
                     store_locations: Dict[int, List[Store]],
                     current_funds: float):

      store_conf = self.config['store_config']
      
      #1 ------------ build q table  --------------------
      #find num stores on map
      num_stores=0
      for player, player_stores in store_locations.items():
        num_stores= num_stores + len(player_stores)
      print ("num stores",num_stores) 
      
      # read choices and top_10
      file = open(os.path.join(os.path.dirname(__file__),"data/Q_player_current_data.txt"),"r")
      lines = file.readlines()
      if (lines!= []):
        indicies=lines[0].split(" ")
        build_q_table(indicies[0], indicies[1], num_stores, current_funds) #for previous round
      file.close()
     
      #2 -----Find list of best choices randomly---
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
      attractives=[]
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
      end=9
      top_10= sorted_list[:end]
      '''
      #throw away points that are in store_type range from each other
      indicies=[]
      for i in range(0, len(top_10)):
        for j in range(0, len(top_10)):
          if j not in indicies:
            distance=euclidean_distance(top_10[i][0], top_10[j][0])
            if (distance < store_conf[store_type]['attractiveness']/2):
              indicies.append(j)
              break #look at next pair 
 
      #remove indicies
      end=end+1
      for idx in indicies:
        top_10.pop(idx)
        top_10.append(sorted_list[end])
        end=end+1
      '''
      #print (top_10) #tuple of a tuple  
      
      #3 - randomly choose 2 stores- temporary
      choices = random.sample(top_10, 2)
      index1 = top_10.index(choices[0])
      index2 = top_10.index(choices[1])

      # write choices and top_10
      f = open(os.path.join(os.path.dirname(__file__),"data/Q_player_current_data.txt"),"w")
      f.write (str(index1) +' '+ str(index2))
      f.close()

      #4 - make selection
      # sample_score <- close to each other, not give right value, doesn't account for overlap
      if choices[0][1]+ choices[1][1] > current_funds: 
        print("only 1") 
        #make most attractive selection
        if (choices[0][1]>=choices[1][1]):
          self.stores_to_place = [Store(choices[0][0], store_type)]
        else:
          self.stores_to_place = [Store(choices[1][0], store_type)]
      else: #make both selections
          print("both")
          selection.append(Store(choices[0][0], store_type))
          selection.append(Store(choices[1][0], store_type))
          self.stores_to_place = selection
      return

def euclidean_distance (p1, p2):
    return math.sqrt(((p1[0]-p2[0])**2)+((p1[1]-p2[1])**2) )

def build_q_table(index1, index2, num_of_stores, current_funds):
    action = [index1, index2]
    state = num_of_stores
    reward = current_funds
    qstates = open(os.path.join(os.path.dirname(__file__),"data/q_states.txt"), "a")
    qstates.write(str(state))
    qstates.write("\n")
    qstates.close()

    qaction = open(os.path.join(os.path.dirname(__file__),"data/q_actions.txt"), "a")
    qaction.write(" ".join(action))
    qaction.write("\n")
    qaction.close()

    qreward = open(os.path.join(os.path.dirname(__file__),"data/q_rewards.txt"), "a")
    qreward.write(str(reward))
    qreward.write("\n")
    qreward.close()
    return