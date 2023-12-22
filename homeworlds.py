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
            #print("found the piece")
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
            #print(f"Player {player} already has a homeworld")
            return False
        size1, color1 = star1
        size2, color2 = star2
        size3, color3 = ship

        #last minute validation, will probably check this beforehand
        #print(format(self.bank_mask[0],"02x"))
        star1_pos = self.check_bank_for_piece(size1, color1)
        if star1_pos != None:
            self.bank_mask[0] = self.bank_mask[0] & ~star1_pos[0]
        #else:
            #print("star1_pos not found")
        #print(format(self.bank_mask[0],"02x"))
        star2_pos = self.check_bank_for_piece(size2, color2)
        if star2_pos != None:
            self.bank_mask[0] = self.bank_mask[0] & ~star2_pos[0]
        #else:
            #print("star2_pos not found")
        #print(format(self.bank_mask[0],"02x"))
        ship_pos  = self.check_bank_for_piece(size3, color3)
        if ship_pos != None:
            self.bank_mask[0] = self.bank_mask[0] & ~ship_pos[0]
        #else:
            #print("ship_pos not found")
        if(star1_pos != None and star2_pos != None and ship_pos != None):
            #change hw_mask, player_mask[player], star_mask, star_positions, and at_star_mask[len(star_positions)+1]
            self.hw_mask[0]          = self.hw_mask[0]          | star1_pos[0] | star2_pos[0]
            self.player_mask[player] = self.player_mask[player] | star1_pos[0] | star2_pos[0] | ship_pos[0]
            self.star_mask[0]        = self.star_mask[0]        | star1_pos[0] | star2_pos[0]
            self.star_positions.append(star1_pos | star2_pos)
            self.at_star_mask[len(self.star_positions)-1] = ship_pos[0]
            return True
        else:
            # the pieces aren't in the bank, somehow?
            #print(f"Player {player} requested an invalid start")
            #bank_mask[0] = bank_mask[0] | star1_pos | star2_pos | ship_pos
            if star1_pos != None:
                self.bank_mask[0] = self.bank_mask[0] | star1_pos
            if star2_pos != None:
                self.bank_mask[0] = self.bank_mask[0] | star2_pos
            if ship_pos != None:
                self.bank_mask[0] = self.bank_mask[0] | ship_pos
            return False

    def print_board(self):
        print("bank_mask\t"+format(self.bank_mask[0],"064b"))
        print("Red\t\t"+format(self.color_mask[0][0],"064b"))
        print("Green\t\t"+format(self.color_mask[1][0],"064b"))
        print("Yellow\t\t"+format(self.color_mask[2][0],"064b"))
        print("Blue\t\t"+format(self.color_mask[3][0],"064b"))
        print("Size 1\t\t"+format(self.size_mask[0][0],"064b"))
        print("Size 2\t\t"+format(self.size_mask[1][0],"064b"))
        print("Size 3\t\t"+format(self.size_mask[2][0],"064b"))
        print("Player 0\t"+format(self.player_mask[0][0],"064b"))
        print("Player 1\t"+format(self.player_mask[1][0],"064b"))
        print("Homeworld\t"+format(self.hw_mask[0],"064b"))
        print("Star mask\t"+format(self.star_mask[0],"064b"))
        for i in range(len(self.star_positions)):
            print(f"At Star {i}\t"+format(self.at_star_mask[i][0],"064b") + " \nStar pos = \t"+format(self.star_positions[i][0],"064b"))
    #origin and dest are star_IDs (handles homeworlds easily)
    def move_ship(self,player,origin,ship,dest, sacrifice = False):
        if(len(self.star_positions) <= dest or origin == dest):
            print("dest star is either origin, or does not yet exist")
            return False
        if sacrifice or not bool(self.color_mask[Color.Yellow][0] & (self.star_positions[origin][0] | (self.at_star_mask[origin][0] & self.player_mask[player][0]))):
            print(f"star is not yellow and does not contain any yellow owned by player {player}")
            return False
        ship_size, ship_color = ship
        for i in Size:
            if bool(self.size_mask[i][0] & self.star_positions[origin][0]) and bool(self.size_mask[i][0] & self.star_positions[dest][0]):
                #at least one star has a size in common, can't move there bro!
                print("this is an invalid move bc star sizes")
                return False
        #can do move, so do
        #find the ship at the origin

        if not bool(self.at_star_mask[origin][0] & self.player_mask[player][0] & self.color_mask[ship_color][0] & self.size_mask[ship_size][0]):
            print(f"requested ship does not exist at origin star for player {player}")
            return False

        search = np.array([0x8000000000000000],dtype=np.uint64)
        while not (search & self.player_mask[player][0] & self.at_star_mask[origin][0] & self.color_mask[ship_color][0] & self.size_mask[ship_size][0]):
            search = search >> 1
        #search holds the position of the first ship of that size & color at the origin star
        self.at_star_mask[origin][0] = self.at_star_mask[origin][0] & (~search[0])
        self.at_star_mask[dest][0] = self.at_star_mask[dest][0] | search[0]
        return True

    def move_ship_to_new_star(self, player, origin, ship, dest, sacrifice=False):
        size, color = dest
        star_pos = self.check_bank_for_piece(size,color)
        if star_pos == None:
            print("requested star isn't available in the bank")
            return False
        self.bank_mask[0] = self.bank_mask[0] & ~star_pos[0]
        self.star_mask[0] = self.star_mask[0] | star_pos[0]
        self.star_positions.append(star_pos)
        #self.at_star_mask[len(self.star_positions)-1] = np.array([0x0000000000000000],dtype=np.uint64)
        if self.move_ship(player, origin, ship, len(self.star_positions)-1, sacrifice):
            return True
        #move didn't work, take down the star that was created
        self.star_mask[0] = self.star_mask[0] & (~star_pos[0])
        self.star_positions.pop()
        return False
    
    #return the position of the next available piece of a certain color in the bank for grow actions
    def get_next_available_piece_in_bank(self,color):
        search = np.array([0x0000000010000000],dtype=np.uint64)
        while not (search & self.color_mask[color][0] & self.bank_mask[0]):
            search = search << 1
        if bool(search):
            return search
        else:
            return None
    #this wraps a move action, it will check whether a new star needs to be created, and destroy a star that is empty after the move
    def move_ship_action(self, player, origin, ship, dest):
        #if dest is a tuple, create a new star
        success = False
        if type(dest) is tuple:
            success = move_ship_to_new_star(self, player, origin, ship, dest) 
        #else check if dest & star_mask != 0
        else:
            success = move_ship(self,player,origin,ship,dest)
        
        if success:
            if self.at_star_mask[origin][0] & self.star_positions[origin] == self.star_positions[origin]:
                #this star is empty, remove origin from star_pos, at_star_mask, star_mask, and add it back to the bank_mask
                print("unimplemented, as yet")

        return success
    #single instance of a sacrifice move, do not destroy the star after moving away 
    def sacrifice_move(self, origin, ship, dest):
        return False


