# Rubik_AI - A* v. 1.0
# Authors: Edoardo Pilia & Alessia Congia

import heapq
import rubik_ai as rb
from rubik_ai import execute_function_set

DEPTH_LIMIT = 21        # Depth Limit (It is demonstrated that every cube configuration is solved with 20 moves max.). Expanding over 20 move then is useless.

def elaborate(queue):    

    expanded = set()            # Tracks already expanded states (cubes). Checking if an element is in the set has a linear time complexity.

    while queue:                                              
            current = heapq.heappop(queue)                      # First element in the queue. Elements are ordered by the heuristic.

            if current.current not in expanded and current.depth < DEPTH_LIMIT: # Verifies if a node was already expanded

                print(f"Nodo aggiunto agli espansi n.{len(expanded)} - Nodi in coda: {len(queue)} - Profondità: {current.depth\
                            } - Euristica: {current.cube_heuristic()}")
                
                expanded.add(current.current)   # Adds the current cube to the expanded set

                if current.current == rb.target:
                    return current, len(expanded)        # Returns the list of expanded nodes

                if current.depth < DEPTH_LIMIT: # Checks if an element is over the limit before expanding it.
                    new_nodes = execute_function_set(current)       # Execute the function set to obtain all the possible nodes
                    for node in new_nodes:
                        heapq.heappush(queue, node) # Adds the new node in the queue, ordered by heuristic + length.
            
                        
    return None, len(expanded) # Return None a target is not found. A* is complete and optimal, if this happens most probably the configuration of the cube is not valid.