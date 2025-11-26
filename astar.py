import rubik_ai as rb
from rubik_ai import G,R,O,Y,B,W
from concurrent.futures import ThreadPoolExecutor, as_completed
import itertools
from collections import deque
from pympler import asizeof

def face_heuristic(face):
    center = face.get_row(1)[1]
    score = 9
    for row in face.matrix:
        for value in row:
            if value == center:
                score -= 1
    return score

def cube_heuristic(cube):
    score = 0
    for face in cube.faces():
        score += face_heuristic(face)
    return score