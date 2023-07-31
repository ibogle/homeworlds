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
class Size(IntEnum):
    One = 0
    Two = 1
    Three = 2
#TODO: use one 64bit int for all board state:
#          -no explicit board state, pieces conceptually stay put positionally
#          -bank mask can change to indicate pieces in play
#          -size and color masks are constant
#          -keep star masks and star position list, and player masks

# Pieces do not move, they just change player ownership and star proximity, so only update the player, star, and at_star masks for board state
class homeworlds_board:
    def __init__(self):
        self.bank_mask    = np.ndarray((1,),   buffer=np.array( [0xFFFFFFFFF0000000], dtype=np.uint64), dtype=np.uint64)
        
        self.size_mask    = np.ndarray((3,1),  buffer=np.array([[0x0381C0E070000000],  #size 1
                                                                [0x1C0E070380000000],  #size 2
                                                                [0xE070381C00000000]], #size 3
                                                                dtype=np.uint64), dtype=np.uint64)
        self.color_mask   = np.ndarray((4,1),  buffer=np.array([[0xFF80000000000000],  #red
                                                                [0x007FC00000000000],  #green
                                                                [0x00003FE000000000],  #yellow
                                                                [0x0000001FF0000000]], #blue 
                                                               dtype=np.uint64), dtype=np.uint64)
        self.hw_mask      = np.ndarray((1,),   buffer=np.array( [0x0000000000000000], dtype=np.uint64), dtype=np.uint64)
        self.player_mask  = np.ndarray((2,1),  buffer=np.array([[0x0000000000000000],
                                                                [0x0000000000000000]], dtype=np.uint64), dtype=np.uint64)
        self.star_mask    = np.ndarray((1,),   buffer=np.array( [0x0000000000000000], dtype=np.uint64), dtype=np.uint64)
        self.at_star_mask = np.ndarray((18,1), buffer=np.array([[0x0000000000000000], #star 0
                                                                [0x0000000000000000], #star 1
                                                                [0x0000000000000000], #star 2
                                                                [0x0000000000000000], #star 3
                                                                [0x0000000000000000], #star 4
                                                                [0x0000000000000000], #star 5
                                                                [0x0000000000000000], #star 6
                                                                [0x0000000000000000], #star 7
                                                                [0x0000000000000000], #star 8
                                                                [0x0000000000000000], #star 9
                                                                [0x0000000000000000], #star 10
                                                                [0x0000000000000000], #star 11
                                                                [0x0000000000000000], #star 12
                                                                [0x0000000000000000], #star 13
                                                                [0x0000000000000000], #star 14
                                                                [0x0000000000000000], #star 15
                                                                [0x0000000000000000], #star 16
                                                                [0x0000000000000000]], dtype=np.uint64),#star 17
                                                                dtype=np.uint64)
        self.players = 2
        self.size_max = 3
        self.star_positions = []

    #returns binary position of the piece if a piece of size and color is present in the bank, -1 otherwise
    def check_bank_for_piece(self, size,color):
        if bool(self.bank_mask&self.size_mask[size]&self.color_mask[color]):
            print("found the piece")
            #return the position of the piece in the bank
            search = np.array([0x8000000000000000],dtype=np.uint64)
            while not bool(search & self.bank_mask & self.size_mask[size] & self.color_mask[color]):
                #print("searching...")
                search = search >> 1

            return search
        else:
            return None

    def count_ones_in_uint64(self,n):#0x0000000000000000              0x0000000000000000
        uCount = n - ((n >> 1) & 0x0333333333333333) - ((n>>2) & 0x0111111111111111)
        return ((uCount + (uCount>>3)) & 0x0307070707070707) % 63

    def choose_homeworld(self,player, star1, star2, ship):
        if bool(self.hw_mask[0] & self.player_mask[player]):
            print(f"Player {player} already has a homeworld")
            return False
        size1, color1 = star1
        size2, color2 = star2
        size3, color3 = ship

        #last minute validation, will probably check this beforehand
        print(format(self.bank_mask[0],"02x"))
        star1_pos = self.check_bank_for_piece(size1, color1)
        print(f"Checking for color {color1} and size {size1}")
        if star1_pos != None:
            print("star1_pos found")
            self.bank_mask[0] = self.bank_mask[0] & ~star1_pos[0]
        else:
            print("star1_pos not found")
        print(format(self.bank_mask[0],"02x"))
        star2_pos = self.check_bank_for_piece(size2, color2)
        print(f"Checking for color {color2} and size {size2}")
        if star2_pos != None:
            print("star2_pos found")
            self.bank_mask[0] = self.bank_mask[0] & ~star2_pos[0]
        else:
            print("star2_pos not found")
        print(format(self.bank_mask[0],"02x"))
        ship_pos  = self.check_bank_for_piece(size3, color3)
        print(f"Checking for color {color3} and size {size3}")
        if ship_pos != None:
            print("ship_pos found")
            self.bank_mask[0] = self.bank_mask[0] & ~ship_pos[0]
        else:
            print("ship_pos not found")
        if(star1_pos != None and star2_pos != None and ship_pos != None):
            #change hw_mask, player_mask[player], star_mask, star_positions, and at_star_mask[len(star_positions)+1]
            self.hw_mask[0]          = self.hw_mask[0]          | star1_pos[0] | star2_pos[0]
            self.player_mask[player] = self.player_mask[player] | star1_pos[0] | star2_pos[0] | ship_pos[0]
            self.star_mask[0]        = self.star_mask[0]        | star1_pos[0] | star2_pos[0]
            self.star_positions.append(star1_pos)
            self.at_star_mask[len(self.star_positions)-1] = ship_pos[0]
            return True
        else:
            # the pieces aren't in the bank, somehow?
            print(f"Player {player} requested an invalid start")
            #bank_mask[0] = bank_mask[0] | star1_pos | star2_pos | ship_pos
            if star1_pos != None:
                self.bank_mask[0] = self.bank_mask[0] | star1_pos
            if star2_pos != None:
                self.bank_mask[0] = self.bank_mask[0] | star2_pos
            if ship_pos != None:
                self.bank_mask[0] = self.bank_mask[0] | ship_pos
            return False

homeworlds = homeworlds_board()
for color in Color:
    for size in Size: 
        print(f"Color {color}, size {size} is present in bank: {homeworlds.check_bank_for_piece(size, color)}")
print("player 0 choosing homeworld")
homeworlds.choose_homeworld(0, (Size.One, Color.Blue), (Size.Two, Color.Green), (Size.Three, Color.Red))
print("player 1 choosing homeworld")
homeworlds.choose_homeworld(1, (Size.One, Color.Blue), (Size.One, Color.Blue), (Size.One, Color.Blue))
print(format(homeworlds.bank_mask[0],"02x"))
