import numpy as np
from moves import *

class CubeState():
    def __init__(self, cp, co, ep, eo):
        self.cp = np.array(cp, dtype='int8')
        self.co = np.array(co, dtype='int8')
        self.ep = np.array(ep, dtype='int8')
        self.eo = np.array(eo, dtype='int8')

    def apply_move(self, move):
        """
        操作を適用し、新しい状態を返す
        """
        new_cp = self.cp[move.cp]
        new_co = (self.co[move.cp] + move.co) % 3
        new_ep = self.ep[move.ep]
        new_eo = (self.eo[move.ep] + move.eo) % 2
        return CubeState(new_cp, new_co, new_ep, new_eo)






def main():
    print(moves)

if __name__ == "__main__":
    main()