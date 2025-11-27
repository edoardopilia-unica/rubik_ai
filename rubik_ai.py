# rubik_ai v. 0.1
# authors Edoardo Pilia & Alessia Congia

import copy

G = 'G'     # G as 'green'
Y = 'Y'     # Y as 'yellow'
W = 'W'     # W as 'white'
B = 'B'     # B as 'blue'
R = 'R'     # R ad 'red'
O = 'O'     # O as 'orange'



class face:
    center_index = 1

    def __init__(self, matrix):
        self.matrix = matrix                        # describing each face as a matrix
        pass
    
    def switch_row(self, index, row):
        if index == self.center_index: return -1    # cannot switch the central row
        self.matrix[index] = row
    
    def switch_column(self, index, column):
        if index == self.center_index: return -1    # cannot switch the central column
        self.matrix[0][index] = column[0]
        self.matrix[1][index] = column[1]
        self.matrix[2][index] = column[2]
        
    
    def rotate(self, backward):
        row0 = copy.copy(self.matrix[0])
        row2 = copy.copy(self.matrix[2])
        column0 = copy.copy(self.get_column(0))
        column2 = copy.copy(self.get_column(2))
        if backward:                                   # anticlockwise face rotation
            self.switch_column(0, row0[::-1])
            self.switch_row(0, column2)
            self.switch_column(2, row2[::-1])
            self.switch_row(2, column0) 
        else:                                           # clockwise face rotation
            self.switch_row(0, column0[::-1])
            self.switch_column(2, row0)
            self.switch_row(2, column2[::-1])
            self.switch_column(0, row2)
            

    
    def get_column(self, index):
        return [self.matrix[0][index], self.matrix[1][index], self.matrix[2][index]]
        
    def get_row(self, index):
        return self.matrix[index]

    def __eq__(self, other):
        result = (self.matrix[0] == other.matrix[0] and self.matrix[1] == other.matrix[1] and self.matrix[2] == other.matrix[2])
        return result
    
    def __ne__(self, other):
        return not self.__eq__(other)

class cube:

    def __eq__(self, other):
        if isinstance(other, type(self)):
            return (
            self.red_face    == other.red_face and
            self.green_face  == other.green_face and
            self.yellow_face == other.yellow_face and
            self.blue_face   == other.blue_face and
            self.white_face  == other.white_face and
            self.orange_face == other.orange_face
        )
        else: 
            return False
    
    def __ne__(self, other):
            return not self.__eq__(other)


    def __init__(self, faces):
        self.red_face = faces[0]     #red
        self.green_face = faces[1]   #green
        self.yellow_face = faces[2]  #yellow
        self.blue_face = faces[3]    #blue
        self.white_face = faces[4]   #white
        self.orange_face = faces[5]  #orange

    # All rotations refer to the red face
  
    def rotate_red_column(self, backward, right):
        return_cube = copy.deepcopy(self)
        index =  2 if right else 0
        op_idx = 0 if right else 2       # opposite index for orange face
        if right: return_cube.blue_face.rotate(not(backward))
        else: return_cube.green_face.rotate(backward)

        if backward:
            return_cube.red_face.switch_column(index, self.yellow_face.get_column(index))
            return_cube.yellow_face.switch_column(index, self.orange_face.get_column(op_idx)[::-1])
            return_cube.orange_face.switch_column(op_idx, self.white_face.get_column(index)[::-1])
            return_cube.white_face.switch_column(index, self.red_face.get_column(index))
        else:
            return_cube.red_face.switch_column(index, self.white_face.get_column(index))
            return_cube.white_face.switch_column(index, self.orange_face.get_column(op_idx)[::-1])
            return_cube.orange_face.switch_column(op_idx, self.yellow_face.get_column(index)[::-1])
            return_cube.yellow_face.switch_column(index, self.red_face.get_column(index))
        return return_cube

    def rotate_red_row(self, backward, up):      
        return_cube = copy.deepcopy(self)
        index = 0 if up else 2
        if up: return_cube.white_face.rotate(not(backward))
        else: return_cube.yellow_face.rotate(backward)

        if backward:
            return_cube.red_face.switch_row(index, self.blue_face.get_row(index))
            return_cube.blue_face.switch_row(index, self.orange_face.get_row(index))
            return_cube.orange_face.switch_row(index, self.green_face.get_row(index))
            return_cube.green_face.switch_row(index, self.red_face.get_row(index))
        else:
            return_cube.red_face.switch_row(index, self.green_face.get_row(index))
            return_cube.green_face.switch_row(index, self.orange_face.get_row(index))
            return_cube.orange_face.switch_row(index, self.blue_face.get_row(index))
            return_cube.blue_face.switch_row(index, self.red_face.get_row(index))
        return return_cube

    def rotate_face(self, red, backward):
        return_cube = copy.deepcopy(self)
        index = 2 if red else 0
        op_idx = 0 if red else 2
        if red: return_cube.red_face.rotate(backward)
        else: 
            return_cube.orange_face.rotate(not backward)   

        if backward:
            return_cube.white_face.switch_row(index, self.blue_face.get_column(op_idx))
            return_cube.blue_face.switch_column(op_idx, self.yellow_face.get_row(op_idx)[::-1])
            return_cube.yellow_face.switch_row(op_idx, self.green_face.get_column(index))
            return_cube.green_face.switch_column(index, self.white_face.get_row(index)[::-1])

        else:
            return_cube.white_face.switch_row(index, self.green_face.get_column(index)[::-1])
            return_cube.green_face.switch_column(index, self.yellow_face.get_row(op_idx))
            return_cube.yellow_face.switch_row(op_idx, self.blue_face.get_column(op_idx)[::-1])
            return_cube.blue_face.switch_column(op_idx, self.white_face.get_row(index))
        return return_cube
    
    def faces(self):
        return [ self.red_face,
        self.green_face ,
        self.yellow_face,
        self.blue_face,
        self.white_face,
        self.orange_face]

    def __hash__(self):
        # Convertiamo le matrici (liste di liste) in tuple di tuple per renderle immutabili e "hashabili"
        def to_tuple(matrix):
            return tuple(tuple(row) for row in matrix)
            
        return hash((
            to_tuple(self.red_face.matrix),
            to_tuple(self.green_face.matrix),
            to_tuple(self.yellow_face.matrix),
            to_tuple(self.blue_face.matrix),
            to_tuple(self.white_face.matrix),
            to_tuple(self.orange_face.matrix)
        )) 


   

