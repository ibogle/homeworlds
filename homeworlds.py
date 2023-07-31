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
        self.star_positions = []

    #returns true if a piece of size and color is present in the bank
    def check_bank_for_piece(size,color):
        return bool(board[0]&bank_mask[0]&size_mask[size][0]&color_mask[color][0])

    def move_from_bank_to_board(size, color, position, is_star=False, ship_at_star=-1):
        #zero out the piece in the bank

        #place that piece in position
        #if is_star is true, update the star positions list, and the relevant star_mask entry
        return True #this should never fail, I check before I do it (famous last words)

    def move_from_board_to_bank(size, color, position, is_star=False, ship_at_star=-1):
        #zero out the piece in position
        #if is_star is true, zero out the star mask and remove the entry from star positions

        #place the piece back in the bank, update relevant masks
        return True #this should never fail, I check before I do it (famous last words)

    def place_homeworld_star(size1, color1, size2, color2, position):
        # This is needed to avoid creating two star_masks
        #create the star mask for the homeworld here, add to the overall star_mask, and the star positions list
        move_from_bank_to_board(size1, color1, position)
        move_from_bank_to_board(size2, color2, position+1)
        return True


    def move_from_board_to_board(size, color, old_pos, new_pos):
        #execute the scooch
        return True

    def choose_homeworld(star1, star2, ship):
        color1, size1 = star1
        color2, size2 = star2
        color3, size3 = ship

        if(check_bank_for_piece(size1,color1) and check_bank_for_piece(size2, color2) and check_bank_for_piece(size3,color3) and first_turn):
            #need to:
            #  zero out the first(farthest right) instance of the piece we're looking for in the board, the color_mask, and the size_mask
            if(player_turn == 1):
                player_turn = 2
                #move_from_bank_to_board(size1,color1,36,True)
                #move_from_bank_to_board(size2,color2,37,True) #this needs fixed, can't have the homeworld star mask taking up two star masks!
                place_homeworld_star(size1, color1, size2, color2, 36)
                move_from_bank_to_board(size3, color3, 38, False, 0)
                # if player one is choosing their homeworld, we want to place the homeworld stars and ship at the 36th, 37th, and 38th bit, respectively
            elif(player_turn == 2):
                player_turn = 1
                first_turn = False
                #move_from_bank_to_board(size1,color1,39,True)
                #move_from_bank_to_board(size2,color2,40,True) #this needs fixed, can't have the homeworld star mask taking up two star masks!
                place_homeworld_star(size1, color1, size2, color2, 39)
                move_from_bank_to_board(size3,color3,41,False,1)
                # if player two is choosing their homeworld, we want to place the homeworld stars and ship at the 39th, 40th, and 41st bit, respectively
            return True
        else:
            # the pieces aren't in the bank, somehow?
            return False


        
homeworlds = homeworlds_board()
