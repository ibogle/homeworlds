import numpy as np
from enum import IntEnum
import warnings
import copy
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
#Also, importantly, move types are aligned with piece colors, so a given ship action can be checked against a color.
class Move(IntEnum):
    Capture = 0
    Grow = 1
    Move = 2
    Transform = 3
    #End of ship actions
    Sacrifice = 4
    Catastrophe = 5
    Pass = 6
#TODO
# implement validation framework:
#   Takes array of moves and args
#   Validates: Are these moves possible given the current board state?
#   returns True if yeah, False if nah

# Pieces do not move, they just change player ownership and star proximity, so only update the player, star, and at_star masks for board state
class homeworlds_board:
    def __eq__(self, other):
        if self.stars != other.stars:
            return False
        for star in range(self.stars):
            for color in Color:
                for size in Size:
                    for player in range(self.players):
                        #check that all the same amount of pieces are used at each star by each player
                        if bin(self.at_star_mask[star][0] & self.color_mask[color][0] & self.size_mask[size][0] & self.player_mask[player][0]).count('1') != \
                           bin(other.at_star_mask[star][0] & other.color_mask[color][0] & other.size_mask[size][0] & other.player_mask[player][0]).count('1'):
                            return False
                        #check that the stars are all the same too
                        if bin(self.at_star_mask[star][0] & self.color_mask[color][0] & self.size_mask[size][0] & self.star_mask[0]).count('1') != \
                           bin(other.at_star_mask[star][0] & other.color_mask[color][0] & other.size_mask[size][0] & other.star_mask[0]).count('1'):
                            return False

        return (self.size_mask == other.size_mask).all() and (self.color_mask == other.color_mask).all() and self.players == other.players and self.size_max == other.size_max and self.stars == other.stars
    def __init__(self, orig=None):
        if orig is None:
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
        else:
            self.bank_mask = copy.deepcopy(orig.bank_mask)
            self.size_mask = copy.deepcopy(orig.size_mask)
            self.color_mask = copy.deepcopy(orig.color_mask)
            self.player_mask = copy.deepcopy(orig.player_mask)
            self.star_mask = copy.deepcopy(orig.star_mask)
            self.at_star_mask = copy.deepcopy(orig.at_star_mask)
            self.players = copy.deepcopy(orig.players)
            self.size_max = copy.deepcopy(orig.size_max)
            self.stars = copy.deepcopy(orig.stars)

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
        search = self.bank_mask & (self.size_mask[0]|self.size_mask[1]|self.size_mask[2]) & self.color_mask[color]
        search = search & -search
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
    #need some way of checking if the piece sacrificed is valid for the type of action
    def validate_ship_action(self, move, sacrifice=False):
        return False
    #just make sure the piece exists where the player says it does
    def validate_sacrifice(self, move):
        return False, Color.Red, Size.One
    
    def validate_catastrophe(self,move):
        #catastrophe move structure:
        #[Move.Catastrophe, star_idx, color]
        if len(move) > 3:
            print("Malformed catastrophe move structure")
            return False
        if move[1] >= self.stars:
            return False
        pieces_of_target_color = self.at_star_mask[move[1]][0] & self.color_mask[move[2]][0]
        if bin(pieces_of_target_color).count('1') >=4:
            return True
        return False
    def execute_catastrophe(self,move):
        #catastrophe move structure:
        #[Move.Catastrophe, star_idx, color]
        temp_board = homeworlds_board(self)
        pieces_of_target_color = temp_board.at_star_mask[move[1]] & temp_board.color_mask[move[2]]
        #if the last star at a system is destroyed, clear out the star, and put everything back in the bank
        if bool(temp_board.star_mask & pieces_of_target_color) and bin(temp_board.star_mask[0] & temp_board.at_star_mask[move[1]][0]).count('1') == 1:
            pieces = temp_board.at_star_mask[move[1]][0]
            temp_board.bank_mask = temp_board.bank_mask | pieces
            temp_board.star_mask = temp_board.star_mask & ~(temp_board.star_mask & pieces)
            temp_board.player_mask[0] = temp_board.player_mask[0] & ~(temp_board.player_mask[0] & pieces)
            temp_board.player_mask[1] = temp_board.player_mask[1] & ~(temp_board.player_mask[1] & pieces)
            #temp_board.at_star_mask.remove(temp_board.at_star_mask[move[1]])
            temp_board.at_star_mask = np.delete(temp_board.at_star_mask,move[1],axis=0)
            temp_board.stars = temp_board.stars-1
            temp_board.at_star_mask = np.append(temp_board.at_star_mask,np.array([[0x0000000000000000]],dtype=np.uint64),axis=0)
        else:
            temp_board.bank_mask = temp_board.bank_mask | pieces_of_target_color
            temp_board.star_mask = temp_board.star_mask & ~(temp_board.star_mask & pieces_of_target_color)
            temp_board.player_mask[0] = temp_board.player_mask[0] & ~(temp_board.player_mask[0] & pieces_of_target_color)
            temp_board.player_mask[1] = temp_board.player_mask[1] & ~(temp_board.player_mask[1] & pieces_of_target_color)
            temp_board.at_star_mask[move[1]][0] = temp_board.at_star_mask[move[1]][0] & ~pieces_of_target_color

        return temp_board



    #this function simply returns true if the moves proposed were able to be completed
    # this cannot be separated from executing the moves, as the board state will change due to moves in the turn
    # create a copy of the current board, try the moves, and return the new board if the moves were valid.
    def validate_turn(self, moves):
        #check that a turn has one pass or one sacrifice or one ship action, otherwise it's not a valid turn
        #checking that the number of actions are correct with the sacrifice is done by trying to execute the moves.
        move_types = [x[0] for x in moves]
        move_dict = dict()
        for move in move_types:
            if move in move_dict:
                move_dict[move] = move_dict[move] + 1
            else:
                move_dict[move] = 1
        if Move.Pass in move_dict and (0 in move_dict or 1 in move_dict or 2 in move_dict or 3 in move_dict or 4 in move_dict) :
            #can't pass and also do something other than a catastrophe
            print("rejecting because there's a pass with a ship action")
            return False, None
        if not Move.Sacrifice in move_dict:
            if Move.Move in move_dict and move_dict[Move.Move] > 1:
                return False, None
            if Move.Grow in move_dict and move_dict[Move.Grow] > 1:
                return False, None
            if Move.Transform in move_dict and move_dict[Move.Transform] > 1:
                return False, None
            if Move.Capture in move_dict and move_dict[Move.Capture] > 1:
                return False, None

        temp_board = homeworlds_board(self)
        sacrifice = False
        sacrifice_color = Color.Red
        sacrifice_size = Size.One
        for move in moves:
            if move[0] == Move.Sacrifice:
                ret, sacrifice_color, sacrifice_size = temp_board.validate_sacrifice(move)
                if ret == False:
                    return False, None
                #do the action on temp_board
            elif move[0] == Move.Pass:
                # check that there isn't a ship action or sacrifice in this set of moves,
                # if there is, this Pass is invalid
                continue # a turn with a pass might have catastrophes in it, still have to validate those.
            elif move[0] == Move.Catastrophe:
                ret = temp_board.validate_catastrophe(move)
                if ret == False:
                    return False, None
                #do the action on temp_board
                temp_board = temp_board.execute_catastrophe(move)
            else:
                if sacrifice and move[0] == sacrifice_color and sacrifice_size > 0 :
                    sacrifice_size = sacrifice_size - 1
                    ret = temp_board.validate_ship_action(move, True)
                    if ret == False:
                        return False, None
                    #do the action on temp_board
                elif sacrifice == False:
                    ret = temp_board.validate_ship_action(move)
                    if ret == False:
                        return False, None
                    #do the action on temp_board
        #set temp_board equal to self
        return True, temp_board
    


if __name__ == "__main__":

    homeworlds = homeworlds_board()
    print(bin(homeworlds.bank_mask[0]).count('1'))
    file = open('test_games/test1.txt')
    homeworlds.load_string_state(file.read())
    homeworlds.print_board()
    ##use the below code to count number of ones (check catastrophes and such)
    #print(bin(homeworlds.bank_mask[0]).count("1"))
