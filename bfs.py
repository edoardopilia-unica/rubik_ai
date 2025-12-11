import rubik_ai as rb
from rubik_ai import execute_function_set

def elaborate(queue):

    expanded = set()            # Tracks already expanded states (cubes). Checking if an element is in the set has a linear time complexity.
    visited = set()             # Used to avoid to re-add a cube in the queue.

    while queue:                                              
            current = queue.popleft()                         

            if current.current not in expanded: # Verifies if a node was already expanded

                print(f"Expanded node n.{len(expanded)} - Queued: {len(queue)} - Depth: {current.depth}")
                
                expanded.add(current.current) # Adds the current cube to the expanded set
                
                new_nodes = execute_function_set(current)

                for node in new_nodes:
                    if node.current not in visited: 
                        queue.append(node)                    # Nodes are inserted at the end of the queue
                        visited.add(node.current)             
                        
                if current.current == rb.target: # Checks if current node is the target
                    return current, len(expanded)
                
    return None, len(expanded) # Return None a target is not found. BFS is complete, if this happens most probably the configuration of the cube is not valid.

