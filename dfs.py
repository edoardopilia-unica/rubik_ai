import time
import rubik_ai as rb
from rubik_ai import cube_node, execute_function_set
from pympler import asizeof
from collections import deque

DEPTH_LIMIT = 3        # Depth Limit (Recommended max. 5)
MEMORY_ALERT = 10e+9   # 1 GB

def elaborate(queue):
    expanded_list = []          # List of already expanded nodes
    expanded = set()            # Used to avoid re-iteration of the list while checking if a node was already been expanded. In addition, expanded list performs a check
                                # also over the parent node, while expanded takes into account only the cube

    while queue:                                             
            current = queue.popleft()                        # First element in the queue

            if current.current not in expanded and current.depth < DEPTH_LIMIT: # Verifies if a node was already expanded of it it over the depth limit

                size = asizeof.asizeof(expanded_list)/(MEMORY_ALERT) # Just an alert if the elaboration is taking too much memory

                print(f"{"!!! Dimensione coda: {size} > 1 GB !!! " if size > 1 \
                         else "" } Nodo aggiunto agli espansi n.{len(expanded_list)} - Nodi in coda: {len(queue)} - Profondità: {current.depth}")

                expanded_list.append(current)   # Adds the current node to the expanded list
                expanded.add(current.current)   # Adds the current cube to the expanded set
                
                if current.current == rb.target:
                    return expanded_list
                
                new_nodes = execute_function_set(current)       # Execute the function set to obtain all the possible nodes

                for node in new_nodes:
                    queue.appendleft(node)  # Adds the new node as the first in the queue

    return None # Return None a target is not found.


def main():

    start_time = time.time()
    
    # List of operations to scramble the cube
    my_cube = rb.cube.create_target()
    my_cube = my_cube.rotate_red_column(False, True)


    root = cube_node(my_cube, None) # Defines the root node as the scrambled configuration and None as a parent


    iteration = 0
    queue = deque([root])

    expanded_list = elaborate(queue)

    elab_time = time.time()
    print("-"*30 )


    if expanded_list is None:
        print("Target non trovato")
    else:
        iteration = len(expanded_list)
        print(f"Percorso effettuato")
        path = []
        current_node = expanded_list.pop()
        while current_node is not None:

            path.append(current_node.current)
            current_node = current_node.parent
    
        for cube in path[::-1]:
            index = path[::-1].index(cube)
            cube.print(f"Nodo {"root" if index == 0 else f"n°{index}"}")

    print("-"*30 )                       
    print(f"Tempo di elaborazione: {(elab_time-start_time)}. s --- N° nodi espansi: {iteration}")
    print("-"*30 )
    print(f"Consumo memoria")
    print(f"Nodi espansi: {asizeof.asizeof(expanded_list)/1000} KB --- Coda rimanente: {asizeof.asizeof(queue)/1000} KB - Lunghezza coda: {len(queue)}")

if __name__=="__main__":
    main()
