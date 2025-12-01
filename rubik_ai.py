# rubik_ai v. 0.1
# authors Edoardo Pilia & Alessia Congia

import copy
import heapq


G = 'G'   # G as 'green'
Y = 'Y'   # Y as 'yellow'
W = 'W'   # W as 'white'
B = 'B'   # B as 'blue'
R = 'R'   # R as 'red'
O = 'O'   # O as 'orange'


# This class describes each face as a 3x3 matrix of symbols
class face:
    center_index = 1
    
    def __init__(self, matrix):
        self.matrix = matrix
        self.color = matrix[1][1]
        pass
        
    #
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
    
    def center(self):
        return self.matrix[1][1]
    

    def __eq__(self, other):
        result = (self.matrix[0] == other.matrix[0] and self.matrix[1] == other.matrix[1] and self.matrix[2] == other.matrix[2])
        return result
    
    def __ne__(self, other):
        return not self.__eq__(other)

class cube:

    def __init__(self, faces):
        self.red_face = faces[0] #red
        self.green_face = faces[1] #green
        self.yellow_face = faces[2] #yellow
        self.blue_face = faces[3] #blue
        self.white_face = faces[4] #white
        self.orange_face = faces[5] #orange
  
    def rotate_red_column(self, backward, right, double=False):
        return_cube = copy.deepcopy(self)

        index =  2 if right else 0
        op_idx = 0 if right else 2
        if right: return_cube.blue_face.rotate(not(backward))
        else: return_cube.green_face.rotate(backward)

        col_red = self.red_face.get_column(index)
        col_white = self.white_face.get_column(index)
        col_yellow = self.yellow_face.get_column(index)
        col_orange = self.orange_face.get_column(op_idx)
        if backward:
            return_cube.red_face.switch_column(index, col_yellow)
            return_cube.yellow_face.switch_column(index, col_orange[::-1])
            return_cube.orange_face.switch_column(op_idx, col_white[::-1])
            return_cube.white_face.switch_column(index, col_red)
        else:
            return_cube.red_face.switch_column(index, col_white)
            return_cube.white_face.switch_column(index, col_orange[::-1])
            return_cube.orange_face.switch_column(op_idx, col_yellow[::-1])
            return_cube.yellow_face.switch_column(index, col_red)

        if double: 
            return_cube = return_cube.rotate_red_column(backward, right, False)

        return return_cube  

    def rotate_red_row(self, backward, up, double=False):
        return_cube = copy.deepcopy(self)

        index = 0 if up else 2
        
        if up: return_cube.white_face.rotate(not backward)
        else: return_cube.yellow_face.rotate(backward)

        row_red = self.red_face.get_row(index)
        row_blue = self.blue_face.get_row(index)
        row_orange = self.orange_face.get_row(index)
        row_green = self.green_face.get_row(index)

        if backward:
            return_cube.red_face.switch_row(index, row_blue)
            return_cube.blue_face.switch_row(index, row_orange)
            return_cube.orange_face.switch_row(index, row_green)
            return_cube.green_face.switch_row(index, row_red)
        else:
            return_cube.red_face.switch_row(index, row_green)
            return_cube.green_face.switch_row(index, row_orange)
            return_cube.orange_face.switch_row(index, row_blue)
            return_cube.blue_face.switch_row(index, row_red)

        if double:
            return_cube = return_cube.rotate_red_row(backward, up, False)

        return return_cube

    def rotate_face(self, backward, red, double=False):       
        return_cube = copy.deepcopy(self)

        index = 2 if red else 0
        op_idx = 0 if red else 2

        if red: return_cube.red_face.rotate(backward)
        else: return_cube.orange_face.rotate(not backward)   

        row_white = self.white_face.get_row(index)
        col_blue = self.blue_face.get_column(op_idx)
        row_yellow = self.yellow_face.get_row(op_idx)
        col_green = self.green_face.get_column(index)

        if backward:
            return_cube.white_face.switch_row(index, col_blue)
            return_cube.blue_face.switch_column(op_idx, row_yellow[::-1])
            return_cube.yellow_face.switch_row(op_idx, col_green)
            return_cube.green_face.switch_column(index, row_white[::-1])
        else:
            return_cube.white_face.switch_row(index, col_green[::-1])
            return_cube.green_face.switch_column(index, row_yellow)
            return_cube.yellow_face.switch_row(op_idx, col_blue[::-1])
            return_cube.blue_face.switch_column(op_idx, row_white)

        if double:
            return_cube = return_cube.rotate_face(red, backward, False)

        return return_cube
    
    def faces(self):
        return [ self.red_face,
        self.green_face ,
        self.yellow_face,
        self.blue_face,
        self.white_face,
        self.orange_face]

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


   

def create_matrix_same(symbol):
    """Crea una matrice 3x3 riempita con un simbolo specifico."""
    return [[symbol for _ in range(3)] for _ in range(3)]

def create_target():
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


def print_cube_state(c, title=""):
    """Stampa lo stato attuale delle facce interessate."""
    print(f"--- {title} ---")
    print(f"Red (Front):    {c.red_face.matrix}")
    print(f"White (Up):     {c.white_face.matrix}")
    print(f"Orange (Back):  {c.orange_face.matrix}")
    print(f"Yellow (Down):  {c.yellow_face.matrix}")
    print(f"Blue (Right):   {c.blue_face.matrix}")
    print(f"Green (Left):   {c.green_face.matrix}")
    print("-" * 30)


