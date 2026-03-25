import time
from main import find_best_move, load_board, BLACK

def test_timeout():
    # Create a board with many possible moves to force a long search
    board = [[('B' if (r+c)%2==0 else 'W') for c in range(8)] for r in range(8)]
    for r in range(1,7):
        for c in range(1,7):
            board[r][c] = 'O'
    start = time.time()
    move = find_best_move(board, BLACK)
    elapsed = time.time() - start
    print(f"Best move: {move}")
    print(f"Elapsed time: {elapsed:.2f} seconds")
    assert move is not None, "No move returned!"
    assert elapsed < 12, "Timeout did not work (should be under 12 seconds)"

if __name__ == "__main__":
    test_timeout()