if __name__ == "__main__":

    homeworlds = homeworlds_board()
    for color in Color:
        for size in Size: 
            print(f"Color {color}, size {size} is present in bank: {homeworlds.check_bank_for_piece(size, color)}")
    print("player 0 choosing homeworld")
    homeworlds.choose_homeworld(0, (Size.One, Color.Blue), (Size.Two, Color.Green), (Size.Three, Color.Red))
    print("player 1 choosing homeworld")
    homeworlds.choose_homeworld(1, (Size.One, Color.Blue), (Size.One, Color.Blue), (Size.One, Color.Blue))
    homeworlds.choose_homeworld(1, (Size.Two, Color.Blue), (Size.Three, Color.Green), (Size.Three, Color.Yellow))
    homeworlds.choose_homeworld(0, (Size.One, Color.Blue), (Size.Two, Color.Green), (Size.Three, Color.Red))
    homeworlds.move_ship(0, 0, (Size.Three, Color.Red), 1)
    homeworlds.move_ship(1, 1, (Size.Three, Color.Yellow), 0)
    homeworlds.move_ship_to_new_star(1,1,(Size.Three, Color.Yellow), (Size.One, Color.Red))
    homeworlds.move_ship(0, 0, (Size.Three, Color.Yellow), 1)
    homeworlds.print_board()

