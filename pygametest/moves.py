from cubestate import CubeState as State

class _const:
    class ConstError(TypeError):
        pass

    def __init__(self):
        self.moves = {
            'U': State([3, 0, 1, 2, 4, 5, 6, 7],
                       [0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 1, 2, 3, 7, 4, 5, 6, 8, 9, 10, 11],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
            'D': State([0, 1, 2, 3, 5, 6, 7, 4],
                       [0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 1, 2, 3, 4, 5, 6, 7, 9, 10, 11, 8],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
            'L': State([4, 1, 2, 0, 7, 5, 6, 3],
                       [2, 0, 0, 1, 1, 0, 0, 2],
                       [11, 1, 2, 7, 4, 5, 6, 0, 8, 9, 10, 3],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
            'R': State([0, 2, 6, 3, 4, 1, 5, 7],
                       [0, 1, 2, 0, 0, 2, 1, 0],
                       [0, 5, 9, 3, 4, 2, 6, 7, 8, 1, 10, 11],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
            'F': State([0, 1, 3, 7, 4, 5, 2, 6],
                       [0, 0, 1, 2, 0, 0, 2, 1],
                       [0, 1, 6, 10, 4, 5, 3, 7, 8, 9, 2, 11],
                       [0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 0]),
            'B': State([1, 5, 2, 3, 0, 4, 6, 7],
                       [1, 2, 0, 0, 2, 1, 0, 0],
                       [4, 8, 2, 3, 1, 5, 6, 7, 0, 9, 10, 11],
                       [1, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0]
                       )}

        move_names = []
        faces = list(self.moves.keys())
        for face_name in faces:
            move_names += [face_name, face_name + '2', face_name + '\'']
            self.moves[face_name + '2'] = self.moves[face_name].apply_move(self.moves[face_name])
            self.moves[face_name + '\''] = self.moves[face_name].apply_move(self.moves[face_name]).apply_move(self.moves[face_name])

    def __setattr__(self, name, value):
        if name in self.__dict__:
            raise self.ConstError("Can't rebind const (%s)" % name)
        self.__dict__[name] = value

import sys
sys.modules[__name__]=_const()