def create_matrix_same(symbol):               # creates a matrix whose elements are all equal to 'symbol'
    return [[symbol for _ in range(3)] for _ in range(3)]

def create_target():                          # creates the desired configuration
    return cube([
        face(create_matrix_same(R)),
         face(create_matrix_same(G)),
         face(create_matrix_same(Y)),
         face(create_matrix_same(B)),
         face(create_matrix_same(W)),
         face(create_matrix_same(O))]
    )

def create_matrix(i11,i12,i13,i21,i22,i23,i31,i32,i33):
    return [[i11,i12,i13],[i21,i22,i23],[i31,i32,i33]]

target = create_target()


def print_cube_state(c, title=""):                 #prints actual cube state
    print(f"--- {title} ---")
    print(f"Red (Front):    {c.red_face.matrix}")
    print(f"White (Up):     {c.white_face.matrix}")
    print(f"Orange (Back):  {c.orange_face.matrix}")
    print(f"Yellow (Down):  {c.yellow_face.matrix}")
    print(f"Blue (Right):   {c.blue_face.matrix}")
    print(f"Green (Left):   {c.green_face.matrix}")
    print("-" * 30)

def main():
    # 1. Setup: creating 6 faces
    faces_data = [
        face(create_matrix(G,R,O,Y,R,Y,B,W,Y)), # 0: Red
        face(create_matrix(R,R,W,O,G,R,Y,Y,Y)), # 1: Green
        face(create_matrix(O,G,G,O,Y,G,G,B,R)), # 2: Yellow
        face(create_matrix(W,W,G,G,B,W,O,O,B)), # 3: Blue
        face(create_matrix(B,O,O,B,W,B,R,G,B)), # 4: White
        face(create_matrix(W,W,W,R,O,B,Y,Y,R))  # 5: Orange
    ]

    # 2. Cube Initialization
    my_cube = cube(faces_data)

    # Printing initial state
    print_cube_state(my_cube, "INITIAL STATE")

    # 3. Action
    #my_cube.rotate_red_row(backward, up)       
    #my_cube.rotate_red_column(backward, right)
    #my_cube.rotate_face(red, backward)
    my_cube.rotate_red_column(False, False)
    
    # 4. Checking final state
    print_cube_state(my_cube, "STATE AFTER ROTATION")

if __name__ == "___main___":
    main()

