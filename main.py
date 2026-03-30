#!/usr/bin/env python3

import sys
import time

BLACK = 'B'
WHITE = 'W'
EMPTY = 'O'   # use whatever matches the board/checker
SIZE = 8
PLAYER = "B"





"""
This is going to load in the board from the txt file
"""
def load_board(filename):
    board = []
    with open(filename, "r") as f:
        for line in f:
            line = line.strip()
            if line:
                board.append(list(line))
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
    return f"{start}-{end}"


"""
Single move string to start and end string
"""
def parse_move(move_string):
    # parts = move_string.split(" -> ")
    # start = parts[0]
    # end = parts[1]
    # return start, end
    move_string = move_string.strip()
    if "-" in move_string:
        start, end = move_string.split("-")
        return start, end
    else:
        return move_string, None


def print_board(board):
    print("  ", end="")
    for col in range(SIZE):
        print(f" {chr(ord('A') + col)}", end="")
    print()
    
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
def is_board_full(board):
    return count_empty(board) == 0


def count_empty(board):
    total = 0
    for row in range(SIZE):
        for col in range(SIZE):
            if board[row][col] == EMPTY:
                total += 1
    return total


def apply_removal_move(board, coord):
    row, col = coord_to_index(coord)
    if board[row][col] == EMPTY:
        return False
    board[row][col] = EMPTY
    return True

"""
This is going to check to make sure a move is valid

CHECKS
    - checks if converted indexes are in the range of the board
    - makes sure start position has a peace and end positon is not a peace
    - checks to make sure we are moving the correct color
    - checks the make sure moves are vertical or horizontal
    - checks to make sure we are jumping over a opponent peace
"""
def is_valid_move(board, start_row, start_col, end_row, end_col, player):
    # check if coordinates are within bounds
    if not (0 <= start_row < SIZE and 0 <= start_col < SIZE):
        return False
    if not (0 <= end_row < SIZE and 0 <= end_col < SIZE):
        return False
    
    # check if start has a piece and end is empty
    piece = board[start_row][start_col]
    if piece != player:
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
This handles the first and second move of the game where a piece is removed instead of moved
    - Default is to take "D5" piece if going first
    - Driver is strict and second piece must also be one of the 4 center pieces
""" 
def find_opening_move(board, player):
    center_stones = ["D5", "E5", "D4", "E4"]

    # first move: full board
    if is_board_full(board):
        if player == BLACK:
            return "D5"
        else:
            return "E5"

    # second move: exactly one empty square
    if count_empty(board) == 1:
        empty_coord = None

        for row in range(SIZE):
            for col in range(SIZE):
                if board[row][col] == EMPTY:
                    empty_coord = index_to_coord(row, col)

        # allowed responses based on which center stone was removed first
        if empty_coord == "D5":
            candidates = ["E5", "D4"]
        elif empty_coord == "E5":
            candidates = ["D5", "E4"]
        elif empty_coord == "D4":
            candidates = ["D5", "E4"]
        elif empty_coord == "E4":
            candidates = ["E5", "D4"]
        else:
            candidates = []

        for coord in candidates:
            row, col = coord_to_index(coord)
            if board[row][col] == player:
                return coord

    return None

"""
This is going to take board, starting and ending positions
    - if this is a valid move it will make the move
        - it will remove the peaces that are going to be jumped over by
            iterating over only that distance and removing things in the middle
    - if this is a invalid move it will not make the move