class cube_node:

    


    def __init__(self, current, parent):
        self.current = current                   # Cubo corrente
        self.parent = parent                     # Nodo genitore (per risalire al percorso che conduce alla soluzione)
        self.depth = 0 if parent is None else parent.depth + 1
        self.function = self.cube_heuristic() + self.depth if self.cube_heuristic() > 0  else 0




    def border(self, color, direction):
        if color == R:
            if direction == 'up':
                return self.current.white_face
            if direction == 'down':
                return self.current.blue_face
            if direction == 'left':
                return self.current.green_face
            if direction == 'right':
                return self.current.yellow_face
        if color == W:
            if direction == 'up':
                return self.current.orange_face
            if direction == 'down':
                return self.current.red_face
            if direction == 'left':
                return self.current.green_face
            if direction == 'right':
                return self.current.blue_face
        if color == O:
            if direction == 'up':
                return self.current.white_face
            if direction == 'down':
                return self.current.yellow_face
            if direction == 'left':
                return self.current.blue_face
            if direction == 'right':
                return self.current.green_face
        if color == Y:
            if direction == 'up':
                return self.current.red_face
            if direction == 'down':
                return self.current.orange_face
            if direction == 'left':
                return self.current.green_face
            if direction == 'right':
                return self.current.blue_face
        if color == G:
            if direction == 'up':
                return self.current.white_face
            if direction == 'down':
                return self.current.yellow_face
            if direction == 'left':
                return self.current.orange_face
            if direction == 'right':
                return self.current.red_face
        if color == B:
            if direction == 'up':
                return self.current.white_face
            if direction == 'down':
                return self.current.yellow_face
            if direction == 'left':
                return self.current.red_face
            if direction == 'right':
                return self.current.orange_face
        return None


    def correct(self, color, row_index, column_index):
        flag = 0

        # Determina direzioni
        col_direction = 'left' if column_index == 0 else 'right' if column_index == 2 else None
        row_direction = 'up' if row_index == 0 else 'down' if row_index == 2 else None

        border_row = self.border(color, row_direction)
        border_column = self.border(color, col_direction)

        # ---------------------------------------------------------
        # 1. CONTROLLO VERTICALE (Sopra/Sotto)
        # ---------------------------------------------------------
        if border_row is None: 
            flag += 1
        else:
            # Caso speciale: FACCE LATERALI (Blu/Verde) che guardano SU/GIÙ (Bianco/Giallo)
            # Qui si passa da una RIGA (del Blu) a una COLONNA (del Bianco)
            if color in [B, G]: 
                # Se sono Blu, tocco la colonna Destra (2) del Bianco
                # Se sono Verde, tocco la colonna Sinistra (0) del Bianco
                b_c_idx = 2 if color == B else 0
                
                # Mappatura coordinate: La mia colonna diventa la sua riga (spesso invertita)
                # Esempio: Blu(0,0) tocca Bianco(2,2). Blu(0,2) tocca Bianco(0,2).
                b_r_idx = 2 - column_index 

            else:
                # Caso Standard (Rosso/Arancio vs Bianco/Giallo): Riga tocca Riga
                b_r_idx = 2 if row_index == 0 else 0
                b_c_idx = column_index

            # Verifica
            if border_row.matrix[b_r_idx][b_c_idx] == border_row.color: 
                flag += 1

        # ---------------------------------------------------------
        # 2. CONTROLLO ORIZZONTALE (Destra/Sinistra)
        # ---------------------------------------------------------
        if border_column is None: 
            flag += 1
        else:
            # Caso speciale: FACCE SUP/INF (Bianco/Giallo) che guardano LATI (Blu/Verde)
            # Qui si passa da una COLONNA (del Bianco) a una RIGA (del Blu)
            if color in [W, Y]:
                # Se esco da Bianco/Giallo verso Blu/Verde, entro nella loro Riga Alta (0) o Bassa (2)
                # Bianco guarda a Destra (Blu) -> Entra nella Riga 0 del Blu
                # Giallo guarda a Destra (Blu) -> Entra nella Riga 2 del Blu
                b_r_idx = 0 if color == W else 2
                
                # La mia riga diventa la sua colonna (invertita)
                b_c_idx = 2 - row_index
            
            else:
                # Caso Standard (Facce laterali tra loro): Colonna tocca Colonna
                b_c_idx = 2 if column_index == 0 else 0
                b_r_idx = row_index

            # Verifica
            if border_column.matrix[b_r_idx][b_c_idx] == border_column.color:
                flag += 1

        return 1 if flag == 2 else 0
    
    
    def cube_heuristic(self):
        score = 54
        for face in self.current.faces():
            face_score = 0
            row_index = 0
            for row in face.matrix:
                column_index = 0
                for value in row:
                    color = face.get_row(1)[1]
                    if value == face.get_row(1)[1]:
                        face_score += self.correct(color, row_index, column_index)
                    column_index += 1
                row_index += 1
            score -= face_score
        return score

    def __lt__(self, other):
        return self.cube_heuristic()+self.depth < other.cube_heuristic()+other.depth


    


def main():
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

if __name__ == "___main___":
    main()

