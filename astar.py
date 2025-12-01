import time
import heapq
import rubik_ai as rb
from rubik_ai import cube_node, execute_function_set
from pympler import asizeof


DEPTH_LIMIT = 21        # Depth Limit (Recommended max. 5)
MEMORY_ALERT = 10e+9    # 1 GB


def elaborate(queue):    
    expanded_list = []          # List of expanded nodes
    expanded = set()            # Used to avoid re-iteration of the list while checking if a node was already been expanded. In addition, expanded list performs a check
                                # also over the parent node, while expanded takes into account only the cube.

    visited = set()             # Used to avoid to re-add elements in the queue.

    while queue:                                              
            current = heapq.heappop(queue)                      # First element in the queue

            if current.current not in expanded and current.depth < DEPTH_LIMIT: # Verifies if a node was already expanded of it it over the depth limit

                size = asizeof.asizeof(expanded_list)/MEMORY_ALERT             # Just an alert if the elaboration is taking too much memory

                print(f"{"!!! Dimensione coda: {size} > 1 GB !!! " if size > 1 \
                         else "" } Nodo aggiunto agli espansi n.{len(expanded_list)} - Nodi in coda: {len(queue)} - Profondità: {current.depth\
                            } - Euristica: {current.cube_heuristic()}")

                expanded_list.append(current)   # Adds the current node to the expanded list
                expanded.add(current.current)   # Adds the current cube to the expanded set
                
                if current.current == rb.target:
                    return expanded_list        # Returns the list of expanded nodes
                
                new_nodes = execute_function_set(current)       # Execute the function set to obtain all the possible nodes

                for node in new_nodes:
                    if node.current not in visited:
                        heapq.heappush(queue, node) # Adds the new node in the queue, ordered by the the heuristic + length
                        visited.add(node.current)
            
    return None # Return None a target is not found. A* is complete and optimal, if this happens most probably the configuration of the cube is not valid.


def main():

    start_time = time.time()
    
    # List of operations to scramble the cube
    my_cube = rb.cube.create_target()

    my_cube = my_cube.rotate_red_row(False, True, False)     # Riga alta
    my_cube = my_cube.rotate_red_column(True, True, False)   # Colonna destra
    my_cube = my_cube.rotate_face(False, True, True)         # Faccia rossa (doppia)
    my_cube = my_cube.rotate_red_row(True, False, False)     # Riga bassa
    my_cube = my_cube.rotate_red_column(False, False, True)  # Colonna sinistra (doppia)
    my_cube = my_cube.rotate_face(True, False, False)        # Faccia arancione
    my_cube = my_cube.rotate_red_row(False, True, True)      # Riga alta (doppia)
    my_cube = my_cube.rotate_red_column(True, True, False)   # Colonna destra

    root = cube_node(my_cube, None)

    queue = [root]
  
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

