import time
import rubik_ai as rb
from rubik_ai import cube_node, execute_function_set
from pympler import asizeof
from collections import deque

DEPTH_LIMIT = 8    # Depth Limit (Recommended max. 5)


def elaborate(queue):
    expanded = set()            # Tracks already expanded states (cubes). Checking if an element is in the set has a linear time complexity.

    while queue:                                             
            current = queue.popleft()                        # First element in the queue

            if current.current not in expanded: # Verifies if a node was already expanded.

                print(f"Expanded node n.{len(expanded)} - Queued: {len(queue)} - Depth: {current.depth}")

                expanded.add(current.current)   # Adds the current cube to the expanded set
                                
                if current.depth < DEPTH_LIMIT:
                    new_nodes = execute_function_set(current)       # Execute the function set to obtain all the possible nodes
                    for node in new_nodes:
                        queue.appendleft(node)  # Adds the new node a the beginning of the queue, it will be expanded as first.

                if current.current == rb.target:
                    return current, len(expanded)
                

    return None, len(expanded) # Return None a target is not found.
