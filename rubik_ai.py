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
    """
    This class describes a face as a 3x3 matrix of symbols

    :matrix: identifies the current status of the face
    :color: identifies the color of the face (always equal to the center)
    """
    center_index = 1
    
    def __init__(self, matrix):
        self.matrix = matrix
        self.color = matrix[self.center_index][self.center_index] # Used to define the color of the face (always equal to the center)

    def __eq__(self, other):
        result = (self.matrix[0] == other.matrix[0] and self.matrix[1] == other.matrix[1] and self.matrix[2] == other.matrix[2])
        return result
    def __ne__(self, other):
        return not self.__eq__(other)
        
    def get_row(self, index):
        '''
        Returns the selected row.
        
        :param index: specifies the addressed row
        '''
        return self.matrix[index]

    def get_column(self, index):
        '''
        Returns the selected column.
        
        :param index: specifies the addressed column
        '''
        return [self.matrix[0][index], self.matrix[1][index], self.matrix[2][index]]

    def switch_row(self, index:int, row:list): 
        """
        Exchange the given row with another. Return -1 if the central row is selected.

        :param index: specifies the addressed row
        :param row: the new row to be exchanged
        """
        if index == self.center_index: return -1 #cannot switch the central row
        self.matrix[index] = row
    
    def switch_column(self, index:int, column:list):
        '''
        Exchange the given column with another. Return -1 if the central column is selected.

        :param index: specifies the addressed column
        :param column: the new column to be exchanged
        '''
        if index == self.center_index: return -1 #cannot switch the central column
        self.matrix[0][index] = column[0]
        self.matrix[1][index] = column[1]
        self.matrix[2][index] = column[2]
        
    
    def rotate(self, backward:bool):
        '''
        Rotate the face backward or frontward.
        
        :param backward: specifies the direction of the rotation.
        '''
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

    @staticmethod    
    def complete_face(symbol):
        '''
        Returns a resolved face with the given symbol. This is a static method.

        :param symbol: the color to be used
        '''
        return face([[symbol for _ in range(3)] for _ in range(3)])

            

class cube:
    """
    This class describes a cube.

    :red_face: identifies the red face
    :green_face: identifies the green face
    :yellow_face: identifies the yellow face
    :blue_face: identifies the blue face
    :white_face: identifies the white face
    :orange_face: identifies the orange face
    """

    def __init__(self, faces:list):
        '''
        :param faces: list of faces following this order: red, green, yellow, blue, white, orange
        '''
        self.red_face = faces[0]
        self.green_face = faces[1]
        self.yellow_face = faces[2]
        self.blue_face = faces[3]
        self.white_face = faces[4]
        self.orange_face = faces[5]

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
        # Needed for using sets. 
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

    def rotate_red_column(self, backward:bool, right:bool, double:bool=False):
        '''
        Rotates a column of the red face

        :param backward: specifies if the rotation is backward or not
        :param right: specifies which column to rotate
        :param double: specifies if the rotation should be done twice
        '''

        return_cube = fast_copy(self)

        index =  2 if right else 0
        op_idx = 0 if right else 2       # opposite index for orange face
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

    def rotate_red_row(self, backward:bool, up:bool, double:bool=False):
        '''
        Rotates a row of the red face

        :param backward: specifies if the rotation is backward or not
        :param up: specifies which row to rotate
        :param double: specifies if the rotation should be done twice
        '''

        return_cube = fast_copy(self)

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

    def rotate_face(self, backward:bool, red:bool, double=False):
        '''
        Rotates the red or the orange face

        :param backward: specifies if the rotation is backward or not
        :param red: specifies which face is to be rotated (red/true or orange/false)
        :param double: specifies if the rotation should be done twice
        '''       
        return_cube = fast_copy(self)

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
        '''
        Returns the cube's current configuration 
        '''
        return [ self.red_face,
        self.green_face ,
        self.yellow_face,
        self.blue_face,
        self.white_face,
        self.orange_face]
    
    def print(self, title=""):
        """
        Prints the cube's current configuration.

        :param title: specifies a title.
        """
        print(f"--- {title} ---")
        print(f"Red (Front):    {self.red_face.matrix}")
        print(f"White (Up):     {self.white_face.matrix}")
        print(f"Orange (Back):  {self.orange_face.matrix}")
        print(f"Yellow (Down):  {self.yellow_face.matrix}")
        print(f"Blue (Right):   {self.blue_face.matrix}")
        print(f"Green (Left):   {self.green_face.matrix}")
        print("-" * 30)

    def border(self, color:str, direction:str):
        '''
        Returns the face that borders with the specified in a direction.

        :param color: specifies the face to analyze
        :param direction: specifies the direction of the border
        '''
        if color == R:
            if direction == 'up':
                return self.white_face
            if direction == 'down':
                return self.blue_face
            if direction == 'left':
                return self.green_face
            if direction == 'right':
                return self.yellow_face
        if color == W:
            if direction == 'up':
                return self.orange_face
            if direction == 'down':
                return self.red_face
            if direction == 'left':
                return self.green_face
            if direction == 'right':
                return self.blue_face
        if color == O:
            if direction == 'up':
                return self.white_face
            if direction == 'down':
                return self.yellow_face
            if direction == 'left':
                return self.blue_face
            if direction == 'right':
                return self.green_face
        if color == Y:
            if direction == 'up':
                return self.red_face
            if direction == 'down':
                return self.orange_face
            if direction == 'left':
                return self.green_face
            if direction == 'right':
                return self.blue_face
        if color == G:
            if direction == 'up':
                return self.white_face
            if direction == 'down':
                return self.yellow_face
            if direction == 'left':
                return self.orange_face
            if direction == 'right':
                return self.red_face
        if color == B:
            if direction == 'up':
                return self.white_face
            if direction == 'down':
                return self.yellow_face
            if direction == 'left':
                return self.red_face
            if direction == 'right':
                return self.orange_face
        return None


    @staticmethod
    def create_target():
        '''
        Returns a resolved cube. This is a static method.
        '''
        return cube([
            face.complete_face(R),
            face.complete_face(G),
            face.complete_face(Y),
            face.complete_face(B),
            face.complete_face(W),
            face.complete_face(O)]
        )
    
