import rubik_ai as rb
from rubik_ai import G,R,O,Y,B,W
from concurrent.futures import ThreadPoolExecutor, as_completed
import itertools
from collections import deque
from pympler import asizeof

import time

class cube_node:
    def __init__(self, current, parent):
        self.current = current                   # Cubo corrente
        self.parent = parent                     # Nodo genitore (per risalire al percorso che conduce alla soluzione) 


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

            futures.append(executor.submit(node.current.rotate_red_column, p1, p2))  # Rotazioni colonna
            futures.append(executor.submit(node.current.rotate_red_row, p1, p2))     # Rotazioni riga
            futures.append(executor.submit(node.current.rotate_face, p1, p2))        # Rotazioni faccia
            
        #esecuzione funzioni
        for future in as_completed(futures):
            result = future.result()                # Qui otteniamo il nodo ruotato
            new_node = cube_node(result, node)
            new_nodes.add(new_node)

    return new_nodes

def elaborate(queue, debug=False):
    expanded_list = []          # Nodi già espansi (nodi interni all'albero di ricerca)
    visited = set()             # Nodi visitati (nodi interni + nodi foglia)
    target_iteration = 0
    first_time = True
    while queue:                                              # Valutazione che la coda non sia vuota
            current = queue.popleft()                         # Estrazione del primo elemento in coda (nel bfs, il nodo più superficiale)

            if current not in expanded_list: 
                new_nodes = execute_function_set(current)     # Espansione del nodo
                for node in new_nodes:
                    if node.current not in visited: 
                        queue.append(node)                    # I nuovi nodi vengono aggiunti alla fine della coda
                        visited.add(node.current)             # e aggiunti alla lista dei nodi visitati 
                expanded_list.append(current)                 # Il nodo che è stato espanso viene aggiunto alla lista dei nodi espansi
                if current.current == rb.target:
                    return expanded_list, len(expanded_list)
                print(f"Nodo aggiunto agli espansi n.{len(expanded_list)} - Nodi in coda: {len(queue)}")
                if (first_time): target_iteration+=1
            if rb.target in visited and debug: 
                print(f"Target individuato in lista - Espansione nodo: {target_iteration}")
                first_time = False
                

def main():

    faces_data = [
        rb.face(rb.create_matrix(Y,B,Y,Y,R,Y,O,B,O)), # 0: Red
        rb.face(rb.create_matrix(G,G,R,B,G,R,G,Y,Y)), # 1: Green
        rb.face(rb.create_matrix(G,Y,G,G,Y,G,W,O,O)), # 2: Yellow
        rb.face(rb.create_matrix(O,O,B,O,B,G,W,W,B)), # 3: Blue
        rb.face(rb.create_matrix(Y,R,R,R,W,R,B,W,B)), # 4: White
        rb.face(rb.create_matrix(W,W,R,O,O,O,W,W,R))  # 5: Orange
    ]

    start_time = time.time()
    

    my_cube = rb.create_target()
    my_cube = my_cube.rotate_red_column(False, True)
    my_cube = my_cube.rotate_red_row(False, True)
    my_cube = my_cube.rotate_red_column(False, False)
    #12my_cube = my_cube.rotate_face(False, False)
    #my_cube = my_cube.rotate_red_column(True, False)
    my_cube = my_cube.rotate_red_row(False, False)
    #my_cube = my_cube.rotate_red_column(True, False)
    #my_cube = my_cube.rotate_red_column(False, True)
    #my_cube = my_cube.rotate_face(True, False)
    rb.print_cube_state(my_cube, "Nodo root")
    debug = False
    
    #if debug: return

    root = cube_node(my_cube, None)

    iteration = 0
    queue = deque([root])

    expanded_list, iteration = elaborate(queue, debug)
    
    elab_time = time.time()


    if debug: print(f"Lista nodi espansi: n. iterazioni: {iteration}")
    #if debug:
        #for node in expanded_list :
            #rb.print_cube_state(node.current, "")
    print("-"*60 )
    print(f"Percorso effettuato")
    path = []
    current_node = expanded_list.pop()
    while current_node is not None:
        #rb.print_cube_state(current_node.current, "")
        path.append(current_node.current)
        current_node = current_node.parent
    
    for cube in path[::-1]:
        index = path[::-1].index(cube)
        rb.print_cube_state(cube, f"Nodo {"root" if index == 0 else f"n°{index}"}")
                            
    print(f"Tempo di elaborazione: {(elab_time-start_time)}. s --- N° nodi espansi: {iteration}")
    print("-"*30 )
    print(f"Consumo memoria")
    print(f"Nodi espansi: {asizeof.asizeof(expanded_list)/1000} KB --- Coda rimanente: {asizeof.asizeof(queue)/1000} KB")

if __name__=="__main__":
    main()
