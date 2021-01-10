class NewPlayer1(SiteLocationPlayer):
    """
    Agent samples locations and selects the highest allocating one using
    the allocation function. 
    """
    def place_stores(self, slmap: SiteLocationMap, 
                     store_locations: Dict[int, List[Store]],
                     current_funds: float):
                         
        #get configuration
        store_conf = self.config['store_config']
        
        # get locations
        sample_pos = []
        for x in range(10):
            for y in range(10):
                sample_pos.append((x*20,y*20))
                
        # get largest store possible
        if current_funds >= store_conf['large']['capital_cost']:
            store_type = 'large'
        elif current_funds >= store_conf['medium']['capital_cost']:
            store_type = 'medium'
        else:
            store_type = 'small'


        best_pos = []
        # for small
        
        if store_type == 'small':
            
            best_score1 = 0
            best_score0 = 0
            sbest_pos = [0,0]
            
            for pos in sample_pos:
                sample_store = Store(pos, store_type)
                temp_store_locations = copy.deepcopy(store_locations)
                temp_store_locations[self.player_id].append(sample_store)
                sample_alloc = attractiveness_allocation(slmap, temp_store_locations, store_conf)
                sample_score = (sample_alloc[self.player_id] * slmap.population_distribution).sum()
                
                if sample_score > best_score1:
                    best_score1 = sample_score
                    sbest_pos[1] = pos   # best position
                    
                elif sample_score > best_score0 and sample_score <= best_score1:
                    best_score0 = sample_score
                    sbest_pos[0] = pos   # second nest position 

            print('small: HERE IS FINEEEEEE')  
            if current_funds < (store_conf['small']['capital_cost'])*2:
                print('ALSO HERE')
                best_pos = [sbest_pos[1]]
                print('ALSO HERE')
        
        # for medium
        if store_type == 'medium':
            
            #medium
            mbest_score = 0
            mbest_pos = []
            
            for pos in sample_pos:
                sample_store = Store(pos, store_type)
                temp_store_locations = copy.deepcopy(store_locations)
                temp_store_locations[self.player_id].append(sample_store)
                sample_alloc = attractiveness_allocation(slmap, temp_store_locations, store_conf)
                sample_score = (sample_alloc[self.player_id] * slmap.population_distribution).sum()
                if sample_score > mbest_score:
                    mbest_score = sample_score
                    mbest_pos = [pos]
                elif sample_score == mbest_score:
                    mbest_pos.append(pos)
                
            #small
            sbest_score1 = 0
            sbest_score0 = 0
            sbest_pos = [0,0]
            
            for pos in sample_pos:
                sample_store = Store(pos, 'small')
                temp_store_locations = copy.deepcopy(store_locations)
                temp_store_locations[self.player_id].append(sample_store)
                sample_alloc = attractiveness_allocation(slmap, temp_store_locations, store_conf)
                sample_score = (sample_alloc[self.player_id] * slmap.population_distribution).sum()
                
                if sample_score > sbest_score1:
                    sbest_score1 = sample_score
                    sbest_pos[1] = pos  # best position 
                    
                elif sample_score > sbest_score0 and sample_score <= sbest_score1:
                    sbest_score0 = sample_score
                    sbest_pos[0] = pos
                    
            print('medium: HERE IS FINEEEEEE')
            if (mbest_score > (sbest_score1 + sbest_score0) ):
                store_type = 'medium'
                print('ALSO HERE')
                best_pos = mbest_pos
                print('ALSO HERE')
            else:
                store_type = 'small'
                print('ALSO HERE')
                best_pos = sbest_pos
                print('ALSO HERE')
            print(store_type)
            print(best_pos)
        
        # for large
        if store_type == 'large':
            
            #large
            lbest_score1 = 0
            lbest_score0 = 0
            lbest_pos = [0,0]
            
            for pos in sample_pos:
                sample_store = Store(pos, store_type)
                temp_store_locations = copy.deepcopy(store_locations)
                temp_store_locations[self.player_id].append(sample_store)
                sample_alloc = attractiveness_allocation(slmap, temp_store_locations, store_conf)
                sample_score = (sample_alloc[self.player_id] * slmap.population_distribution).sum()
                
                if sample_score > lbest_score1:
                    lbest_score1 = sample_score
                    lbest_pos[1] = pos
                    
                elif sample_score > lbest_score0 and sample_score <= lbest_score1:
                    lbest_score0 = sample_score
                    lbest_pos[0] = pos
            
            #medium
            mbest_score1 = 0
            mbest_score0 = 0
            mbest_pos = [0,0]
            
            for pos in sample_pos:
                sample_store = Store(pos, 'medium')
                temp_store_locations = copy.deepcopy(store_locations)
                temp_store_locations[self.player_id].append(sample_store)
                sample_alloc = attractiveness_allocation(slmap, temp_store_locations, store_conf)
                sample_score = (sample_alloc[self.player_id] * slmap.population_distribution).sum()
                
                if sample_score > mbest_score1:
                    mbest_score1 = sample_score
                    mbest_pos[1] = pos
                    
                elif sample_score > mbest_score0 and sample_score <= mbest_score1:
                    mbest_score0 = sample_score
                    mbest_pos[0] = pos
            print("LARGE: HERE IS FINEEEEEEE")
            if (max(lbest_score0, lbest_score1) > (mbest_score1 + mbest_score0)):
                store_type = 'large'
                if current_fund > (store_conf['large']['capital_cost'])*2:
                    print('ALSO HERE')
                    best_pos = lbest_pos
                    print('ALSO HERE')
                else:
                    print('ALSO HERE')
                    best_pos = [lbest_pos[1]]
                    print('ALSO HERE')
            else:
                store_type = 'medium'
                print('ALSO HERE')
                best_pos = mbest_pos
                print('ALSO HERE')
        
        # max_alloc_positons = np.argwhere(alloc[self.player_id] == np.amax(alloc[self.player_id]))
        # pos = random.choice(max_alloc_positons)
        if len(best_pos) == 2:
            self.stores_to_place = [Store(best_pos[0], store_type), Store(best_pos[1], store_type)]
        else:
            self.stores_to_place = [Store(best_pos[0], store_type)]
        return