import numpy as np
from enum import IntEnum
#bitmask-based representation of the board state of homeworlds
#72 bits for total board state, 10 masks for total board state = 720 bits, or 10 pairs of 64 bit integers, a 2x10 uint64 tensor/matrix
#with only the first 8 bits of the second uint64 being used (annoying, but necessary)

#size1 = int(1), size2 = int(2), size3 = int(3)
class Color(IntEnum):
    Red = 0
    Green = 1
    Yellow = 2
    Blue = 3

class homeworlds_board:
    def __init__(self):
        self.board       = np.ndarray((2,1), buffer=np.array([0xFFFFFFFFF0000000,0x0], dtype=np.uint64), dtype=np.uint64)
        self.bank_mask   = np.ndarray((2,1), buffer=np.array([0xFFFFFFFFF0000000,0x0], dtype=np.uint64), dtype=np.uint64)
        self.size_mask   = np.ndarray((3,2), buffer=np.array([[0x0381C0E070000000,0x0],  #size 1
                                                              [0x1C0E070380000000,0x0],  #size 2
                                                              [0xE070381C00000000,0x0]], #size 3
                                                              dtype=np.uint64), dtype=np.uint64)
        #self.size2_mask  = np.ndarray((2,1), buffer=np.array([0x1C0E070380000000,0x0], dtype=np.uint64), dtype=np.uint64)
        #self.size3_mask  = np.ndarray((2,1), buffer=np.array([0xE070381C00000000,0x0], dtype=np.uint64), dtype=np.uint64)
        self.color_mask  = np.ndarray((4,2), buffer=np.array([[0xFF80000000000000,0x0],  #red
                                                              [0x007FC00000000000,0x0],  #green
                                                              [0x00003FE000000000,0x0],  #yellow
                                                              [0x0000001FF0000000,0x0]], #blue 
                                                             dtype=np.uint64), dtype=np.uint64)
        #self.red_mask    = np.ndarray((2,1), buffer=np.array([0xFF80000000000000,0x0], dtype=np.uint64), dtype=np.uint64)
        #self.green_mask  = np.ndarray((2,1), buffer=np.array([0x007FC00000000000,0x0], dtype=np.uint64), dtype=np.uint64)
        #self.yellow_mask = np.ndarray((2,1), buffer=np.array([0x00003FE000000000,0x0], dtype=np.uint64), dtype=np.uint64)
        #self.blue_mask   = np.ndarray((2,1), buffer=np.array([0x0000001FF0000000,0x0], dtype=np.uint64), dtype=np.uint64)
        self.player_mask = np.ndarray((2,1), buffer=np.array([0x0000000000000000,0x0], dtype=np.uint64), dtype=np.uint64)
        self.star_mask   = np.ndarray((2,1), buffer=np.array([0x0000000000000000,0x0], dtype=np.uint64), dtype=np.uint64)
        self.players = 2
        self.player_turn = 1
        self.first_turn = True

    #returns true if a piece of size and color is present in the bank
    def check_bank_for_piece(size,color):
        return bool(board[0]&bank_mask[0]&size_mask[size][0]&color_mask[color][0])

    def move_from_bank_to_board(size, color, position):
        #zero out the piece in the bank

        #place that piece in position
        return True #this should never fail, I check before I do it (famous last words)

    def move_from_board_to_bank(size, color, position):
        return True #this should never fail, I check before I do it (famous last words)

    def move_from_board_to_board(size, color, old_pos, new_pos):
        return True

    def choose_homeworld(star1, star2, ship):
        color1, size1 = star1
        color2, size2 = star2
        color3, size3 = ship

        if(check_bank_for_piece(size1,color1) and check_bank_for_piece(size2, color2) and check_bank_for_piece(size3,color3) and first_turn):
            #need to:
            #  zero out the first(farthest right) instance of the piece we're looking for in the board, the color_mask, and the size_mask
            if(player_turn == 1):
              #  if player one is choosing their homeworld, we want to place the homeworld stars and ship at the 36th, 37th, and 38th bit, respectively
            #  if player two is choosing their homeworld, we want to place the homeworld stars and ship at the 39th, 40th, and 41st bit, respectively
            return True
        else:
            return False


        
homeworlds = homeworlds_board()
print("{:b}".format(int(homeworlds.board[0])))
