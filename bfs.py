import rubik_ai as rb
from rubik_ai import G,R,O,Y,B,W
from concurrent.futures import ThreadPoolExecutor, as_completed
import itertools
from collections import deque
import time

faces_data = [
        rb.face(rb.create_matrix(B,R,R,B,R,R,B,R,R)), # Red
        rb.face(rb.create_matrix(R,R,W,G,G,W,G,G,W)), # 1: Green
        rb.face(rb.create_matrix(R,G,G,Y,Y,Y,Y,Y,Y)), # 2: Yellow
        rb.face(rb.create_matrix(G,O,O,G,B,B,G,B,B)), # 3: Blue
        rb.face(rb.create_matrix(W,W,W,W,W,W,O,B,B)), # White
        rb.face(rb.create_matrix(G,G,G,O,O,O,O,O,O))  # 5: Orange
]

working = [
        rb.face(rb.create_matrix(W,B,B,R,R,R,R,R,R)), # Red
        rb.face(rb.create_matrix(R,R,R,G,G,Y,G,G,Y)), # 1: Green
        rb.face(rb.create_matrix(B,B,B,Y,Y,Y,Y,Y,Y)), # 2: Yellow
        rb.face(rb.create_matrix(O,O,O,W,B,B,W,B,B)), # 3: Blue
        rb.face(rb.create_matrix(G,W,W,G,W,W,G,W,W)), # White
        rb.face(rb.create_matrix(G,G,Y,O,O,O,O,O,O))  # 5: Orange
]






def execute_function_set(node):
    new_nodes = set()
    boolean_pairs = list(itertools.product([False, True], repeat=2))
    futures = []

    #threading executor
    with ThreadPoolExecutor(max_workers=12) as executor:
        for p1, p2 in boolean_pairs:

            futures.append(executor.submit(node.rotate_red_column, p1, p2))
            futures.append(executor.submit(node.rotate_red_row, p1, p2))
            futures.append(executor.submit(node.rotate_face, p1, p2))
            
        #esecuzione funzioni
        for future in as_completed(futures):
            result = future.result() # Qui otteniamo il nodo ruotato
            new_nodes.add(result)

    return new_nodes

def elaborate(queue, iteration, debug=False):
    expanded_list = []
    visited = set()
    target_iteration = 0
    iteration = 0
    first_time = True
    while queue:
            current = queue.popleft()

            if current not in expanded_list: 
                new_nodes = execute_function_set(current)
                for node in new_nodes:
                    if node not in visited: 
                        queue.append(node)
                        visited.add(node)
                expanded_list.append(current)
                if current == rb.target:
                    rb.print_cube_state(current, "")
                    return expanded_list, iteration
                print(f"Insertion in expanded n.{iteration}/{len(queue)}")
                if (first_time): target_iteration+=1
            if rb.target in visited and debug: 
                print(f"Target individuato in lista - Espansione nodo: {target_iteration}")
                first_time = False
                
            iteration+=1

def main():

    faces_data = [
        rb.face(rb.create_matrix(B,B,B,R,R,R,B,B,B)), # 0: Red
        rb.face(rb.create_matrix(R,R,R,G,G,G,R,R,R)), # 1: Green
        rb.face(rb.create_matrix(Y,Y,Y,Y,Y,Y,Y,Y,Y)), # 2: Yellow
        rb.face(rb.create_matrix(O,O,O,B,B,B,O,O,O)), # 3: Blue
        rb.face(rb.create_matrix(W,W,W,W,W,W,W,W,W)), # 4: White
        rb.face(rb.create_matrix(G,G,G,O,O,O,G,G,G))  # 5: Orange
    ]

    start_time = time.time()
    

    my_cube = rb.cube(faces_data)
    my_cube = my_cube.rotate_face(False, False)
    my_cube = my_cube.rotate_red_column(True, False)
    #my_cube = my_cube.rotate_red_row(False, False)
    #my_cube = my_cube.rotate_red_column(True, False)
    #my_cube = my_cube.rotate_red_column(False, True)
    #my_cube = my_cube.rotate_face(True, False)
    rb.print_cube_state(rb.target, "")
    debug = True
    
       

    iteration = 0
    queue = deque([my_cube])

    expanded_list, iteration = elaborate(queue, iteration, debug)
    
    elab_time = time.time()


    print(f"Lista nodi espansi: n. iterazioni: {iteration}")
    for node in expanded_list:
        rb.print_cube_state(node, "")
    
    print(f"Tempo di elaborazione: {(elab_time-start_time)}. s --- N° nodi espansi: {iteration}")
    

if __name__=="__main__":
    main()

