import numpy as np

#bitmask-based representation of the board state of homeworlds
#72 bits for total board state, 10 masks for total board state = 720 bits, or 10 pairs of 64 bit integers, a 2x10 uint64 tensor/matrix
#with only the first 8 bits of the second uint64 being used (annoying, but necessary)

class homeworlds_board:
    def __init__(self):
        self.board       = np.ndarray((2,1), buffer=np.array([0xFFFFFFFFF0000000,0x0], dtype=np.uint64), dtype=np.uint64)
        self.bank_mask   = np.ndarray((2,1), buffer=np.array([0xFFFFFFFFF0000000,0x0], dtype=np.uint64), dtype=np.uint64)
        self.size1_mask  = np.ndarray((2,1), buffer=np.array([0x0381C0E070000000,0x0], dtype=np.uint64), dtype=np.uint64)
        self.size2_mask  = np.ndarray((2,1), buffer=np.array([0x1C0E070380000000,0x0], dtype=np.uint64), dtype=np.uint64)
        self.size3_mask  = np.ndarray((2,1), buffer=np.array([0xE070381C00000000,0x0], dtype=np.uint64), dtype=np.uint64)
        self.red_mask    = np.ndarray((2,1), buffer=np.array([0xFF80000000000000,0x0], dtype=np.uint64), dtype=np.uint64)
        self.green_mask  = np.ndarray((2,1), buffer=np.array([0x007FC00000000000,0x0], dtype=np.uint64), dtype=np.uint64)
        self.yellow_mask = np.ndarray((2,1), buffer=np.array([0x00003FE000000000,0x0], dtype=np.uint64), dtype=np.uint64)
        self.blue_mask   = np.ndarray((2,1), buffer=np.array([0x0000001FF0000000,0x0], dtype=np.uint64), dtype=np.uint64)
        self.player_mask = np.ndarray((2,1), buffer=np.array([0x0000000000000000,0x0], dtype=np.uint64), dtype=np.uint64)
        self.star_mask   = np.ndarray((2,1), buffer=np.array([0x0000000000000000,0x0], dtype=np.uint64), dtype=np.uint64)

homeworlds = homeworlds_board()
print("{:b}".format(int(homeworlds.board[0])))
