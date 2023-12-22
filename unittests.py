import unittest
import homeworlds as hw

class TestHomeworldSelection(unittest.TestCase):

    def test_homeworld_selection(self):
        #player one's first piece
        valid=0
        invalid=0
        piece_usage = dict()
        for size in hw.Size:
            for color in hw.Color:
                piece_usage[(size,color)] = 0
        #try every possible (and impossible) combination
        for size1 in hw.Size:
            for color1 in hw.Color:
                piece_one = (size1, color1)
                piece_usage[piece_one] += 1
                for size2 in hw.Size:
                    for color2 in hw.Color:
                        piece_two = (size2, color2)
                        piece_usage[piece_two] += 1
                        for size3 in hw.Size:
                            for color3 in hw.Color:
                                piece_three = (size3, color3)
                                piece_usage[piece_three] += 1
                                for size4 in hw.Size:
                                    for color4 in hw.Color:
                                        piece_four = (size4, color4)
                                        piece_usage[piece_four] += 1
                                        for size5 in hw.Size:
                                            for color5 in hw.Color:
                                                piece_five = (size5, color5)
                                                piece_usage[piece_five] += 1
                                                for size6 in hw.Size:
                                                    for color6 in hw.Color:
                                                        piece_six = (size6, color6)
                                                        piece_usage[piece_six] += 1
                                                        #check size and color usage
                                                        expected_result = True
                                                        if 4 in piece_usage.values():
                                                            expected_result = False
                                                        if 5 in piece_usage.values():
                                                            expected_result = False
                                                        if 6 in piece_usage.values():
                                                            expected_result = False
                                                        board = hw.homeworlds_board()
                                                        board.choose_homeworld(0, piece_one, piece_two, piece_three)
                                                        result = board.choose_homeworld(1, piece_four, piece_five, piece_six)
                                                        if expected_result==True:
                                                            valid+=1
                                                        else:
                                                            invalid+=1
                                                        if not result==expected_result:
                                                            print(f"size_usage.values():{size_usage.values()}")
                                                            print(f"color_usage.values():{color_usage.values()}")
                                                            print(f"expected: {expected_result}, got: {result}")
                                                            print(f"p1 tried to select {piece_one}, {piece_two}, {piece_three}")
                                                            print(f"p2 tried to select {piece_four}, {piece_five}, {piece_six}")
                                                        self.assertEqual(result, expected_result, "rejected valid homeworld, or accepted invalid homeworld")
                                                        piece_usage[piece_six] -= 1
                                                piece_usage[piece_five] -= 1
                                        piece_usage[piece_four] -= 1
                                piece_usage[piece_three] -= 1
                        piece_usage[piece_two] -= 1
                piece_usage[piece_one] -= 1
        print(f"valid starts found: {valid}, invalid starts checked: {invalid}")



if __name__ == '__main__':
    unittest.main()
