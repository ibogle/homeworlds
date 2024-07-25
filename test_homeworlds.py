import unittest
import homeworlds as hw
from homeworlds import Move, Color

class TestHomeworldSelection(unittest.TestCase):
    
    def test_file_reading(self):
        file = open("test_games/file_reading_test.txt")
        homeworlds = hw.homeworlds_board()
        homeworlds.load_string_state(file.read())
        file.close()
        #test this, probably by reconverting to the string and diffing the input file. SHould be the same.
        #TODO write the conversion from binary to string state
        self.assertTrue(True)

    def test_catastrophe(self):
        file = open("test_games/catastrophe_test.txt")
        homeworlds = hw.homeworlds_board()
        homeworlds.load_string_state(file.read())
        file.close()
        #This doesn't work because there's not enough yellow at the target star
        move = [hw.Move.Catastrophe, 0, hw.Color.Yellow]
        ret, tmp_board = homeworlds.validate_turn([move])
        self.assertFalse(ret)
        self.assertTrue(tmp_board == None)
        #This doesn't work because star 4 doesn't exist
        move = [hw.Move.Catastrophe, 4, hw.Color.Yellow]
        ret, tmp_board = homeworlds.validate_turn([move])
        self.assertFalse(ret)
        self.assertTrue(tmp_board == None)
        #the last catastrophe doesn't work because it references a star that no longer exists (the star moved up one index) 
        move = [[Move.Pass],[Move.Catastrophe, 0, Color.Blue],[Move.Catastrophe,0,Color.Green],[Move.Catastrophe,1,Color.Yellow],[Move.Catastrophe,2,Color.Red]]
        ret, tmp_board = homeworlds.validate_turn(move)
        self.assertFalse(ret)
        self.assertTrue(tmp_board == None)
        #second, test a catastrophe that should work
        move = [hw.Move.Catastrophe, 0, hw.Color.Blue]
        ret, tmp_board = homeworlds.validate_turn([move])
        self.assertTrue(ret)
        self.assertFalse(tmp_board == homeworlds)
        file = open("test_games/catastrophe_test_ans1.txt")
        answer_board = hw.homeworlds_board()
        answer_board.load_string_state(file.read())
        file.close()
        
        self.assertTrue(tmp_board == answer_board)
        #third, test that all possible catastrophes can be triggered in the same move
        turn = [[Move.Pass],[Move.Catastrophe, 0, Color.Blue],[Move.Catastrophe,0,Color.Green],[Move.Catastrophe,1,Color.Yellow],[Move.Catastrophe, 1, Color.Red]]
        ret, tmp_board = homeworlds.validate_turn(turn)
        self.assertTrue(ret)
        self.assertFalse(tmp_board == homeworlds)
        file = open("test_games/catastrophe_test_ans2.txt")
        answer_board = hw.homeworlds_board()
        answer_board.load_string_state(file.read())
        file.close()
        self.assertTrue(tmp_board == answer_board)


if __name__ == '__main__':
    unittest.main()
