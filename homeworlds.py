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
#these are the only types of moves possible
#each needs unique arguments and validation.
class Move(IntEnum):
    Sacrifice = 0
    Move = 1
    Grow = 2
    Change = 3
    Capture = 4
    Catastrophe = 5
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
        self.stars = 0

    #returns binary position of the piece if a piece of size and color is present in the bank, -1 otherwise
    def check_bank_for_piece(self, size,color):
        search = self.bank_mask&self.size_mask[size]&self.color_mask[color]
        search = ((search >> 1) ^ search) & search
        if bool(search):
            return search
        else:
            return None

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
        #print("Homeworld\t"+format(self.hw_mask[0],"064b"))
        print("Star mask\t"+format(self.star_mask[0],"064b"))
        #for i in range(len(self.star_positions)):
        for i in range(self.stars):
            print(f"At Star {i}\t"+format(self.at_star_mask[i][0],"064b"))
    
    #return the position of the next available piece of a certain color in the bank for grow actions
    def get_next_available_piece_in_bank(self,color):
        search = self.bank_mask & self.size_mask[0] & self.color_mask[color]
        search = ((search << 1) ^ search) & search
        if bool(search):
            return search

        search = self.bank_mask & self.size_mask[1] & self.color_mask[color]
        search = ((search << 1) ^ search) & search
        if bool(search):
            return search

        search = self.bank_mask & self.size_mask[2] & self.color_mask[color]
        search = ((search << 1) ^ search) & search
        if bool(search):
            return search
        return None

    def string_to_piece(self,piece_str):
        color = Color.Blue
        size = Size.One
        if piece_str[0] == 'r':
            color = Color.Red
        elif piece_str[0] == 'g':
            color = Color.Green
        elif piece_str[0] == 'y':
            color = Color.Yellow
        if piece_str[1] == '2':
            size = size.Two
        elif piece_str[1] == '3':
            size = size.Three
        return (color,size)
            
    def create_star(self,player,stars):
        for star in stars:
            star_pos = self.check_bank_for_piece(star[1],star[0])
            if star_pos == None:
                print("Listed star piece could not be found in bank, aborting")
                return False
            self.bank_mask = self.bank_mask & ~star_pos
            if not player == None:
                self.player_mask[player] = self.player_mask[player] | star_pos
            self.star_mask = self.star_mask | star_pos
            self.at_star_mask[self.stars] = self.at_star_mask[self.stars] | star_pos
        self.stars += 1
        return True

    def create_ship(self, player, star_idx, ship):
        ship_pos = self.check_bank_for_piece(ship[1],ship[0])
        if ship_pos == None:
            print("Listed ship piece could not be found in bank, aborting")
            return False
        self.bank_mask = self.bank_mask & ~ship_pos
        self.player_mask[player] = self.player_mask[player] | ship_pos
        self.at_star_mask[star_idx] = self.at_star_mask[star_idx] | ship_pos
        return True
        

    def load_string_state(self,string_state):
        #index of the current star (0=this is player0's homeworld)
        for i, star_str in enumerate(string_state.split()):
            #up to the first ';' is player0's ships at a star:
            player0_ships_str = star_str[:star_str.find(';')].split(',') 
            #print(f"player 0 ship string: {player0_ships_str}")
            player0_ships = [self.string_to_piece(x) for x in player0_ships_str if x != '']
            #print(f"player 0 ship array: {player0_ships}")
            #between the first and second ';' is the star:
            star_piece_str = star_str[star_str.find(';')+1:star_str.rfind(';')].split(',')
            #print(f"star:{star_piece_str}")
            star_piece = [self.string_to_piece(x) for x in star_piece_str if x != '']
            #print(f"star piece: {star_piece}")
            # note idx indicates if we're at the first or last lines(indicating hw)
            player1_ships_str = star_str[star_str.rfind(';')+1:].split(',')
            #print(f"player 1 ship string: {player1_ships_str}")
            player1_ships = [self.string_to_piece(x) for x in player1_ships_str if x != '']
            #print(f"player 1 ship array: {player1_ships}")
            player = None

            if i == 0:
                player = 0
            elif i == len(string_state.split())-1:
                player = 1

            self.create_star(player,star_piece)
                
            #put ships at stars
            for ship in player0_ships:
                self.create_ship(0, i, ship)

            for ship in player1_ships:
                self.create_ship(1, i, ship)

        return False


if __name__ == "__main__":

    homeworlds = homeworlds_board()
    print(bin(homeworlds.bank_mask[0]).count('1'))
    file = open('test_games/test1.txt')
    homeworlds.load_string_state(file.read())
    homeworlds.print_board()
    print(bin(homeworlds.bank_mask[0]).count('1'))
    #for color in Color:
    #    for size in Size: 
    #        print(f"Color {color}, size {size} is present in bank: {homeworlds.check_bank_for_piece(size, color)}")
    #print("player 0 choosing homeworld")
    #homeworlds.choose_homeworld(0, (Size.One, Color.Blue), (Size.Two, Color.Green), (Size.Three, Color.Red))
    #print("player 1 choosing homeworld")
    #homeworlds.choose_homeworld(1, (Size.One, Color.Blue), (Size.One, Color.Blue), (Size.One, Color.Blue))
    #homeworlds.choose_homeworld(1, (Size.Two, Color.Blue), (Size.Three, Color.Green), (Size.Three, Color.Yellow))
    #homeworlds.choose_homeworld(0, (Size.One, Color.Blue), (Size.Two, Color.Green), (Size.Three, Color.Red))
    #homeworlds.move_ship(0, 0, (Size.Three, Color.Red), 1)
    #homeworlds.move_ship(1, 1, (Size.Three, Color.Yellow), 0)
    #homeworlds.move_ship_to_new_star(1,1,(Size.Three, Color.Yellow), (Size.One, Color.Red))
    #homeworlds.move_ship(0, 0, (Size.Three, Color.Yellow), 1)
    #homeworlds.print_board()

