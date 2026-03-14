
BLACK = 'B'
WHITE = 'W'
EMPTY = 'O'   # use whatever matches the board/checker
SIZE = 8
VALID_POSITIONS = {(r, c) for r in range(SIZE) for c in range(SIZE)}
#TODO: this needs to be taken from the input
PLAYER = "B"
BE = "board_early.txt"
BL = "board_late.txt"
BM = "board_mid.txt"


"""
This is going to load in the board from the txt file and clear a single space if full
"""
def load_board(filename):
    board = []
    with open(filename, "r") as f:
        for line in f:
            line = line.strip()
            if line:
                board.append(list(line))
    board = remove_center_if_full(board)
    return board


"""
This takes the chess notation and gives the matrix index
"""
def coord_to_index(coord):
    col = ord(coord[0].upper()) - ord('A')
    row = SIZE - int(coord[1])
    return row, col


"""
This is going to take a index and turn it into a chess cord
"""
def index_to_coord(row, col):
    return chr(ord('A') + col) + str(SIZE - row)


"""
Start and end strings to single move string
"""
def format_move(start, end):
    return f"{start} -> {end}"


"""
Single move string to start and end string
"""
def parse_move(move_string):
    parts = move_string.split(" -> ")
    start = parts[0]
    end = parts[1]
    return start, end


def print_board(board):
    # print column headers (top)
    print("  ", end="")
    for col in range(SIZE):
        print(f" {chr(ord('A') + col)}", end="")
    print()
    
    # print each row with row numbers on left
    for row in range(SIZE):
        row_num = SIZE - row
        print(f"{row_num} ", end="")
        for col in range(SIZE):
            print(f" {board[row][col]}", end="")
        print()
        
        

"""
this checks if a baord is full and will remove peace

This is only going to be run when the boards is read in from the file 
"""
#TODO: This is going to need to be changed to the correct possition
def remove_center_if_full(board):
    for row in range(SIZE):
        for col in range(SIZE):
            if board[row][col] == EMPTY:
                return board  
    
    
    center_row = SIZE // 2
    center_col = SIZE // 2
    board[center_row][center_col] = EMPTY
    print("TRIGGERED")
    
    return board


"""
This is going to check to make sure a move is valid

CHECKS
    - checks if converted indexes are in the range of the board
    - makes sure start position has a peace and end positon is not a peace
    - checks to make sure we are moving the correct color
    - checks the make sure moves are vertical or horizontal
    - checks to make sure we are jumping over a opponent peace
"""
def is_valid_move(board, start_row, start_col, end_row, end_col):
    # check if coordinates are within bounds
    if (start_row, start_col) not in VALID_POSITIONS:
        return False
    if (end_row, end_col) not in VALID_POSITIONS:
        return False
    
    # check if start has a piece and end is empty
    piece = board[start_row][start_col]
    if piece != PLAYER:
        return False
    if piece == EMPTY:
        return False
    if board[end_row][end_col] != EMPTY:
        return False
    
    # must move in a straight line (horizontal or vertical)
    row_diff = end_row - start_row
    col_diff = end_col - start_col
    
    if row_diff != 0 and col_diff != 0:
        return False  # diagonal move not allowed
    
    if row_diff == 0 and col_diff == 0:
        return False  # no movement
    
    # determine direction and distance
    if row_diff != 0:
        # vertical move
        distance = abs(row_diff)
        direction = 1 if row_diff > 0 else -1
        # check all positions between start and end
        for i in range(1, distance):
            check_row = start_row + (i * direction)
            if i % 2 == 1:  # odd positions should have opponent pieces
                if board[check_row][start_col] == EMPTY or board[check_row][start_col] == piece:
                    return False
            else:  # even positions should be empty
                if board[check_row][start_col] != EMPTY:
                    return False
    else:
        # horizontal move
        distance = abs(col_diff)
        direction = 1 if col_diff > 0 else -1
        # check all positions between start and end
        for i in range(1, distance):
            check_col = start_col + (i * direction)
            if i % 2 == 1:  # odd positions should have opponent pieces
                if board[start_row][check_col] == EMPTY or board[start_row][check_col] == piece:
                    return False
            else:  # even positions should be empty
                if board[start_row][check_col] != EMPTY:
                    return False
    
    # distance must be even (jump is 2, 4, 6, etc spaces)
    if distance % 2 != 0:
        return False
    
    return True


"""
This is going to take board, starting and ending positions
    - if this is a valid move it will make the move
        - it will remove the peaces that are going to be jumped over by
            iterating over only that distance and removing things in the middle
    - if this is a invalid move it will not make the move
"""
def move_piece(board, move):
    start, end = parse_move(move)
    start_row, start_col = coord_to_index(start)
    end_row, end_col = coord_to_index(end)
    
    # validate the move first
    if not is_valid_move(board, start_row, start_col, end_row, end_col):
        print("Invalid move")
        return None

    piece = board[start_row][start_col]

    # move the piece
    board[end_row][end_col] = piece
    board[start_row][start_col] = 'O'

    # remove all jumped pieces
    row_diff = end_row - start_row
    col_diff = end_col - start_col
    
    if row_diff != 0:
        # vertical jumps
        direction = 1 if row_diff > 0 else -1
        distance = abs(row_diff)
        for i in range(1, distance, 2):
            board[start_row + (i * direction)][start_col] = 'O'
    else:
        # horizontal jumps
        direction = 1 if col_diff > 0 else -1
        distance = abs(col_diff)
        for i in range(1, distance, 2):
            board[start_row][start_col + (i * direction)] = 'O'
    
    return index_to_coord(end_row, end_col)


"""
This is going to find a single valid move and return this move

************************
THIS IS JUST A STARTING POINT AND WILL NOT WORK FOR THE FINAL VERISON
************************
"""
#TODO: this is going to have to be changed to the alpha beta pruning with minimax
def find_valid_move(board):
    # iterate through all board positions
    for row in range(SIZE):
        for col in range(SIZE):
            # check if this position has a player piece
            if board[row][col] == PLAYER:
                start_coord = index_to_coord(row, col)
                
                # try all four directions: up, down, left, right
                # try distances: 2, 4, 6 (even numbers for valid jumps)
                directions = [
                    (-2, 0), (-4, 0), (-6, 0),  # up
                    (2, 0), (4, 0), (6, 0),     # down
                    (0, -2), (0, -4), (0, -6),  # left
                    (0, 2), (0, 4), (0, 6)      # right
                ]
                
                for row_offset, col_offset in directions:
                    end_row = row + row_offset
                    end_col = col + col_offset
                    
                    # check if this move is valid
                    if is_valid_move(board, row, col, end_row, end_col):
                        end_coord = index_to_coord(end_row, end_col)
                        return format_move(start_coord, end_coord)
    
    return None  # no valid moves found
def find_move_test():
    board = load_board(BE)
    print_board(board)
    print("\n" + "--------------------------------------"+ "\n")
    move = find_valid_move(board)
    print(move + "\n")
    move_piece(board, move)
    print_board(board)

def state1():
    board = load_board(BE)
    print_board(board)
    
def state2():
    board = load_board(BM)
    print_board(board)
    print("-----------------------------------------------------------")
    #valid move
    cord = move_piece(board, "A8 -> C8")
    
    # move_piece(board, "A7", "C7")
    print(cord)
    print_board(board)
        
def main():
    # state1()
    # state2()
    find_move_test()
    
    
    
        
    
        
        
        
if __name__ == "__main__":
    main()