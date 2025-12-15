# Rubik_AI - DFS v. 1.0
# Authors: Edoardo Pilia & Alessia Congia

import rubik_ai as rb
from rubik_ai import execute_function_set

DEPTH_LIMIT = 6    # Depth Limit (Recommended max. 6)


def elaborate(queue, depth_limit=DEPTH_LIMIT):
    expanded = {}            # Tracks already expanded states (cubes). Checking if an element is in the set has a linear time complexity.

    while queue:                                             
            current = queue.pop()                        # First element in the queue

            if current.current in expanded and expanded[current.current] < current.depth: # Verifies if a node was already expanded at a minor depth
                continue
            else:
                print(f"Expanded node n.{len(expanded)} - Queued: {len(queue)} - Depth: {current.depth}")

                expanded[current.current] = current.depth   # Adds the current cube to the expanded set
                
                if current.current == rb.target:
                    return current, len(expanded)

                if current.depth < depth_limit:
                    new_nodes = execute_function_set(current)       # Execute the function set to obtain all the possible nodes
                    for node in new_nodes:
                        queue.append(node)  # Adds the new node a the beginning of the queue, it will be expanded as first.

                

    return None, len(expanded) # Return None a target is not found.