def fast_copy(self):
    # Crea una copia manuale molto più veloce di deepcopy
    new_faces = []
    for f in self.faces():
        # Copia la matrice 3x3 manualmente (list comprehension è veloce)
        new_matrix = [row[:] for row in f.matrix]
        new_faces.append(face(new_matrix))
    return cube(new_faces)

target = cube.create_target()

class cube_node:
    """
    This class describes a node for searching algorithms

    :current: describes the cube's current configuration (cube type object).
    :parent: reference to parent node (cube_node type object). None if root. 
    :depth: specifies the depth of the current node if relevant for the algorithm.
    :function: returns the heuristic of the node.
    """
    
    def __init__(self, current, parent):
        self.current = current                   
        self.parent = parent                    
        self.depth = 0 if parent is None else parent.depth + 1
        self.function = self.cube_heuristic() + self.depth if self.cube_heuristic() > 0  else 0

    def get_face_distance(self, current_face_color, sticker_color):
        """
        Returns the minimum distance between a sticker and its face.
        0: Correct face
        2: Opposite face
        1: Lateral face
        """
        if current_face_color == sticker_color:
            return 0
        
        opposites = {
            W: Y, 
            Y: W,
            G: B, 
            B: G,
            R: O, 
            O: R
        }
        
        if opposites.get(current_face_color) == sticker_color:
            return 2

        return 1

    def cube_heuristic(self):
        """
        Returns the Manhattan Distance / 8.
        """
        total_distance = 0
        
        for face in self.current.faces():
            current_face_color = face.color
            
            for row in face.matrix:
                for sticker_color in row:
                    
                    dist = self.get_face_distance(current_face_color, sticker_color)
                    total_distance += dist
        
        return total_distance / 4

    def __lt__(self, other):
        return self.cube_heuristic()+self.depth < other.cube_heuristic()+other.depth
    


# Function set for node expansion
def execute_function_set(node):
    new_nodes = set()
    current_cube = node.current

    
    moves = []
    

    moves.append((current_cube.rotate_red_column, False, True, False))  # R
    moves.append((current_cube.rotate_red_column, True,  True, False))  # R'
    moves.append((current_cube.rotate_red_column, False, True, True))   # R2
    
    moves.append((current_cube.rotate_red_column, False, False, False)) # L
    moves.append((current_cube.rotate_red_column, True,  False, False)) # L'
    moves.append((current_cube.rotate_red_column, False, False, True))  # L2

    moves.append((current_cube.rotate_red_row, False, True, False))   # U
    moves.append((current_cube.rotate_red_row, True,  True, False))   # U'
    moves.append((current_cube.rotate_red_row, False, True, True))    # U2
    
    moves.append((current_cube.rotate_red_row, False, False, False))  # D
    moves.append((current_cube.rotate_red_row, True,  False, False))  # D'
    moves.append((current_cube.rotate_red_row, False, False, True))   # D2

    moves.append((current_cube.rotate_face, False, True, False))    # F
    moves.append((current_cube.rotate_face, True,  True, False))    # F'
    moves.append((current_cube.rotate_face, False, True, True))     # F2
    
    moves.append((current_cube.rotate_face, False, False, False))   # B
    moves.append((current_cube.rotate_face, True,  False, False))   # B'
    moves.append((current_cube.rotate_face, False, False, True))    # B2

    for action, p1, p2, p3 in moves:

        new_cube_state = action(p1, p2, p3)
        
        if node.parent and new_cube_state == node.parent.current:
            continue

        new_node = cube_node(new_cube_state, node)
        new_nodes.add(new_node)

    return new_nodes