import bfs
import dfs
import astar
import rubik_ai as rb
from rubik_ai import cube_node
import time
from pympler import asizeof
from collections import deque


def main():

# Write the desired configuration below:
# --- TEST 2 MOSSE (R U) ---
    my_cube = rb.cube.create_target()
    my_cube = my_cube.rotate_red_column(False, True, False)  # R
    my_cube = my_cube.rotate_red_row(False, True, False)     # U

    root = cube_node(my_cube, None) # Defines the root node as the scrambled configuration and None as a parent
    algorithms = input("Choose an algorithm: BFS (1), DFS (2), A* (3): ")
    start_time = time.time()
    try:
        if algorithms == '1':
            current_node, iteration, queue = execute_algorithm('bfs', root)
        if algorithms == '2':
            current_node, iteration, queue = execute_algorithm('dfs', root)
        if algorithms == '3':
            current_node, iteration, queue = execute_algorithm('astar', root)
    except Exception as err:
        print(f"Caught exception")
        print(f"Info: {err=}, {type(err)=}")
        print("Retrying...")
        main()
    except KeyboardInterrupt:
        elab_time = time.time()
        print("-"*30 )
        print("Program interrupted by user")
        print(f"Elapsed time: {(elab_time-start_time)} s")
        print("Goodbye")
        exit()


    elab_time = time.time()
    print("-"*30 )

    if current_node is None:
        print("Target non found")
    else:
        print(f"Path: ")
        path = []
        while current_node is not None:

            path.append(current_node.current)
            current_node = current_node.parent
    
        for cube in path[::-1]:
            index = path[::-1].index(cube)
            cube.print(f"{"Root node" if index == 0 else f"Node n°{index}"}")

    print("-"*30 )                       
    print(f"Elapsed time: {round(elab_time-start_time, 3)} s")
    print("-"*30 )
    print(f"Memory Consumption: ")
    print(f"N° expanded node: {iteration} --- Queue size: {asizeof.asizeof(queue)/1000} KB - Queue length: {len(queue)}")


    

def execute_algorithm(algorithm, root):

    if algorithm == 'bfs':
        queue = deque([root])             
        current_node, iteration = bfs.elaborate(queue)
    elif algorithm == 'dfs':
        queue = deque([root])
        current_node, iteration = dfs.elaborate(queue)
    elif algorithm == 'astar':
        queue = [root]
        current_node, iteration = astar.elaborate(queue)
    else:
        raise Exception("Algorithm not found")
   
    return current_node, iteration, queue

if __name__=="__main__":
    main()


