import rubik_ai as rb
from rubik_ai import G,R,O,Y,B,W

faces_data = [
        rb.face(rb.create_matrix(B,R,R,B,R,R,B,R,R)), # Red
        rb.face(rb.create_matrix(R,R,W,G,G,W,G,G,W)), # 1: Green
        rb.face(rb.create_matrix(R,G,G,Y,Y,Y,Y,Y,Y)), # 2: Yellow
        rb.face(rb.create_matrix(G,O,O,G,B,B,G,B,B)), # 3: Blue
        rb.face(rb.create_matrix(W,W,W,W,W,W,O,B,B)), # White
        rb.face(rb.create_matrix(G,G,G,O,O,O,O,O,O))  # 5: Orange
]


def execute_function_set(node, visited):
    for p1 in [False, True]:
        for p2 in [False, True]:
            rrc = node.rotate_red_column(p1,p2)
            if rrc not in visited: visited.append(rrc)
            else: print("alr")
            rrr = node.rotate_red_row (p1, p2)
            if rrr not in visited: visited.append(rrr)
            else: print("alr")
            rf = node.rotate_face(p1,p2)
            if rf not in visited: visited.append(rf)
            else: print("alr")

def main():
    faces_data_ = [
        rb.face(rb.create_matrix(B,B,B,R,R,R,R,R,R)), # Red
        rb.face(rb.create_matrix(R,R,R,G,G,G,G,G,G)), # 1: Green
        rb.face(rb.create_matrix(Y,Y,Y,Y,Y,Y,Y,Y,Y)), # 2: Yellow
        rb.face(rb.create_matrix(O,O,O,B,B,B,B,B,B)), # 3: Blue
        rb.face(rb.create_matrix(W,W,W,W,W,W,W,W,W)), # White
        rb.face(rb.create_matrix(G,G,G,O,O,O,O,O,O))  # 5: Orange
]

    faces_data = [
        rb.face(rb.create_matrix(W,B,B,R,R,R,R,R,R)), # Red
        rb.face(rb.create_matrix(R,R,R,G,G,Y,G,G,Y)), # 1: Green
        rb.face(rb.create_matrix(B,B,B,Y,Y,Y,Y,Y,Y)), # 2: Yellow
        rb.face(rb.create_matrix(O,O,O,W,B,B,W,B,B)), # 3: Blue
        rb.face(rb.create_matrix(G,W,W,G,W,W,G,W,W)), # White
        rb.face(rb.create_matrix(G,G,Y,O,O,O,O,O,O))  # 5: Orange
]

    my_cube = rb.cube(faces_data)
    visited_list = [my_cube]
    expanded_list = []
    execute_function_set(my_cube, visited_list)
    expanded_list.append(my_cube)
    index = 1
    iteration = 0
    for visited in visited_list:
        #if iteration > 300: break
        if visited == rb.target:
            print("Target ottenuto")
            expanded_list.append(visited)
            break
        if visited not in expanded_list:
            execute_function_set(visited, visited_list)
            expanded_list.append(visited)
            print(f"Insertion in expanded n.{iteration}/{len(visited_list)}")
            index += 1
        iteration+=1

    print("Lista nodi espansi")
    for node in expanded_list:
        rb.print_cube_state(node, expanded_list.index(node))

if __name__=="__main__":
    main()

