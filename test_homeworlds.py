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
        #first, test a catastrophe that shouldn't work
        move = [hw.Move.Catastrophe, 0, hw.Color.Yellow]
        self.assertFalse(homeworlds.validate_turn([move]))
        #second, test each catastrophe that should work
        move = [hw.Move.Catastrophe, 0, hw.Color.Blue]
        self.assertTrue(homeworlds.validate_turn([move]))
        #third, test that all possible catastrophes can be triggered in the same move
        turn = [[Move.Catastrophe, 0, Color.Blue],[Move.Catastrophe,0,Color.Green],[Move.Catastrophe,1,Color.Yellow],[Move.Catastrophe, 2, Color.Red]]
        self.assertTrue(homeworlds.validate_turn(turn))


if __name__ == '__main__':
    unittest.main()