"""
def move_piece(board, move, player):
    start, end = parse_move(move)

    # opening removal move support
    if end is None:
        if apply_removal_move(board, start):
            return start
        return None
    
    start_row, start_col = coord_to_index(start)
    end_row, end_col = coord_to_index(end)
    
    # validate the move first
    if not is_valid_move(board, start_row, start_col, end_row, end_col, player):
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
                    if is_valid_move(board, row, col, end_row, end_col, PLAYER):
                        end_coord = index_to_coord(end_row, end_col)
                        return format_move(start_coord, end_coord)
    
    return None  # no valid moves found

def evaluate_tile_mobility_signed(board, player):
    """
    Returns an 8x8 matrix:
    - Your pieces: positive move count
    - Opponent pieces: negative move count
    - Empty: 0
    """
    mobility_matrix = [[0 for _ in range(SIZE)] for _ in range(SIZE)]
    opponent = WHITE if player == BLACK else BLACK

    directions = [
        (-2, 0), (-4, 0), (-6, 0),  # up
        (2, 0), (4, 0), (6, 0),     # down
        (0, -2), (0, -4), (0, -6),  # left
        (0, 2), (0, 4), (0, 6)      # right
    ]

    for row in range(SIZE):
        for col in range(SIZE):
            piece = board[row][col]
            if piece == EMPTY:
                mobility_matrix[row][col] = 0
            elif piece == player or piece == opponent:
                move_count = 0
                for row_offset, col_offset in directions:
                    end_row = row + row_offset
                    end_col = col + col_offset
                    if is_valid_move(board, row, col, end_row, end_col, piece):
                        move_count += 1
                if piece == player:
                    mobility_matrix[row][col] = move_count
                else:
                    mobility_matrix[row][col] = -move_count
    return mobility_matrix

def get_all_move_evaluations(board, player):
    """
    For each possible move for the player, generate the resulting board,
    call evaluate_tile_mobility_signed, and store:
      - 'move': move string
      - 'start': (row, col)
      - 'end': (row, col)
      - 'eval_sum': sum of evaluation matrix after move
    Returns a list of dicts, one per possible move.
    """
    moves = []
    directions = [
        (-2, 0), (-4, 0), (-6, 0),  # up
        (2, 0), (4, 0), (6, 0),     # down
        (0, -2), (0, -4), (0, -6),  # left
        (0, 2), (0, 4), (0, 6)      # right
    ]
    opponent = WHITE if player == BLACK else BLACK
    for row in range(SIZE):
        for col in range(SIZE):
            if board[row][col] == player:
                start_coord = index_to_coord(row, col)
                for row_offset, col_offset in directions:
                    end_row = row + row_offset
                    end_col = col + col_offset
                    if is_valid_move(board, row, col, end_row, end_col, player):
                        end_coord = index_to_coord(end_row, end_col)
                        move_str = format_move(start_coord, end_coord)
                        # Make a deep copy of the board and apply the move
                        board_copy = [r[:] for r in board]
                        move_piece(board_copy, move_str, player)
                        # Evaluate the resulting board
                        eval_sum = evaluate_board_weighted(board_copy, player)
                        # Now, generate all possible opponent replies from this board state
                        replies = []
                        for opp_row in range(SIZE):
                            for opp_col in range(SIZE):
                                if board_copy[opp_row][opp_col] == opponent:
                                    opp_start = index_to_coord(opp_row, opp_col)
                                    for opp_row_offset, opp_col_offset in directions:
                                        opp_end_row = opp_row + opp_row_offset
                                        opp_end_col = opp_col + opp_col_offset
                                        if is_valid_move(board_copy, opp_row, opp_col, opp_end_row, opp_end_col, opponent):
                                            opp_end = index_to_coord(opp_end_row, opp_end_col)
                                            opp_move_str = format_move(opp_start, opp_end)
                                            replies.append({
                                                'move': opp_move_str,
                                                'start': (opp_row, opp_col),
                                                'end': (opp_end_row, opp_end_col)
                                            })
                        moves.append({
                            'move': move_str,
                            'start': (row, col),
                            'end': (end_row, end_col),
                            'eval_sum': eval_sum,
                            'replies': replies
                        })
    return moves

def alphabeta_on_evaluations(moves, depth, alpha, beta, is_maximizing, board, player):
    """
    Runs alpha-beta pruning on the move list from get_all_move_evaluations.
    Returns (best_move_string, best_score).
    Supports a timeout: if time.time() - start_time > time_limit, returns best move so far.
    """
    # Use globals for timing
    global _ALPHABETA_START_TIME, _ALPHABETA_TIME_LIMIT, _ALPHABETA_TIMEOUT
    opponent = WHITE if player == BLACK else BLACK

    # Check for timeout
    if time.time() - _ALPHABETA_START_TIME > _ALPHABETA_TIME_LIMIT:
        _ALPHABETA_TIMEOUT = True
        return None, float('-inf') if is_maximizing else float('inf')

    if not moves:
        score = float('-inf') if is_maximizing else float('inf')
        return None, score

    best_move = None

    if is_maximizing:
        best_val = float('-inf')
        for entry in moves:
            # Check for timeout at each iteration
            if time.time() - _ALPHABETA_START_TIME > _ALPHABETA_TIME_LIMIT:
                _ALPHABETA_TIMEOUT = True
                break
            score = entry['eval_sum']

            # Go deeper using the opponent's replies if we can
            if depth > 1 and entry['replies']:
                board_copy = [r[:] for r in board]
                move_piece(board_copy, entry['move'], player)
                opp_moves = get_all_move_evaluations(board_copy, opponent)
                _, score = alphabeta_on_evaluations(
                    opp_moves, depth - 1, alpha, beta, False, board_copy, opponent
                )
                if _ALPHABETA_TIMEOUT:
                    break

            if score > best_val:
                best_val = score
                best_move = entry['move']

            alpha = max(alpha, score)
            if beta <= alpha:
                break  # prune

        return best_move, best_val

    else:
        best_val = float('inf')
        for entry in moves:
            # Check for timeout at each iteration
            if time.time() - _ALPHABETA_START_TIME > _ALPHABETA_TIME_LIMIT:
                _ALPHABETA_TIMEOUT = True
                break
            score = entry['eval_sum']

            if depth > 1 and entry['replies']:
                board_copy = [r[:] for r in board]
                move_piece(board_copy, entry['move'], opponent)
                our_moves = get_all_move_evaluations(board_copy, player)
                _, score = alphabeta_on_evaluations(
                    our_moves, depth - 1, alpha, beta, True, board_copy, player
                )
                if _ALPHABETA_TIMEOUT:
                    break

            if score < best_val:
                best_val = score
                best_move = entry['move']

            beta = min(beta, score)
            if beta <= alpha:
                break  # prune

        return best_move, best_val


def find_best_move(board, player):
    """Calls get_all_move_evaluations then picks the best move via alpha-beta."""
    moves = get_all_move_evaluations(board, player)
    if not moves:
        return None
    moves.sort(key=lambda x: x['eval_sum'], reverse=True)
    # Set up timing globals
    global _ALPHABETA_START_TIME, _ALPHABETA_TIME_LIMIT, _ALPHABETA_TIMEOUT
    _ALPHABETA_START_TIME = time.time()
    _ALPHABETA_TIME_LIMIT = 10.0  # seconds
    _ALPHABETA_TIMEOUT = False
    best_move = None
    best_val = float('-inf')
    try:
        best_move, best_val = alphabeta_on_evaluations(
            moves,
            depth=5,
            alpha=float('-inf'),
            beta=float('inf'),
            is_maximizing=True,
            board=board,
            player=player
        )
    except Exception as e:
        print(e, file=sys.stderr)
    # If timeout, best_move may be None; fallback to first move
    if best_move is None and moves:
        best_move = moves[0]['move']
    return best_move

def evaluate_tile_safety(board, player):
    """
    Returns an 8x8 matrix:
    - Your pieces: positive if not capturable in one move, negative if capturable
    - Opponent pieces: negative if not capturable, positive if capturable
    - Empty: 0
    """
    safety_matrix = [[0 for _ in range(SIZE)] for _ in range(SIZE)]
    opponent = WHITE if player == BLACK else BLACK
    adjacent = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for row in range(SIZE):
        for col in range(SIZE):
            piece = board[row][col]
            if piece == EMPTY:
                safety_matrix[row][col] = 0
            elif piece == player or piece == opponent:
                # Assume safe until proven unsafe
                safe = 1
                checker = opponent if piece == player else player
                for dr, dc in adjacent:
                    adj_row, adj_col = row + dr, col + dc
                    land_row, land_col = row - dr, col - dc
                    if (0 <= adj_row < SIZE and 0 <= adj_col < SIZE and
                        0 <= land_row < SIZE and 0 <= land_col < SIZE):
                        if board[adj_row][adj_col] == checker:
                            if is_valid_move(board, adj_row, adj_col, land_row, land_col, checker):
                                safe = 0
                                break
                if piece == player:
                    safety_matrix[row][col] = safe
                else:
                    safety_matrix[row][col] = -safe
    return safety_matrix

def evaluate_center_control(board, player):
    """
    Returns a single score: number of player's pieces in the 4 center squares minus opponent's.
    """
    center_coords = [(3, 3), (3, 4), (4, 3), (4, 4)]  # D4, D5, E4, E5 (0-indexed)
    player_count = 0
    opponent = WHITE if player == BLACK else BLACK
    opponent_count = 0
    for row, col in center_coords:
        if board[row][col] == player:
            player_count += 1
        elif board[row][col] == opponent:
            opponent_count += 1
    return player_count - opponent_count

def evaluate_board_weighted(board, player, w_mob=0.4, w_safe=0.4, w_center=0.2):
    opponent = WHITE if player == BLACK else BLACK
    directions = [(-2,0),(-4,0),(-6,0),(2,0),(4,0),(6,0),(0,-2),(0,-4),(0,-6),(0,2),(0,4),(0,6)]

    mobility = 0
    for row in range(SIZE):
        for col in range(SIZE):
            piece = board[row][col]
            if piece == EMPTY:
                continue
            for dr, dc in directions:
                if is_valid_move(board, row, col, row+dr, col+dc, piece):
                    mobility += 1 if piece == player else -1

    safety_matrix = evaluate_tile_safety(board, player)
    safety_score = sum(val for row in safety_matrix for val in row)
    center_score = evaluate_center_control(board, player)
    return w_mob * mobility + w_safe * safety_score + w_center * center_score

def choose_move(board, player):
    opening_move = find_opening_move(board, player)
    if opening_move is not None:
        return opening_move

    global PLAYER
    PLAYER = player
    return find_best_move(board, player)  #  was find_valid_move(board)
      
def main():
    # check for correct arguments
    if len(sys.argv) != 3:
        return
    
    board_file = sys.argv[1]
    player = sys.argv[2]

    global PLAYER
    PLAYER = player

    board = load_board(board_file)

    # Track number of opening removals (first two moves are removals)
    opening_removals = 0

    my_move = choose_move(board, player)
    if my_move is not None and '-' not in my_move:
        opening_removals += 1
    if my_move is None:
        print("you win", flush=True)
        sys.exit(0)

    print(my_move, flush=True)
    move_piece(board, my_move, player)

    while True:
        try:
            opponent_move = input()
        except EOFError:
            sys.exit(0)

        if not opponent_move:
            sys.exit(0)

        if opponent_move.strip() == "you win":
            sys.exit(0)

        opponent = WHITE if player == BLACK else BLACK
        move_piece(board, opponent_move, opponent)

        if '-' not in opponent_move:
            opening_removals += 1

        my_move = choose_move(board, player)
        if my_move is not None and opening_removals < 2 and '-' not in my_move:
            opening_removals += 1
        elif my_move is None:
            print("you win", flush=True)
            sys.exit(0)

        print(my_move, flush=True)
        move_piece(board, my_move, player)

if __name__ == "__main__":
    main()