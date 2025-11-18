# rubik_ai v. 0.1
# authors Edoardo Pilia & Alessia Congia

import copy

G = 'G'
Y = 'Y'
W = 'W'
B = 'B'
R = 'R'
O = 'O'

class face:
    center_index = 1

    def __init__(self, matrix):
        self.matrix = matrix
        pass
    
    def switch_row(self, index, row):
        if index == self.center_index: return -1 #cannot switch the central row
        self.matrix[index] = row
    
    def switch_column(self, index, column):
        if index == self.center_index: return -1 #cannot switch the central column
        self.matrix[0][index] = column[0]
        self.matrix[1][index] = column[1]
        self.matrix[2][index] = column[2]
        
    
    def rotate(self, backward):
        row0 = copy.copy(self.matrix[0])
        row2 = copy.copy(self.matrix[2])
        column0 = copy.copy(self.get_column(0))
        column2 = copy.copy(self.get_column(2))
        if backward:
            self.switch_column(0, row0[::-1])
            self.switch_row(0, column2)
            self.switch_column(2, row2[::-1])
            self.switch_row(2, column0) 
        else:
            self.switch_row(0, column0[::-1])
            self.switch_column(2, row0)
            self.switch_row(2, column2[::-1])
            self.switch_column(0, row2)
            

    
    def get_column(self, index):
        return [self.matrix[0][index], self.matrix[1][index], self.matrix[2][index]]
    def get_row(self, index):
        return self.matrix[index]



class cube:
    face_number = 6

    def __init__(self, faces):
        self.red_face = faces[0] #red
        self.green_face = faces[1] #green
        self.yellow_face = faces[2] #yellow
        self.blue_face = faces[3] #blue
        self.white_face = faces[4] #white
        self.orange_face = faces[5] #orange

        
    def rotate_red_column(self, backward, right):
        reference_cube = copy.deepcopy(self)
        index =  2 if right else 0
        op_idx = 0 if right else 2
        if right: self.blue_face.rotate(backward)
        else: self.green_face.rotate(backward)

        if backward:
            self.red_face.switch_column(index, reference_cube.yellow_face.get_column(index))
            self.yellow_face.switch_column(index, reference_cube.orange_face.get_column(op_idx)[::-1])
            self.orange_face.switch_column(op_idx, reference_cube.white_face.get_column(index)[::-1])
            self.white_face.switch_column(index, reference_cube.red_face.get_column(index))
        else:
            self.red_face.switch_column(index, reference_cube.white_face.get_column(index))
            self.white_face.switch_column(index, reference_cube.orange_face.get_column(op_idx)[::-1])
            self.orange_face.switch_column(op_idx, reference_cube.yellow_face.get_column(index)[::-1])
            self.yellow_face.switch_column(index, reference_cube.red_face.get_column(index))


    def rotate_red_row(self, backward, up):
        reference_cube = copy.deepcopy(self)
        index = 0 if up else 2
        if up: self.white_face.rotate(backward)
        else: self.yellow_face.rotate(backward)

        if backward:
            self.red_face.switch_row(index, reference_cube.green_face.get_row(index))
            self.green_face.switch_row(index, reference_cube.orange_face.get_row(index))
            self.orange_face.switch_row(index, reference_cube.blue_face.get_row(index))
            self.blue_face.switch_row(index, reference_cube.red_face.get_row(index))
        else:
            self.red_face.switch_row(index, reference_cube.blue_face.get_row(index))
            self.blue_face.switch_row(index, reference_cube.orange_face.get_row(index))
            self.orange_face.switch_row(index, reference_cube.green_face.get_row(index))
            self.green_face.switch_row(index, reference_cube.red_face.get_row(index))
    

    def rotate_face(self, red, backward):
        reference_cube = copy.deepcopy(self)
        index = 2 if red else 0
        op_idx = 0 if red else 2
        if red: self.red_face.rotate(backward)
        else: self.orange_face.rotate(not(backward))

        if backward:
            self.white_face.switch_row(index, reference_cube.blue_face.get_column(op_idx))
            self.blue_face.switch_column(op_idx, reference_cube.yellow_face.get_row(op_idx)[::-1])
            self.yellow_face.switch_row(op_idx, reference_cube.green_face.get_column(index))
            self.green_face.switch_column(index, reference_cube.white_face.get_row(index)[::-1])
        else:
            self.white_face.switch_row(index, reference_cube.green_face.get_column(index)[::-1])
            self.green_face.switch_column(index, reference_cube.yellow_face.get_row(op_idx))
            self.yellow_face.switch_row(op_idx, reference_cube.blue_face.get_column(op_idx)[::-1])
            self.blue_face.switch_column(op_idx, reference_cube.white_face.get_row(index))



             


def create_dummy_matrix(symbol):
    """Crea una matrice 3x3 riempita con un simbolo specifico."""
    return [[symbol for _ in range(3)] for _ in range(3)]

def create_matrix(i11,i12,i13,i21,i22,i23,i31,i32,i33):
    return [[i11,i12,i13],[i21,i22,i23],[i31,i32,i33]]


def print_cube_state(c, title):
    """Stampa lo stato attuale delle facce interessate."""
    print(f"--- {title} ---")
    print(f"Red (Front):    {c.red_face.matrix}")
    print(f"White (Up):     {c.white_face.matrix}")
    print(f"Orange (Back):  {c.orange_face.matrix}")
    print(f"Yellow (Down):  {c.yellow_face.matrix}")
    print(f"Blue (Right):   {c.blue_face.matrix}")
    print(f"Green (Left):   {c.green_face.matrix}")
    print("-" * 30)

# 1. Setup: Creiamo le 6 facce con colori distinti
# Ordine da tuo codice: red, green, yellow, blue, white, orange
faces_data = [
    face(create_matrix(G,R,O,Y,R,Y,B,W,Y)), # Red
    face(create_matrix(R,R,W,O,G,R,Y,Y,Y)), # 1: Green
    face(create_matrix(O,G,G,O,Y,G,G,B,R)), # 2: Yellow
    face(create_matrix(W,W,G,G,B,W,O,O,B)), # 3: Blue
    face(create_matrix(B,O,O,B,W,B,R,G,B)), # White
    face(create_matrix(W,W,W,R,O,B,Y,Y,R))  # 5: Orange
]

# 2. Inizializzazione Cubo
my_cube = cube(faces_data)

# Mostriamo lo stato iniziale
print_cube_state(my_cube, "STATO INIZIALE")

# 3. Azione: Ruotiamo la colonna DESTRA della faccia Rossa in avanti
# (Questo dovrebbe spostare i pezzi tra Red, White, Orange, Yellow)
#print(">>> Eseguo: rotate_red_column(backward=False, right=True)")
#my_cube.rotate_red_row(backward, up)
#my_cube.rotate_red_column(backward, right)
#my_cube.rotate_face(red, backward)

my_cube.rotate_red_column(False, False)
# 4. Verifica
print_cube_state(my_cube, "STATO DOPO ROTAZIONE")

#print(">>> Eseguo: rotate_red_column(backward=False, right=True)")
#my_cube.rotate_red_row(backward=False, up=True)
