import numpy as np
from typing import List, Dict, Optional, Tuple
import copy

from site_location import SiteLocationPlayer, Store, SiteLocationMap, euclidian_distances, attractiveness_allocation

class LogicalPlayer(SiteLocationPlayer):
    """
    
    """
    def place_stores(self, slmap: SiteLocationMap, 
                     store_locations: Dict[int, List[Store]],
                     current_funds: float):
        print ("hi")


