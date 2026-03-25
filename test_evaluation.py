import unittest
from main import evaluate_board_weighted, alphabeta_on_evaluations, get_all_move_evaluations, load_board, BLACK, WHITE

class TestEvaluationFunction(unittest.TestCase):
    def setUp(self):
        # Define 5 different board states as lists of lists
        self.boards = []
        # Board 1: Full board, all black
        self.boards.append([[BLACK]*8 for _ in range(8)])
        # Board 2: Full board, all white
        self.boards.append([[WHITE]*8 for _ in range(8)])
        # Board 3: Center empty
        board3 = [[BLACK]*8 for _ in range(8)]
        for r in [3,4]:
            for c in [3,4]:
                board3[r][c] = 'O'
        self.boards.append(board3)
        # Board 4: Alternating black and white
        board4 = [[BLACK if (r+c)%2==0 else WHITE for c in range(8)] for r in range(8)]
        self.boards.append(board4)
        # Board 5: Custom mid-game state
        board5 = [
            list("BBBBWOOO"),
            list("BWBWOOOO"),
            list("BWBWOOOO"),
            list("OOOOOOOO"),
            list("OOOOOOOO"),
            list("OOOOOOOO"),
            list("OOOOOOOO"),
            list("OOOOOOOO"),
        ]
        self.boards.append(board5)

        # Board 6: Many possible moves (alternating pattern, but with larger empty area)
        board6 = [[('B' if (r+c)%2==0 else 'W') for c in range(8)] for r in range(8)]
        for r in range(1,7):
            for c in range(1,7):
                board6[r][c] = 'O'  # create a larger open area in the center
        self.boards.append(board6)

    def test_evaluate_board_weighted(self):
        # Just check that the function runs and returns a float
        for i, board in enumerate(self.boards):
            score_black = evaluate_board_weighted(board, BLACK)
            score_white = evaluate_board_weighted(board, WHITE)
            self.assertIsInstance(score_black, float, f"Board {i+1} black score not float")
            self.assertIsInstance(score_white, float, f"Board {i+1} white score not float")

    def test_alphabeta_on_evaluations_depth5(self):
        # For each board, get moves for black, run alphabeta at depth 5, and check output
        for i, board in enumerate(self.boards):
            moves = get_all_move_evaluations(board, BLACK)
            if moves:
                best_move, best_val = alphabeta_on_evaluations(moves, 5, float('-inf'), float('inf'), True, board, BLACK)
                self.assertIsInstance(best_move, str, f"Board {i+1} best_move not str (depth 5)")
                self.assertIsInstance(best_val, float, f"Board {i+1} best_val not float (depth 5)")
                # For board 6 (many moves), ensure there are at least 10 possible moves
                if i == 5:
                    self.assertGreaterEqual(len(moves), 10, "Board 6 should have many possible moves for black")
            else:
                self.assertEqual(moves, [], f"Board {i+1} should have no moves (depth 5)")

if __name__ == '__main__':
    unittest.main()
